from __future__ import annotations

from datetime import timedelta
from typing import Optional

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import HTTPException

from .config import load_config
from .extensions import db, migrate, jwt, cors
from .api import register_api
from .api.responses import error_response
from .commands import register_commands


def create_app(cfg_path: str = "config.cfg") -> Flask:
    cfg = load_config(cfg_path)

    app = Flask(__name__)

    app.config.update(
        DEBUG=cfg.debug,
        HOST=cfg.host,
        PORT=cfg.port,

        TIMEZONE=cfg.timezone,

        SQLALCHEMY_DATABASE_URI=cfg.db_url,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        JWT_SECRET_KEY=cfg.jwt_secret,
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=cfg.access_token_expires_minutes),

        QR_SECRET=cfg.qr_secret,
        QR_TOKEN_TTL_SECONDS=cfg.qr_token_ttl_seconds,

        CAMPUS_CIRCLES=cfg.campus_circles,
        MAX_ACCURACY_M=cfg.max_accuracy_m,

        FRONTEND_SCAN_BASE_URL=(cfg.cors_origins[0].rstrip("/") + "/scan"),
        CORS_ORIGINS=cfg.cors_origins,
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": cfg.cors_origins}})

    register_api(app)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        return error_response(e.name, e.description, e.code or 500)

    @app.errorhandler(Exception)
    def handle_unexpected(e: Exception):
        return error_response("INTERNAL_ERROR", str(e), 500)

    @app.get("/health")
    def health():
        return jsonify({"ok": True})

    register_commands(app)

    # Otomatik tablo oluşturma
    with app.app_context():
        db.create_all()

    return app
