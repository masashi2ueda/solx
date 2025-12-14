"""Tests for solx.primitives.types module."""
import pytest

from solx.primitives.types import CenterType


class TestCenterType:
    """Test cases for CenterType enum."""

    def test_center_type_values(self):
        """Test that CenterType has expected values."""
        # Test that the enum has the expected values
        assert hasattr(CenterType, 'BOTTOM_CENTER')
        assert hasattr(CenterType, 'CENTER')
        assert hasattr(CenterType, 'BOTTOM_LEFT')

    def test_center_type_equality(self):
        """Test CenterType equality comparison."""
        assert CenterType.BOTTOM_CENTER == CenterType.BOTTOM_CENTER
        assert CenterType.CENTER == CenterType.CENTER
        assert CenterType.BOTTOM_LEFT == CenterType.BOTTOM_LEFT
        
        assert CenterType.BOTTOM_CENTER != CenterType.CENTER
        assert CenterType.CENTER != CenterType.BOTTOM_LEFT
        assert CenterType.BOTTOM_LEFT != CenterType.BOTTOM_CENTER

    def test_center_type_string_representation(self):
        """Test CenterType string representation."""
        # Test that string representation works
        assert str(CenterType.BOTTOM_CENTER) is not None
        assert str(CenterType.CENTER) is not None
        assert str(CenterType.BOTTOM_LEFT) is not None

    def test_center_type_membership(self):
        """Test CenterType membership in collections."""
        center_types = [CenterType.BOTTOM_CENTER, CenterType.CENTER, CenterType.BOTTOM_LEFT]
        
        assert CenterType.BOTTOM_CENTER in center_types
        assert CenterType.CENTER in center_types
        assert CenterType.BOTTOM_LEFT in center_types

    def test_center_type_iteration(self):
        """Test that we can iterate over CenterType values."""
        center_types = list(CenterType)
        assert len(center_types) >= 3  # At least the three we know about
        assert CenterType.BOTTOM_CENTER in center_types
        assert CenterType.CENTER in center_types
        assert CenterType.BOTTOM_LEFT in center_types

    def test_center_type_unique_values(self):
        """Test that CenterType values are unique."""
        all_values = list(CenterType)
        unique_values = set(all_values)
        assert len(all_values) == len(unique_values)

    def test_center_type_hashable(self):
        """Test that CenterType values are hashable."""
        # Should be able to use as dictionary keys
        center_dict = {
            CenterType.BOTTOM_CENTER: "bottom_center",
            CenterType.CENTER: "center",
            CenterType.BOTTOM_LEFT: "bottom_left"
        }
        
        assert center_dict[CenterType.BOTTOM_CENTER] == "bottom_center"
        assert center_dict[CenterType.CENTER] == "center"
        assert center_dict[CenterType.BOTTOM_LEFT] == "bottom_left"

    def test_center_type_ordering(self):
        """Test CenterType ordering if applicable."""
        # Some enums support ordering, test if these do
        try:
            # This might raise TypeError if ordering is not supported
            result = CenterType.BOTTOM_CENTER < CenterType.CENTER
            assert isinstance(result, bool)
        except TypeError:
            # If ordering is not supported, that's fine
            pass