from __future__ import annotations

from datetime import datetime, timedelta

from flask import Flask, current_app
from werkzeug.security import generate_password_hash

from .extensions import db
from .models import (
    User,
    Role,
    Term,
    Course,
    CourseOffering,
    OfferingInstructor,
    Enrollment,
    MeetingPattern,
    ClassSession,
)
from .utils.schedule import generate_sessions_for_offering


def register_commands(app: Flask) -> None:
    @app.cli.command("init-db")
    def init_db():

        db.create_all()
        print("DB tables created.")

    @app.cli.command("seed")
    def seed():


        instructor = db.session.execute(db.select(User).where(User.email == "instructor@demo.com")).scalar_one_or_none()
        if not instructor:
            instructor = User(
                email="instructor@demo.com",
                full_name="Demo Instructor",
                password_hash=generate_password_hash("demo1234"),
                role=Role.INSTRUCTOR.value,
            )
            db.session.add(instructor)

        student = db.session.execute(db.select(User).where(User.email == "student@demo.com")).scalar_one_or_none()
        if not student:
            student = User(
                email="student@demo.com",
                full_name="Demo Student",
                password_hash=generate_password_hash("demo1234"),
                role=Role.STUDENT.value,
            )
            db.session.add(student)


        term = db.session.execute(db.select(Term).where(Term.code == "2025-FALL")).scalar_one_or_none()
        if not term:
            term = Term(
                code="2025-FALL",
                starts_on=datetime.utcnow() - timedelta(days=14),
                ends_on=datetime.utcnow() + timedelta(days=90),
            )
            db.session.add(term)


        course = db.session.execute(db.select(Course).where(Course.code == "CSE101")).scalar_one_or_none()
        if not course:
            course = Course(code="CSE101", title="MVC Tabanlı Web Mimarisi")
            db.session.add(course)

        db.session.flush()


        offering = db.session.execute(
            db.select(CourseOffering).where(
                CourseOffering.course_id == course.id,
                CourseOffering.term_id == term.id,
                CourseOffering.section == "1",
            )
        ).scalar_one_or_none()
        if not offering:
            offering = CourseOffering(course_id=course.id, term_id=term.id, section="1", capacity=60)
            db.session.add(offering)

        db.session.flush()


        oi = db.session.execute(
            db.select(OfferingInstructor).where(
                OfferingInstructor.offering_id == offering.id,
                OfferingInstructor.instructor_id == instructor.id,
            )
        ).scalar_one_or_none()
        if not oi:
            db.session.add(OfferingInstructor(offering_id=offering.id, instructor_id=instructor.id, is_primary=True))


        enr = db.session.execute(
            db.select(Enrollment).where(
                Enrollment.offering_id == offering.id,
                Enrollment.student_id == student.id,
            )
        ).scalar_one_or_none()
        if not enr:
            db.session.add(Enrollment(offering_id=offering.id, student_id=student.id))

        db.session.flush()

        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        weekday = now.weekday()
        starts_t = now.time()
        ends_t = (now + timedelta(hours=1)).time()

        existing_mp = db.session.execute(
            db.select(MeetingPattern).where(
                MeetingPattern.offering_id == offering.id,
                MeetingPattern.weekday == weekday,
                MeetingPattern.starts_time == starts_t,
                MeetingPattern.ends_time == ends_t,
            )
        ).scalar_one_or_none()

        if not existing_mp:
            db.session.add(MeetingPattern(offering_id=offering.id, weekday=weekday, starts_time=starts_t, ends_time=ends_t))

        db.session.commit()

        tz_name = str(current_app.config.get("TIMEZONE", "Europe/Istanbul"))
        created = generate_sessions_for_offering(offering.id, tz_name=tz_name)
        db.session.commit()

        today_session = db.session.execute(
            db.select(ClassSession).where(
                ClassSession.offering_id == offering.id,
                ClassSession.starts_at == now,
            )
        ).scalar_one_or_none()
        if today_session:
            today_session.is_open = True
            db.session.commit()

        print("Seed complete.")
        print("Instructor: instructor@demo.com / demo1234 | Student: student@demo.com / demo1234")
        print(f"Offering ID: {offering.id}")
        print(f"Sessions created: {created}")
        if today_session:
            print(f"Today's Session ID: {today_session.id} (is_open={today_session.is_open})")
        else:
            print("Today's Session not found (check meeting pattern).")

    @app.cli.command("generate-sessions")
    def generate_sessions_cmd():
        from .models import MeetingPattern as MP

        tz_name = str(current_app.config.get("TIMEZONE", "Europe/Istanbul"))

        offering_ids = db.session.execute(db.select(MP.offering_id).distinct()).scalars().all()
        total = 0
        for oid in offering_ids:
            total += generate_sessions_for_offering(int(oid), tz_name=tz_name)
        db.session.commit()
        print(f"Generated {total} sessions across {len(offering_ids)} offerings.")
