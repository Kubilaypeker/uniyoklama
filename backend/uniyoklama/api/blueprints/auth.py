from __future__ import annotations

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from werkzeug.security import check_password_hash

from ..responses import error_response
from ...extensions import db
from ...models import User
from ...schemas import LoginSchema, UserSchema

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    errors = LoginSchema().validate(data)
    if errors:
        return error_response("VALIDATION_ERROR", errors, 400)

    user = db.session.execute(db.select(User).where(User.email == data["email"])).scalar_one_or_none()
    if not user or not check_password_hash(user.password_hash, data["password"]):
        return error_response("INVALID_CREDENTIALS", "E-posta veya şifre hatalı.", 401)

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role, "email": user.email},
    )
    return jsonify(
        {
            "access_token": access_token,
            "user": UserSchema().dump(
                {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}
            ),
        }
    )


@bp.get("/me")
@jwt_required()
def me():
    uid = int(get_jwt_identity())
    user = db.session.get(User, uid)
    if not user:
        return error_response("NOT_FOUND", "Kullanıcı bulunamadı.", 404)

    return jsonify(
        {
            "user": UserSchema().dump(
                {"id": user.id, "email": user.email, "full_name": user.full_name, "role": user.role}
            )
        }
    )
