from __future__ import annotations

from flask import Blueprint

from .blueprints.auth import bp as auth_bp
from .blueprints.instructor import bp as instructor_bp
from .blueprints.student import bp as student_bp


def register_api(app) -> None:
    api = Blueprint("api", __name__, url_prefix="/api")

    api.register_blueprint(auth_bp)
    api.register_blueprint(instructor_bp)
    api.register_blueprint(student_bp)

    app.register_blueprint(api)
