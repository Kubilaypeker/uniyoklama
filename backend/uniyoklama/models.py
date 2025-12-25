from __future__ import annotations

from datetime import datetime, time
from enum import Enum
from typing import Optional

from sqlalchemy import UniqueConstraint, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .extensions import db


class Role(str, Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"
    INSTRUCTOR = "INSTRUCTOR"
    STUDENT = "STUDENT"


class AttendanceStatus(str, Enum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LATE = "LATE"
    EXCUSED = "EXCUSED"


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    full_name: Mapped[str] = mapped_column(default="")
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default=Role.STUDENT.value)

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # relationships
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    instructor_offerings = relationship("OfferingInstructor", back_populates="instructor", cascade="all, delete-orphan")


class Term(db.Model):
    __tablename__ = "terms"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, index=True)  # e.g., 2025-FALL
    starts_on: Mapped[datetime]
    ends_on: Mapped[datetime]

    __table_args__ = (
        CheckConstraint("starts_on <= ends_on", name="ck_term_dates"),
    )


class Course(db.Model):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True, index=True)  # e.g., CSE101
    title: Mapped[str] = mapped_column(default="")


class CourseOffering(db.Model):
    __tablename__ = "course_offerings"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"))
    term_id: Mapped[int] = mapped_column(ForeignKey("terms.id", ondelete="CASCADE"))
    section: Mapped[str] = mapped_column(default="1")
    capacity: Mapped[Optional[int]] = mapped_column(nullable=True)

    course = relationship("Course")
    term = relationship("Term")

    enrollments = relationship("Enrollment", back_populates="offering", cascade="all, delete-orphan")
    instructors = relationship("OfferingInstructor", back_populates="offering", cascade="all, delete-orphan")
    meeting_patterns = relationship("MeetingPattern", back_populates="offering", cascade="all, delete-orphan")
    sessions = relationship("ClassSession", back_populates="offering", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("course_id", "term_id", "section", name="uq_offering_course_term_section"),
    )


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id: Mapped[int] = mapped_column(primary_key=True)
    offering_id: Mapped[int] = mapped_column(ForeignKey("course_offerings.id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    offering = relationship("CourseOffering", back_populates="enrollments")
    student = relationship("User", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("offering_id", "student_id", name="uq_enrollment_offering_student"),
    )


class OfferingInstructor(db.Model):
    __tablename__ = "offering_instructors"

    id: Mapped[int] = mapped_column(primary_key=True)
    offering_id: Mapped[int] = mapped_column(ForeignKey("course_offerings.id", ondelete="CASCADE"))
    instructor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    is_primary: Mapped[bool] = mapped_column(default=False)

    offering = relationship("CourseOffering", back_populates="instructors")
    instructor = relationship("User", back_populates="instructor_offerings")

    __table_args__ = (
        UniqueConstraint("offering_id", "instructor_id", name="uq_offering_instructor"),
    )


class MeetingPattern(db.Model):
    __tablename__ = "meeting_patterns"

    id: Mapped[int] = mapped_column(primary_key=True)
    offering_id: Mapped[int] = mapped_column(ForeignKey("course_offerings.id", ondelete="CASCADE"))

    weekday: Mapped[int] = mapped_column()
    starts_time: Mapped[time]
    ends_time: Mapped[time]

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    offering = relationship("CourseOffering", back_populates="meeting_patterns")

    __table_args__ = (
        CheckConstraint("weekday >= 0 AND weekday <= 6", name="ck_meeting_weekday"),
        CheckConstraint("starts_time < ends_time", name="ck_meeting_times"),
        UniqueConstraint("offering_id", "weekday", "starts_time", "ends_time", name="uq_meeting_pattern"),
    )


class ClassSession(db.Model):
    __tablename__ = "class_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    offering_id: Mapped[int] = mapped_column(ForeignKey("course_offerings.id", ondelete="CASCADE"))

    starts_at: Mapped[datetime]
    ends_at: Mapped[datetime]

    is_open: Mapped[bool] = mapped_column(default=False)  # Instructor yoklamayı açtı mı?
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    offering = relationship("CourseOffering", back_populates="sessions")
    attendance_records = relationship("Attendance", back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint("offering_id", "starts_at", name="uq_session_offering_starts"),
    )


class Attendance(db.Model):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("class_sessions.id", ondelete="CASCADE"))
    student_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[str] = mapped_column(default=AttendanceStatus.PRESENT.value)

    scanned_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    session = relationship("ClassSession", back_populates="attendance_records")
    student = relationship("User")

    __table_args__ = (
        UniqueConstraint("session_id", "student_id", name="uq_attendance_session_student"),
    )


class Announcement(db.Model):
    """Ders duyurusu - Hocaların öğrencilere duyuru yapabilmesi için"""
    __tablename__ = "announcements"

    id: Mapped[int] = mapped_column(primary_key=True)
    offering_id: Mapped[int] = mapped_column(ForeignKey("course_offerings.id", ondelete="CASCADE"))
    instructor_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))

    title: Mapped[str] = mapped_column(default="")
    content: Mapped[str] = mapped_column(default="")

    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(default=True)

    offering = relationship("CourseOffering")
    instructor = relationship("User")
