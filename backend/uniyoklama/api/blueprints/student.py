from __future__ import annotations

from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity

from ..rbac import require_roles
from ..responses import error_response
from ...extensions import db
from ...models import Attendance, AttendanceStatus, ClassSession, Enrollment, Announcement, CourseOffering
from ...schemas import ScanAttendanceSchema, AttendanceSchema
from ...utils.qr import decode_qr_token, QRTokenError
from ...utils.geofence import check_geofence

bp = Blueprint("student", __name__, url_prefix="/student")


@bp.post("/attendance/scan")
@require_roles("STUDENT")
def scan_attendance():
    uid = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    errors = ScanAttendanceSchema().validate(data)
    if errors:
        return error_response("VALIDATION_ERROR", errors, 400)

    token = data["token"]
    try:
        print("QR GARDAŞ", current_app.config["QR_SECRET"])
        payload = decode_qr_token(
            secret=current_app.config["QR_SECRET"],
            token=token,
            max_age_seconds=int(current_app.config["QR_TOKEN_TTL_SECONDS"]) or 120,
        )
    except QRTokenError as e:
        return error_response("QR_TOKEN_ERROR", str(e), 400)

    sid = payload.get("sid")
    if not isinstance(sid, int):
        try:
            sid = int(sid)
        except Exception:
            return error_response("QR_TOKEN_ERROR", "QR içeriği hatalı.", 400)

    session = db.session.get(ClassSession, sid)
    if not session:
        return error_response("NOT_FOUND", "Session bulunamadı.", 404)

    if not session.is_open:
        return error_response("SESSION_CLOSED", "Yoklama kapalı.", 400)

    tz = ZoneInfo(str(current_app.config.get("TIMEZONE", "Europe/Istanbul")))
    now = datetime.now(tz).replace(tzinfo=None)
    starts = session.starts_at
    ends = session.ends_at
    if now < starts - timedelta(minutes=30) or now > ends + timedelta(minutes=30):
        return error_response("OUTSIDE_TIME_WINDOW", "Bu QR bu ders zamanı içerisinde değil.", 400)

    enr = db.session.execute(
        db.select(Enrollment).where(
            Enrollment.offering_id == session.offering_id,
            Enrollment.student_id == uid,
        )
    ).scalar_one_or_none()
    if not enr:
        return error_response("NOT_ENROLLED", "Bu derse kayıtlı değilsiniz.", 403)

    lat = float(data["lat"])
    lng = float(data["lng"])
    accuracy_m = data.get("accuracy_m", None)
    if accuracy_m is not None:
        try:
            accuracy_m = float(accuracy_m)
        except Exception:
            accuracy_m = None

    geo_res = check_geofence(
        lat=lat,
        lng=lng,
        circles=current_app.config["CAMPUS_CIRCLES"],
        accuracy_m=accuracy_m,
        max_accuracy_m=float(current_app.config["MAX_ACCURACY_M"]),
    )
    if not geo_res.allowed:
        return error_response("GEOFENCE_DENIED", geo_res.reason, 403)

    att = db.session.execute(
        db.select(Attendance).where(
            Attendance.session_id == session.id,
            Attendance.student_id == uid,
        )
    ).scalar_one_or_none()

    if att is None:
        att = Attendance(
            session_id=session.id,
            student_id=uid,
            status=AttendanceStatus.PRESENT.value,
            scanned_at=datetime.utcnow(),
        )
        db.session.add(att)
    else:
        att.status = AttendanceStatus.PRESENT.value
        att.scanned_at = datetime.utcnow()

    db.session.commit()

    return jsonify({"ok": True, "attendance": AttendanceSchema().dump(
        {
            "id": att.id,
            "session_id": att.session_id,
            "student_id": att.student_id,
            "status": att.status,
            "scanned_at": att.scanned_at,
        }
    )})


@bp.get("/attendance/history")
@require_roles("STUDENT")
def history():
    uid = int(get_jwt_identity())
    rows = db.session.execute(
        db.select(Attendance)
        .where(Attendance.student_id == uid)
        .order_by(Attendance.created_at.desc())
        .limit(100)
    ).scalars().all()

    data = [
        {
            "id": a.id,
            "session_id": a.session_id,
            "student_id": a.student_id,
            "status": a.status,
            "scanned_at": a.scanned_at.isoformat() if a.scanned_at else None,
        }
        for a in rows
    ]
    return jsonify({"items": data})


@bp.get("/announcements")
@require_roles("STUDENT")
def student_announcements():
    """Öğrencinin kayıtlı olduğu derslerin duyurularını getir"""
    uid = int(get_jwt_identity())

    # Öğrencinin kayıtlı olduğu dersleri bul
    enrolled_offering_ids = db.session.execute(
        db.select(Enrollment.offering_id).where(Enrollment.student_id == uid)
    ).scalars().all()

    if not enrolled_offering_ids:
        return jsonify({"items": []})

    # Bu derslerin aktif duyurularını getir
    announcements = db.session.execute(
        db.select(Announcement, CourseOffering)
        .join(CourseOffering, CourseOffering.id == Announcement.offering_id)
        .where(
            Announcement.offering_id.in_(enrolled_offering_ids),
            Announcement.is_active == True
        )
        .order_by(Announcement.created_at.desc())
        .limit(20)
    ).all()

    items = [
        {
            "id": a.id,
            "title": a.title,
            "content": a.content,
            "created_at": a.created_at.isoformat(),
            "course_code": o.course.code if o.course else "",
            "course_title": o.course.title if o.course else "",
        }
        for a, o in announcements
    ]
    return jsonify({"items": items})
