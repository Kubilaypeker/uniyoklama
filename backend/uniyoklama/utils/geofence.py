from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Tuple, Optional


Circle = Tuple[float, float, float]  # (lat, lng, radius_m)


@dataclass(frozen=True)
class GeofenceResult:
    allowed: bool
    reason: str
    matched_circle: Optional[Circle] = None
    distance_m: Optional[float] = None


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def check_geofence(
    lat: float,
    lng: float,
    circles: Iterable[Circle],
    accuracy_m: Optional[float] = None,
    max_accuracy_m: float = 150.0,
) -> GeofenceResult:
    if accuracy_m is not None and accuracy_m > max_accuracy_m:
        return GeofenceResult(
            allowed=False,
            reason=f"Konum doğruluğu yetersiz (accuracy={accuracy_m:.0f}m > {max_accuracy_m:.0f}m).",
        )

    best: Optional[GeofenceResult] = None
    for c in circles:
        c_lat, c_lng, radius_m = c
        d = haversine_m(lat, lng, c_lat, c_lng)
        allowed = d <= radius_m
        if allowed:
            return GeofenceResult(
                allowed=True,
                reason="OK",
                matched_circle=c,
                distance_m=d,
            )
        if best is None or (best.distance_m is not None and d < best.distance_m):
            best = GeofenceResult(
                allowed=False,
                reason="Kampüs alanı dışında.",
                matched_circle=c,
                distance_m=d,
            )

    return best or GeofenceResult(allowed=False, reason="Geofence tanımı yok.")
