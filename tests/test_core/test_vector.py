"""Tests for solx.core.vector module."""
import pytest

from solx.core.vector import Vector3D, normalize_vector3d


class TestVector3D:
    """Test cases for Vector3D class."""

    def test_init_with_three_values(self):
        """Test Vector3D initialization with x, y, z values."""
        v = Vector3D(1, 2, 3)
        assert v.x == 1
        assert v.y == 2
        assert v.z == 3

    def test_init_with_single_value(self):
        """Test Vector3D initialization with single value (uniform)."""
        v = Vector3D(5)
        assert v.x == 5
        assert v.y == 5
        assert v.z == 5

    def test_from_tuple(self):
        """Test Vector3D creation from tuple."""
        v = Vector3D.from_tuple((1, 2, 3))
        assert v.x == 1
        assert v.y == 2
        assert v.z == 3

    def test_from_list(self):
        """Test Vector3D creation from list."""
        v = Vector3D.from_list([1, 2, 3])
        assert v.x == 1
        assert v.y == 2
        assert v.z == 3

    def test_to_tuple(self):
        """Test Vector3D conversion to tuple."""
        v = Vector3D(1, 2, 3)
        assert v.to_tuple() == (1, 2, 3)

    def test_to_list(self):
        """Test Vector3D conversion to list."""
        v = Vector3D(1, 2, 3)
        assert v.to_list() == [1, 2, 3]

    def test_addition(self):
        """Test Vector3D addition."""
        v1 = Vector3D(1, 2, 3)
        v2 = Vector3D(4, 5, 6)
        result = v1 + v2
        assert result.x == 5
        assert result.y == 7
        assert result.z == 9

    def test_subtraction(self):
        """Test Vector3D subtraction."""
        v1 = Vector3D(4, 5, 6)
        v2 = Vector3D(1, 2, 3)
        result = v1 - v2
        assert result.x == 3
        assert result.y == 3
        assert result.z == 3

    def test_multiplication_scalar(self):
        """Test Vector3D multiplication by scalar."""
        v = Vector3D(1, 2, 3)
        result = v * 2
        assert result.x == 2
        assert result.y == 4
        assert result.z == 6

    def test_division_scalar(self):
        """Test Vector3D division by scalar."""
        v = Vector3D(2, 4, 6)
        result = v / 2
        assert result.x == 1
        assert result.y == 2
        assert result.z == 3

    def test_equality(self):
        """Test Vector3D equality comparison."""
        v1 = Vector3D(1, 2, 3)
        v2 = Vector3D(1, 2, 3)
        v3 = Vector3D(1, 2, 4)
        assert v1 == v2
        assert v1 != v3

    def test_length(self):
        """Test Vector3D length calculation."""
        v = Vector3D(3, 4, 0)
        assert v.length() == 5.0

    def test_normalize(self):
        """Test Vector3D normalization."""
        v = Vector3D(3, 4, 0)
        normalized = v.normalize()
        assert abs(normalized.length() - 1.0) < 1e-10

    def test_dot_product(self):
        """Test Vector3D dot product."""
        v1 = Vector3D(1, 2, 3)
        v2 = Vector3D(4, 5, 6)
        result = v1.dot(v2)
        assert result == 32  # 1*4 + 2*5 + 3*6 = 4 + 10 + 18 = 32

    def test_cross_product(self):
        """Test Vector3D cross product."""
        v1 = Vector3D(1, 0, 0)
        v2 = Vector3D(0, 1, 0)
        result = v1.cross(v2)
        assert result.x == 0
        assert result.y == 0
        assert result.z == 1

    def test_repr(self):
        """Test Vector3D string representation."""
        v = Vector3D(1, 2, 3)
        assert repr(v) == "Vector3D(1, 2, 3)"


class TestNormalizeVector3D:
    """Test cases for normalize_vector3d function."""

    def test_normalize_vector3d_object(self):
        """Test normalization of Vector3D object."""
        v = Vector3D(3, 4, 0)
        normalized = normalize_vector3d(v)
        assert isinstance(normalized, Vector3D)
        assert abs(normalized.length() - 1.0) < 1e-10

    def test_normalize_tuple(self):
        """Test normalization of tuple."""
        result = normalize_vector3d((3, 4, 0))
        assert isinstance(result, Vector3D)
        assert abs(result.length() - 1.0) < 1e-10

    def test_normalize_list(self):
        """Test normalization of list."""
        result = normalize_vector3d([3, 4, 0])
        assert isinstance(result, Vector3D)
        assert abs(result.length() - 1.0) < 1e-10

    def test_normalize_zero_vector(self):
        """Test normalization of zero vector."""
        with pytest.raises(ValueError):
            normalize_vector3d((0, 0, 0))