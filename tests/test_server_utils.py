# (c) 2023 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
import glob
import os
import subprocess
import tempfile
from unittest.mock import ANY, Mock, patch

import pytest

from ansys.additive.server_utils import DEFAULT_ANSYS_VERSION, launch_server


@patch("os.name", "unknown_os")
def test_launch_server_with_invalid_os_raises_exception():
    # arrange
    # act, assert
    with pytest.raises(OSError) as excinfo:
        launch_server(0)
    assert "Unsupported OS" in str(excinfo.value)


@patch("os.name", "nt")
def test_launch_server_with_windows_os_and_AWP_ROOT_not_defined_raises_exception():
    # arrange
    orig_ansys_ver = None
    if f"AWP_ROOT{DEFAULT_ANSYS_VERSION}" in os.environ:
        orig_ansys_ver = os.environ[f"AWP_ROOT{DEFAULT_ANSYS_VERSION}"]
        del os.environ[f"AWP_ROOT{DEFAULT_ANSYS_VERSION}"]
    # act, assert
    with pytest.raises(Exception) as excinfo:
        launch_server(0)
    assert "Cannot find Ansys installation directory" in str(excinfo.value)

    # cleanup
    if orig_ansys_ver:
        os.environ[f"AWP_ROOT{DEFAULT_ANSYS_VERSION}"] = orig_ansys_ver


@patch("os.name", "posix")
@patch("os.path.isdir")
def test_launch_server_with_linux_os_and_no_install_dir_raises_exception(mock_isdir):
    # arrange
    mock_isdir.return_value = False
    # act, assert
    with pytest.raises(Exception) as excinfo:
        launch_server(0)
    assert "Cannot find Ansys installation directory" in str(excinfo.value)


@patch("os.name", "nt")
@patch("subprocess.Popen")
def test_launch_server_calls_popen_as_expected(mock_popen):
    # arrange
    tmpdir = tempfile.TemporaryDirectory()
    os.environ["AWP_ROOT241"] = tmpdir.name
    mock_process = Mock()
    attrs = {"poll.return_value": None}
    mock_process.configure_mock(**attrs)
    mock_popen.return_value = mock_process

    # act
    launch_server(0, tmpdir.name)

    # assert
    mock_popen.assert_called_once_with(
        '"'
        + os.path.join(tmpdir.name, "Additive", "additive_grpc", "Additive.Grpc.exe")
        + '"'
        + " --port 0",
        shell=False,
        cwd=tmpdir.name,
        stdout=ANY,
        stderr=subprocess.STDOUT,
    )
    assert len(glob.glob(os.path.join(tmpdir.name, "additive_server_*.log"))) == 1


@patch("os.name", "nt")
@patch("subprocess.Popen")
def test_launch_server_raises_exception_if_process_fails_to_start(mock_popen):
    # arrange
    tmpdir = tempfile.TemporaryDirectory()
    os.environ["AWP_ROOT241"] = tmpdir.name
    mock_process = Mock()
    attrs = {"poll.return_value": 1}
    mock_process.configure_mock(**attrs)
    mock_popen.return_value = mock_process

    # act, assert
    with pytest.raises(Exception) as excinfo:
        launch_server(0, tmpdir.name)
    assert "Server exited with code" in str(excinfo.value)
