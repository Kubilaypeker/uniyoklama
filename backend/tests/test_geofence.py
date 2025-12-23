from uniyoklama.utils.geofence import check_geofence


def test_geofence_allows_inside_circle():
    circles = [(41.0, 29.0, 1000)]  # 1km radius
    res = check_geofence(lat=41.0, lng=29.0, circles=circles, accuracy_m=20, max_accuracy_m=150)
    assert res.allowed is True


def test_geofence_denies_bad_accuracy():
    circles = [(41.0, 29.0, 1000)]
    res = check_geofence(lat=41.0, lng=29.0, circles=circles, accuracy_m=500, max_accuracy_m=150)
    assert res.allowed is False
    assert "accuracy" in res.reason.lower()
