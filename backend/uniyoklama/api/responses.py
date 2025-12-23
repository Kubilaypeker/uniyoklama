from __future__ import annotations

from flask import jsonify


def error_response(error: str, details=None, status_code: int = 400):
    payload = {"error": error}
    if details is not None:
        payload["details"] = details
    return jsonify(payload), status_code
