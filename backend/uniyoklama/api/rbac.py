from __future__ import annotations

from functools import wraps
from typing import Callable, Iterable, Set

from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

from .responses import error_response


def require_roles(*roles: str) -> Callable:
    allowed: Set[str] = set(roles)

    def decorator(fn: Callable) -> Callable:
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            role = claims.get("role")
            if role not in allowed:
                return error_response("FORBIDDEN", f"Bu işlem için yetkiniz yok. (role={role})", 403)
            return fn(*args, **kwargs)

        return wrapper

    return decorator
