from __future__ import annotations

import base64
from io import BytesIO
from typing import Any, Dict
from urllib.parse import urlparse, parse_qs

import qrcode
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


class QRTokenError(Exception):
    pass


def make_serializer(secret: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret, salt="uniyoklama-qr-v1")



def create_qr_token(secret: str, payload: Dict[str, Any]) -> str:
    s = make_serializer(secret)
    return s.dumps(payload)


def decode_qr_token(secret: str, token: str, max_age_seconds: int) -> Dict[str, Any]:
    s = make_serializer(secret)

    token = (token or "").strip()

    if "/scan?token=" in token or token.startswith("http://") or token.startswith("https://") or token.startswith("localhost:"):
        try:
            u = urlparse(token if token.startswith("http") else "http://" + token)
            extracted = (parse_qs(u.query).get("token", [""])[0] or "").strip()
            if extracted:
                token = extracted
        except Exception:
            pass

    token = token.replace(" ", "+")

    try:
        data = s.loads(token, max_age=max_age_seconds)
        if not isinstance(data, dict):
            raise QRTokenError("Invalid token payload")
        return data
    except SignatureExpired as e:
        raise QRTokenError("QR kodun süresi dolmuş. Lütfen yeni QR okutun.") from e
    except BadSignature as e:
        raise QRTokenError("QR kod geçersiz.") from e



def make_qr_png_bytes(text: str) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=3,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    bio = BytesIO()
    img.save(bio, format="PNG")
    return bio.getvalue()


def png_bytes_to_data_url(png_bytes: bytes) -> str:
    b64 = base64.b64encode(png_bytes).decode("ascii")
    return f"data:image/png;base64,{b64}"
