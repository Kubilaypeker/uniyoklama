from __future__ import annotations

from marshmallow import Schema, fields, validate


class ErrorSchema(Schema):
    error = fields.String(required=True)
    details = fields.Raw(required=False)


class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=4))


class UserSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Email(required=True)
    full_name = fields.String(required=True)
    role = fields.String(required=True)


class SessionSchema(Schema):
    id = fields.Int(required=True)
    offering_id = fields.Int(required=True)
    starts_at = fields.DateTime(required=True)
    ends_at = fields.DateTime(required=True)
    is_open = fields.Bool(required=True)


class InstructorSessionDetailSchema(SessionSchema):
    course_code = fields.String(required=True)
    course_title = fields.String(required=True)
    term_code = fields.String(required=True)
    section = fields.String(required=True)
    attendance = fields.List(fields.Dict(), required=True)


class QRResponseSchema(Schema):
    token = fields.String(required=True)
    expires_in = fields.Int(required=True)
    scan_url = fields.String(required=True)
    image_data_url = fields.String(required=True)


class ScanAttendanceSchema(Schema):
    token = fields.String(required=True)
    lat = fields.Float(required=True)
    lng = fields.Float(required=True)
    accuracy_m = fields.Float(required=False, allow_none=True)


class AttendanceSchema(Schema):
    id = fields.Int(required=True)
    session_id = fields.Int(required=True)
    student_id = fields.Int(required=True)
    status = fields.String(required=True)
    scanned_at = fields.DateTime(allow_none=True)
