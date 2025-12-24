from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple


Circle = Tuple[float, float, float]  # (lat, lng, radius_m)


@dataclass(frozen=True)
class AppConfig:
    debug: bool
    host: str
    port: int
    cors_origins: List[str]
    timezone: str

    db_url: str

    jwt_secret: str
    access_token_expires_minutes: int

    qr_secret: str
    qr_token_ttl_seconds: int

    campus_circles: List[Circle]
    max_accuracy_m: float


def _parse_bool(value: str, default: bool = False) -> bool:
    v = (value or "").strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _parse_campus_circles(raw: str) -> List[Circle]:
    circles: List[Circle] = []
    raw = (raw or "").strip()
    if not raw:
        return circles

    parts = [p.strip() for p in raw.split("|") if p.strip()]
    for p in parts:
        nums = [x.strip() for x in p.split(",")]
        if len(nums) != 3:
            raise ValueError(f"Invalid circle format: '{p}'. Expected lat,lng,radius_m")
        lat, lng, r = float(nums[0]), float(nums[1]), float(nums[2])
        circles.append((lat, lng, r))
    return circles


def load_config(cfg_path: str) -> AppConfig:
    path = Path(cfg_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Config file not found: {cfg_path}. "
            f"Create it by copying backend/config.example.cfg -> backend/config.cfg"
        )

    parser = configparser.ConfigParser()
    parser.read(path, encoding="utf-8")

    app = parser["app"]
    db = parser["db"]
    sec = parser["security"]
    geo = parser["geofence"]

    cors_origins = [o.strip() for o in app.get("cors_origins", "").split(",") if o.strip()]

    cfg = AppConfig(
        debug=_parse_bool(app.get("debug", "false"), False),
        host=app.get("host", "127.0.0.1"),
        port=int(app.get("port", "5000")),
        cors_origins=["http://localhost:5173", "https://uniyoklama.vercel.app"],
        timezone=app.get("timezone", "Europe/Istanbul"),

        db_url=db.get("url"),

        jwt_secret=sec.get("jwt_secret"),
        access_token_expires_minutes=int(sec.get("access_token_expires_minutes", "180")),

        qr_secret=sec.get("qr_secret"),
        qr_token_ttl_seconds=int(sec.get("qr_token_ttl_seconds", "120")),

        campus_circles=_parse_campus_circles(geo.get("campus_circles", "")),
        max_accuracy_m=float(geo.get("max_accuracy_m", "150")),
    )

    if not cfg.db_url:
        raise ValueError("[db] url is required")
    if cfg.qr_token_ttl_seconds < 15:
        raise ValueError("qr_token_ttl_seconds is too low; use >= 15 seconds")
    if not cfg.campus_circles:
        raise ValueError("[geofence] campus_circles must contain at least one circle")

    return cfg
