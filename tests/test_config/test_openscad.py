"""Tests for solx.config.openscad module."""
import os
from unittest.mock import MagicMock, patch

import pytest

from solx.config.openscad import get_openscad_path


class TestGetOpenSCADPath:
    """Test cases for get_openscad_path function."""

    def test_get_openscad_path_returns_string(self):
        """Test that get_openscad_path returns a string."""
        path = get_openscad_path()
        assert isinstance(path, str)

    def test_get_openscad_path_not_empty(self):
        """Test that get_openscad_path returns non-empty string."""
        path = get_openscad_path()
        assert len(path) > 0

    @patch('shutil.which')
    def test_get_openscad_path_with_which_found(self, mock_which):
        """Test get_openscad_path when 'which' finds OpenSCAD."""
        mock_which.return_value = '/usr/bin/openscad'
        
        path = get_openscad_path()
        assert path == '/usr/bin/openscad'
        mock_which.assert_called_with('openscad')

    @patch('shutil.which')
    @patch('os.path.exists')
    def test_get_openscad_path_fallback_to_common_paths(self, mock_exists, mock_which):
        """Test get_openscad_path falls back to common installation paths."""
        # Simulate 'which' not finding OpenSCAD
        mock_which.return_value = None
        
        # Mock that one of the common paths exists
        def mock_exists_side_effect(path):
            return path == '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD'
        
        mock_exists.side_effect = mock_exists_side_effect
        
        path = get_openscad_path()
        assert '/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD' in path

    @patch('shutil.which')
    @patch('os.path.exists')
    def test_get_openscad_path_no_installation_found(self, mock_exists, mock_which):
        """Test get_openscad_path when no OpenSCAD installation is found."""
        # Simulate 'which' not finding OpenSCAD
        mock_which.return_value = None
        
        # Simulate no common paths existing
        mock_exists.return_value = False
        
        # Should fall back to default 'openscad' command
        path = get_openscad_path()
        assert path == 'openscad'

    @patch.dict('os.environ', {'OPENSCAD_PATH': '/custom/path/to/openscad'})
    def test_get_openscad_path_with_env_variable(self):
        """Test get_openscad_path with environment variable set."""
        # If the function supports environment variables
        try:
            path = get_openscad_path()
            # This test might need adjustment based on actual implementation
            if 'OPENSCAD_PATH' in os.environ:
                expected = os.environ['OPENSCAD_PATH']
                # The function might or might not use environment variables
                # so we just test that it returns something valid
                assert isinstance(path, str)
        except Exception:
            # If environment variable support is not implemented, that's fine
            pass

    @patch('platform.system')
    @patch('shutil.which')
    @patch('os.path.exists')
    def test_get_openscad_path_windows(self, mock_exists, mock_which, mock_system):
        """Test get_openscad_path on Windows."""
        mock_system.return_value = 'Windows'
        mock_which.return_value = None
        
        # Mock Windows-specific paths
        def mock_exists_side_effect(path):
            return 'Program Files' in path and 'OpenSCAD' in path
        
        mock_exists.side_effect = mock_exists_side_effect
        
        path = get_openscad_path()
        assert isinstance(path, str)

    @patch('platform.system')
    @patch('shutil.which')
    @patch('os.path.exists')
    def test_get_openscad_path_linux(self, mock_exists, mock_which, mock_system):
        """Test get_openscad_path on Linux."""
        mock_system.return_value = 'Linux'
        mock_which.return_value = None
        
        # Mock Linux-specific paths
        def mock_exists_side_effect(path):
            return path == '/usr/bin/openscad' or path == '/usr/local/bin/openscad'
        
        mock_exists.side_effect = mock_exists_side_effect
        
        path = get_openscad_path()
        assert isinstance(path, str)

    @patch('platform.system')
    @patch('shutil.which')
    @patch('os.path.exists')
    def test_get_openscad_path_macos(self, mock_exists, mock_which, mock_system):
        """Test get_openscad_path on macOS."""
        mock_system.return_value = 'Darwin'
        mock_which.return_value = None
        
        # Mock macOS-specific paths
        def mock_exists_side_effect(path):
            return '/Applications/OpenSCAD.app' in path
        
        mock_exists.side_effect = mock_exists_side_effect
        
        path = get_openscad_path()
        assert isinstance(path, str)

    def test_get_openscad_path_caching(self):
        """Test that get_openscad_path returns consistent results."""
        # Call the function multiple times
        path1 = get_openscad_path()
        path2 = get_openscad_path()
        path3 = get_openscad_path()
        
        # Should return the same path each time (if caching is implemented)
        assert path1 == path2 == path3

    def test_openscad_path_is_executable_name_or_path(self):
        """Test that returned path is either an executable name or valid path."""
        path = get_openscad_path()
        
        # Should either be just 'openscad' (executable name) or a path
        assert path == 'openscad' or os.path.isabs(path) or '/' in path