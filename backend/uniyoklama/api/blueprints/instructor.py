from __future__ import annotations

from datetime import datetime, timedelta, timezone, time as dtime
from typing import Optional, List, Dict, Any
from zoneinfo import ZoneInfo

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity

from ..rbac import require_roles
from ..responses import error_response
from ...extensions import db
from ...models import (
    ClassSession,
    CourseOffering,
    OfferingInstructor,
    Attendance,
    User,
    MeetingPattern,
    Announcement,
)
from ...schemas import InstructorSessionDetailSchema, QRResponseSchema
from ...utils.qr import create_qr_token, make_qr_png_bytes, png_bytes_to_data_url
from ...utils.schedule import generate_sessions_for_offering

bp = Blueprint("instructor", __name__, url_prefix="/instructor")


def _ensure_instructor_owns_offering(instructor_id: int, offering_id: int) -> bool:
    q = db.select(OfferingInstructor).where(
        OfferingInstructor.offering_id == offering_id,
        OfferingInstructor.instructor_id == instructor_id,
    )
    return db.session.execute(q).scalar_one_or_none() is not None


def _ensure_instructor_owns_session(instructor_id: int, session: ClassSession) -> bool:
    return _ensure_instructor_owns_offering(instructor_id, session.offering_id)


def _parse_hhmm(s: str) -> Optional[dtime]:
    s = (s or "").strip()
    if not s:
        return None
    try:
        parts = s.split(":")
        hh = int(parts[0])
        mm = int(parts[1]) if len(parts) > 1 else 0
        ss = int(parts[2]) if len(parts) > 2 else 0
        return dtime(hour=hh, minute=mm, second=ss)
    except Exception:
        return None


@bp.get("/offerings")
@require_roles("INSTRUCTOR")
def my_offerings():
    instructor_id = int(get_jwt_identity())

    q = (
        db.select(CourseOffering)
        .join(OfferingInstructor, OfferingInstructor.offering_id == CourseOffering.id)
        .where(OfferingInstructor.instructor_id == instructor_id)
        .order_by(CourseOffering.id.desc())
    )
    offerings = db.session.execute(q).scalars().all()

    tz = ZoneInfo(str(current_app.config.get("TIMEZONE", "Europe/Istanbul")))
    now = datetime.now(tz).replace(tzinfo=None)
    items: List[Dict[str, Any]] = []
    for o in offerings:
        next_session = db.session.execute(
            db.select(ClassSession)
            .where(ClassSession.offering_id == o.id, ClassSession.starts_at >= now)
            .order_by(ClassSession.starts_at.asc())
            .limit(1)
        ).scalar_one_or_none()

        sess_count = db.session.execute(
            db.select(db.func.count(ClassSession.id)).where(ClassSession.offering_id == o.id)
        ).scalar_one()

        mp_count = db.session.execute(
            db.select(db.func.count(MeetingPattern.id)).where(MeetingPattern.offering_id == o.id)
        ).scalar_one()

        items.append(
            {
                "id": o.id,
                "course_code": o.course.code if o.course else "",
                "course_title": o.course.title if o.course else "",
                "term_code": o.term.code if o.term else "",
                "section": o.section,
                "capacity": o.capacity,
                "meeting_patterns": int(mp_count),
                "sessions_total": int(sess_count),
                "next_session_id": next_session.id if next_session else None,
                "next_session_starts_at": next_session.starts_at.isoformat() if next_session else None,
            }
        )

    return jsonify({"items": items})


@bp.get("/offerings/<int:offering_id>/meeting-patterns")
@require_roles("INSTRUCTOR")
def list_meeting_patterns(offering_id: int):
    instructor_id = int(get_jwt_identity())
    if not _ensure_instructor_owns_offering(instructor_id, offering_id):
        return error_response("FORBIDDEN", "Bu ders/şube size ait değil.", 403)

    patterns = db.session.execute(
        db.select(MeetingPattern).where(MeetingPattern.offering_id == offering_id).order_by(MeetingPattern.weekday.asc(), MeetingPattern.starts_time.asc())
    ).scalars().all()

    items = [
        {
            "id": p.id,
            "weekday": int(p.weekday),
            "starts_time": p.starts_time.strftime("%H:%M"),
            "ends_time": p.ends_time.strftime("%H:%M"),
        }
        for p in patterns
    ]
    return jsonify({"items": items})


@bp.post("/offerings/<int:offering_id>/meeting-patterns")
@require_roles("INSTRUCTOR")
def create_meeting_pattern(offering_id: int):
    instructor_id = int(get_jwt_identity())
    if not _ensure_instructor_owns_offering(instructor_id, offering_id):
        return error_response("FORBIDDEN", "Bu ders/şube size ait değil.", 403)

    data = request.get_json(silent=True) or {}
    weekday = data.get("weekday", None)
    starts_time = _parse_hhmm(str(data.get("starts_time", "")))
    ends_time = _parse_hhmm(str(data.get("ends_time", "")))

    try:
        weekday = int(weekday)
    except Exception:
        weekday = None

    if weekday is None or weekday < 0 or weekday > 6:
        return error_response("VALIDATION_ERROR", {"weekday": ["0-6 arası olmalı (Pzt=0 ... Paz=6)."]}, 400)
    if not starts_time or not ends_time:
        return error_response("VALIDATION_ERROR", {"time": ["starts_time/ends_time HH:MM formatında olmalı."]}, 400)
    if starts_time >= ends_time:
        return error_response("VALIDATION_ERROR", {"time": ["starts_time < ends_time olmalı."]}, 400)

    p = MeetingPattern(offering_id=offering_id, weekday=weekday, starts_time=starts_time, ends_time=ends_time)
    db.session.add(p)
    db.session.commit()

    created = generate_sessions_for_offering(offering_id, tz_name=str(current_app.config.get("TIMEZONE", "Europe/Istanbul")))
    db.session.commit()

    return jsonify({"ok": True, "pattern_id": p.id, "sessions_created": created})


@bp.delete("/meeting-patterns/<int:pattern_id>")
@require_roles("INSTRUCTOR")
def delete_meeting_pattern(pattern_id: int):
    instructor_id = int(get_jwt_identity())
    p = db.session.get(MeetingPattern, pattern_id)
    if not p:
        return error_response("NOT_FOUND", "Kayıt bulunamadı.", 404)
    if not _ensure_instructor_owns_offering(instructor_id, int(p.offering_id)):
        return error_response("FORBIDDEN", "Bu kayıt size ait değil.", 403)

    db.session.delete(p)
    db.session.commit()
    return jsonify({"ok": True})


@bp.post("/offerings/<int:offering_id>/generate-sessions")
@require_roles("INSTRUCTOR")
def generate_sessions(offering_id: int):
    instructor_id = int(get_jwt_identity())
    if not _ensure_instructor_owns_offering(instructor_id, offering_id):
        return error_response("FORBIDDEN", "Bu ders/şube size ait değil.", 403)

    created = generate_sessions_for_offering(offering_id, tz_name=str(current_app.config.get("TIMEZONE", "Europe/Istanbul")))
    db.session.commit()
    return jsonify({"ok": True, "created": created})


@bp.get("/offerings/<int:offering_id>/sessions")
@require_roles("INSTRUCTOR")
def list_sessions(offering_id: int):
    instructor_id = int(get_jwt_identity())
    if not _ensure_instructor_owns_offering(instructor_id, offering_id):
        return error_response("FORBIDDEN", "Bu ders/şube size ait değil.", 403)

    q_from = request.args.get("from")
    q_to = request.args.get("to")

    tz = ZoneInfo(str(current_app.config.get("TIMEZONE", "Europe/Istanbul")))
    now = datetime.now(tz).replace(tzinfo=None)
    default_from = now - timedelta(days=7)
    default_to = now + timedelta(days=60)

    def _parse_dt(s: Optional[str]) -> Optional[datetime]:
        if not s:
            return None
        try:
            if len(s) == 10 and s[4] == "-" and s[7] == "-":
                return datetime.fromisoformat(s + "T00:00:00")
            return datetime.fromisoformat(s)
        except Exception:
            return None

    dt_from = _parse_dt(q_from) or default_from
    dt_to = _parse_dt(q_to) or default_to

    sess = db.session.execute(
        db.select(ClassSession)
        .where(ClassSession.offering_id == offering_id, ClassSession.starts_at >= dt_from, ClassSession.starts_at <= dt_to)
        .order_by(ClassSession.starts_at.asc())
    ).scalars().all()

    items: List[Dict[str, Any]] = []
    for s in sess:
        count = db.session.execute(
            db.select(db.func.count(Attendance.id)).where(Attendance.session_id == s.id)
        ).scalar_one()
        items.append(
            {
                "id": s.id,
                "starts_at": s.starts_at.isoformat(),
                "ends_at": s.ends_at.isoformat(),
                "is_open": s.is_open,
                "attendance_count": int(count),
            }
        )

    return jsonify({"items": items, "range": {"from": dt_from.isoformat(), "to": dt_to.isoformat()}})


@bp.get("/sessions/<int:session_id>")
@require_roles("INSTRUCTOR")
def session_detail(session_id: int):
    instructor_id = int(get_jwt_identity())
    session = db.session.get(ClassSession, session_id)
    if not session:
        return error_response("NOT_FOUND", "Session bulunamadı.", 404)
    if not _ensure_instructor_owns_session(instructor_id, session):
        return error_response("FORBIDDEN", "Bu session size ait değil.", 403)

    offering = db.session.get(CourseOffering, session.offering_id)
    att_q = (
        db.select(Attendance, User)
        .join(User, User.id == Attendance.student_id)
        .where(Attendance.session_id == session.id)
        .order_by(User.full_name.asc(), User.email.asc())
    )
    rows = db.session.execute(att_q).all()
    attendance = [
        {
            "attendance_id": a.id,
            "student_id": u.id,
            "student_name": u.full_name,
            "student_email": u.email,
            "status": a.status,
            "scanned_at": a.scanned_at.isoformat() if a.scanned_at else None,
        }
        for a, u in rows
    ]

    payload = {
        "id": session.id,
        "offering_id": session.offering_id,
        "starts_at": session.starts_at,
        "ends_at": session.ends_at,
        "is_open": session.is_open,
        "course_code": offering.course.code if offering and offering.course else "",
        "course_title": offering.course.title if offering and offering.course else "",
        "term_code": offering.term.code if offering and offering.term else "",
        "section": offering.section if offering else "",
        "attendance": attendance,
    }
    return jsonify({"session": InstructorSessionDetailSchema().dump(payload)})


@bp.post("/sessions/<int:session_id>/open")
@require_roles("INSTRUCTOR")
def session_open(session_id: int):
    instructor_id = int(get_jwt_identity())
    session = db.session.get(ClassSession, session_id)
    if not session:
        return error_response("NOT_FOUND", "Session bulunamadı.", 404)
    if not _ensure_instructor_owns_session(instructor_id, session):
        return error_response("FORBIDDEN", "Bu session size ait değil.", 403)

    session.is_open = True
    db.session.commit()
    return jsonify({"ok": True, "session_id": session.id, "is_open": session.is_open})


@bp.post("/sessions/<int:session_id>/close")
@require_roles("INSTRUCTOR")
def session_close(session_id: int):
    instructor_id = int(get_jwt_identity())
    session = db.session.get(ClassSession, session_id)
    if not session:
        return error_response("NOT_FOUND", "Session bulunamadı.", 404)
    if not _ensure_instructor_owns_session(instructor_id, session):
        return error_response("FORBIDDEN", "Bu session size ait değil.", 403)

    session.is_open = False
    db.session.commit()
    return jsonify({"ok": True, "session_id": session.id, "is_open": session.is_open})


@bp.get("/sessions/<int:session_id>/qr")
@require_roles("INSTRUCTOR")
def session_qr(session_id: int):
    instructor_id = int(get_jwt_identity())
    session = db.session.get(ClassSession, session_id)
    if not session:
        return error_response("NOT_FOUND", "Session bulunamadı.", 404)
    if not _ensure_instructor_owns_session(instructor_id, session):
        return error_response("FORBIDDEN", "Bu session size ait değil.", 403)
    if not session.is_open:
        return error_response("SESSION_CLOSED", "Yoklama kapalı. Önce session'ı açın.", 400)

    ttl = int(current_app.config["QR_TOKEN_TTL_SECONDS"])
    print("QR CANM", current_app.config["QR_SECRET"])
    token = create_qr_token(
        current_app.config["QR_SECRET"],
        {
            "sid": session.id,
            "issued_by": instructor_id,
            "iat": int(datetime.now(tz=timezone.utc).timestamp()),
        },
    )

    scan_base = current_app.config["FRONTEND_SCAN_BASE_URL"]
    scan_url = f"{scan_base}?token={token}"

    png = make_qr_png_bytes(scan_url)
    data_url = png_bytes_to_data_url(png)

    payload = {
        "token": token,
        "expires_in": ttl,
        "scan_url": scan_url,
        "image_data_url": data_url,
    }
    return jsonify({"qr": QRResponseSchema().dump(payload)})


# ─────────────────────────────────────────────────────────────────────────────
# DUYURU (Announcement) ENDPOINTLERİ
# ─────────────────────────────────────────────────────────────────────────────

@bp.get("/offerings/<int:offering_id>/announcements")
@require_roles("INSTRUCTOR")
def list_announcements(offering_id: int):
    """Derse ait tüm duyuruları listele"""
    instructor_id = int(get_jwt_identity())
    if not _ensure_instructor_owns_offering(instructor_id, offering_id):
        return error_response("FORBIDDEN", "Bu ders/şube size ait değil.", 403)

    announcements = db.session.execute(
        db.select(Announcement)
        .where(Announcement.offering_id == offering_id)
        .order_by(Announcement.created_at.desc())
    ).scalars().all()

    items = [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "created_at": a.created_at.isoformat(),
            "is_active": a.is_active,
        }
        for a in announcements
    ]
    return jsonify({"items": items})


@bp.post("/offerings/<int:offering_id>/announcements")
@require_roles("INSTRUCTOR")
def create_announcement(offering_id: int):
    """Yeni duyuru oluştur"""
    instructor_id = int(get_jwt_identity())
    if not _ensure_instructor_owns_offering(instructor_id, offering_id):
        return error_response("FORBIDDEN", "Bu ders/şube size ait değil.", 403)

    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    content = (data.get("content") or "").strip()

    if not title:
        return error_response("VALIDATION_ERROR", {"title": ["Başlık gerekli."]}, 400)

    announcement = Announcement(
        offering_id=offering_id,
        instructor_id=instructor_id,
        title=title,
        content=content,
    )
    db.session.add(announcement)
    db.session.commit()

    return jsonify({
        "ok": True,
        "announcement": {
            "id": announcement.id,
            "title": announcement.title,
            "content": announcement.content,
            "created_at": announcement.created_at.isoformat(),
        }
    })


@bp.delete("/announcements/<int:announcement_id>")
@require_roles("INSTRUCTOR")
def delete_announcement(announcement_id: int):
    """Duyuruyu sil"""
    instructor_id = int(get_jwt_identity())
    announcement = db.session.get(Announcement, announcement_id)

    if not announcement:
        return error_response("NOT_FOUND", "Duyuru bulunamadı.", 404)
    if not _ensure_instructor_owns_offering(instructor_id, int(announcement.offering_id)):
        return error_response("FORBIDDEN", "Bu duyuru size ait değil.", 403)

    db.session.delete(announcement)
    db.session.commit()
    return jsonify({"ok": True})


@bp.get("/announcements")
@require_roles("INSTRUCTOR")
def my_announcements():
    """Öğretim görevlisinin tüm derslerindeki duyuruları getir"""
    instructor_id = int(get_jwt_identity())

    # Öğretim görevlisinin derslerinin ID'lerini bul
    offering_ids = db.session.execute(
        db.select(OfferingInstructor.offering_id).where(
            OfferingInstructor.instructor_id == instructor_id
        )
    ).scalars().all()

    if not offering_ids:
        return jsonify({"items": []})

    # Bu derslerin duyurularını getir
    announcements = db.session.execute(
        db.select(Announcement, CourseOffering)
        .join(CourseOffering, CourseOffering.id == Announcement.offering_id)
        .where(Announcement.offering_id.in_(offering_ids))
        .order_by(Announcement.created_at.desc())
        .limit(50)
    ).all()

    items = [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "created_at": a.created_at.isoformat(),
            "is_active": a.is_active,
            "course_code": o.course.code if o.course else "",
            "course_title": o.course.title if o.course else "",
        }
        for a, o in announcements
    ]
    return jsonify({"items": items})

