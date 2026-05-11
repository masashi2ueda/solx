import pytest

from solx.primitives.cube import Cube
from solx.primitives.cylinder import Cylinder
from solx.primitives.types import CenterType


@pytest.mark.parametrize(
    ("center", "expected_center"),
    [
        (CenterType.BOTTOM_CENTER, (0.0, 0.0, 1.5)),
        (CenterType.CENTER, (0.0, 0.0, 0.0)),
        (CenterType.BOTTOM_LEFT, (1.0, 2.0, 1.5)),
    ],
)
def test_cube_center_and_size(center: CenterType, expected_center: tuple[float, float, float]) -> None:
    cube = Cube(size=(2.0, 4.0, 3.0), center=center)

    assert cube.size == pytest.approx((2.0, 4.0, 3.0))
    assert cube.center.to_tuple() == pytest.approx(expected_center)


def test_cube_param_apply_translates_all_points() -> None:
    cube = Cube(size=(2.0, 2.0, 2.0), center=CenterType.BOTTOM_CENTER)
    moved = cube.translate((10.0, -5.0, 3.0))

    assert moved.center.to_tuple() == pytest.approx((10.0, -5.0, 4.0))
    assert moved.pts[0].to_tuple() == pytest.approx((9.0, -6.0, 3.0))


def test_cylinder_centers_for_each_origin() -> None:
    c_bottom = Cylinder(radius=2.0, height=6.0, center=CenterType.BOTTOM_CENTER)
    assert c_bottom.bottom_center.to_tuple() == pytest.approx((0.0, 0.0, 0.0))
    assert c_bottom.top_center.to_tuple() == pytest.approx((0.0, 0.0, 6.0))

    c_center = Cylinder(radius=2.0, height=6.0, center=CenterType.CENTER)
    assert c_center.bottom_center.to_tuple() == pytest.approx((0.0, 0.0, -3.0))
    assert c_center.top_center.to_tuple() == pytest.approx((0.0, 0.0, 3.0))

    c_left = Cylinder(radius=2.0, height=6.0, center=CenterType.BOTTOM_LEFT)
    assert c_left.bottom_center.to_tuple() == pytest.approx((2.0, 2.0, 0.0))
    assert c_left.top_center.to_tuple() == pytest.approx((2.0, 2.0, 6.0))


def test_cylinder_invalid_center_raises() -> None:
    with pytest.raises(ValueError, match="Invalid CenterType"):
        Cylinder(radius=1.0, height=1.0, center="bad")  # type: ignore[arg-type]
