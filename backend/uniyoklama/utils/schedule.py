from __future__ import annotations

from datetime import datetime, timedelta, date

from ..extensions import db
from ..models import CourseOffering, ClassSession, MeetingPattern


def _daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def generate_sessions_for_offering(offering_id: int, tz_name: str = "Europe/Istanbul") -> int:
    """Generate ClassSession rows from MeetingPattern rows for an offering.

    Tasarım notu:
    - Session datetime'ları **naive** olarak kaydedilir ve uygulama TIMEZONE'una göre yorumlanır.
    - Böylece UI'da saatler "yerel saat" gibi görünür (öğrenci/öğretim elemanı için daha kullanıcı dostu).
    - Idempotent: aynı offering için aynı starts_at varsa atlar.
    """
    offering = db.session.get(CourseOffering, offering_id)
    if not offering or not offering.term:
        return 0

    term_start = offering.term.starts_on.date()
    term_end = offering.term.ends_on.date()

    patterns = db.session.execute(
        db.select(MeetingPattern).where(MeetingPattern.offering_id == offering_id)
    ).scalars().all()

    created = 0
    for p in patterns:
        for day in _daterange(term_start, term_end):
            if day.weekday() != int(p.weekday):
                continue

            start_local = datetime.combine(day, p.starts_time)
            end_local = datetime.combine(day, p.ends_time)

            exists = db.session.execute(
                db.select(ClassSession).where(
                    ClassSession.offering_id == offering_id,
                    ClassSession.starts_at == start_local,
                )
            ).scalar_one_or_none()
            if exists:
                continue

            db.session.add(
                ClassSession(
                    offering_id=offering_id,
                    starts_at=start_local,
                    ends_at=end_local,
                    is_open=False,
                )
            )
            created += 1

    return created


def generate_sessions_for_instructor_offerings(instructor_id: int, tz_name: str = "Europe/Istanbul") -> int:
    """Generate sessions for every offering the instructor is assigned to."""
    from ..models import OfferingInstructor

    offering_ids = db.session.execute(
        db.select(OfferingInstructor.offering_id).where(OfferingInstructor.instructor_id == instructor_id)
    ).scalars().all()

    total = 0
    for oid in offering_ids:
        total += generate_sessions_for_offering(int(oid), tz_name=tz_name)
    return total
