import time
import pytest

from uniyoklama.utils.qr import create_qr_token, decode_qr_token, QRTokenError


def test_qr_token_roundtrip():
    secret = "s3cr3t"
    token = create_qr_token(secret, {"sid": 123})
    data = decode_qr_token(secret, token, max_age_seconds=10)
    assert data["sid"] == 123


def test_qr_token_expired():
    secret = "s3cr3t"
    token = create_qr_token(secret, {"sid": 1})
    time.sleep(1)
    with pytest.raises(QRTokenError):
        decode_qr_token(secret, token, max_age_seconds=0)
