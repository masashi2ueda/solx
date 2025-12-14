"""Pytest configuration and shared fixtures for solx tests."""
from unittest.mock import MagicMock

import pytest
import solid

from solx.core import SolxObject, Vector3D
from solx.primitives.types import CenterType


@pytest.fixture
def sample_vector3d():
    """Fixture providing a sample Vector3D object."""
    return (1, 2, 3)


@pytest.fixture
def sample_openscad_object():
    """Fixture providing a sample OpenSCAD object."""
    return solid.cube([10, 10, 10])


@pytest.fixture
def sample_solx_object(sample_openscad_object):
    """Fixture providing a sample SolxObject."""
    return SolxObject(sample_openscad_object)


@pytest.fixture
def mock_renderer():
    """Fixture providing a mocked renderer for testing."""
    mock = MagicMock()
    mock.render.return_value = None
    return mock


@pytest.fixture(params=[
    CenterType.BOTTOM_CENTER,
    CenterType.CENTER,
    CenterType.BOTTOM_LEFT,
])
def center_type(request):
    """Fixture providing different center types for parametrized tests."""
    return request.param


@pytest.fixture(params=[
    (1, 1, 1),
    (5, 10, 15),
    (0.5, 2.5, 7.5),
])
def size_vector(request):
    """Fixture providing different size vectors for parametrized tests."""
    return request.param


@pytest.fixture(params=[
    Vector3D(0, 0, 0),
    Vector3D(10, 20, 30),
    Vector3D(-5, -10, 5),
])
def position_vector(request):
    """Fixture providing different position vectors for parametrized tests."""
    return request.param


@pytest.fixture
def cleanup_files():
    """Fixture for cleaning up generated files after tests."""
    created_files = []
    
    def add_file(filepath):
        created_files.append(filepath)
    
    yield add_file
    
    # Cleanup after test
    import os
    for filepath in created_files:
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except OSError:
            pass  # Ignore cleanup errors


# Test markers
def pytest_configure(config):
    """Configure pytest markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )
    config.addinivalue_line(
        "markers", "rendering: marks tests that require OpenSCAD rendering"
    )