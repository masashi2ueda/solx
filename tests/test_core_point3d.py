import pytest

from solx.core.base import Point3D, param_apply


def test_point3d_translate_rotate_scale_mirror() -> None:
    p = Point3D(1.0, 2.0, 3.0)

    moved = p.translate((2.0, -1.0, 4.0))
    assert moved.to_tuple() == pytest.approx((3.0, 1.0, 7.0))

    rotated = Point3D(1.0, 0.0, 0.0).rotate((0.0, 0.0, 90.0))
    assert rotated.to_tuple() == pytest.approx((0.0, 1.0, 0.0), abs=1e-9)

    scaled = p.scale((2.0, 3.0, 4.0))
    assert scaled.to_tuple() == pytest.approx((2.0, 6.0, 12.0))

    mirrored = p.mirror((1.0, 0.0, 1.0))
    assert mirrored.to_tuple() == pytest.approx((-1.0, 2.0, -3.0))


def test_point3d_distance_to() -> None:
    p1 = Point3D(0.0, 0.0, 0.0)
    p2 = Point3D(3.0, 4.0, 12.0)
    assert p1.distance_to(p2) == pytest.approx(13.0)


def test_param_apply_on_point_and_invalid_name() -> None:
    p = Point3D(1.0, 1.0, 1.0)
    moved = param_apply("translate", (1.0, 2.0, 3.0), p)
    assert isinstance(moved, Point3D)
    assert moved.to_tuple() == pytest.approx((2.0, 3.0, 4.0))

    with pytest.raises(ValueError, match="Unknown function name"):
        param_apply("unknown", (0.0, 0.0, 0.0), p)


def test_param_apply_rejects_unsupported_target_type() -> None:
    with pytest.raises(ValueError, match="Target must be OpenSCADObject or Point3D"):
        param_apply("translate", (1.0, 2.0, 3.0), object())
