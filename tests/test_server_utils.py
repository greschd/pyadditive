# (c) 2023 ANSYS, Inc. Unauthorized use, distribution, or duplication is prohibited.
import glob
import os
from pathlib import Path
import subprocess
import tempfile
from unittest.mock import ANY, Mock, patch

import pytest

from ansys.additive.server_utils import DEFAULT_ANSYS_VERSION, find_open_port, launch_server


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
def test_launch_server_when_exe_not_found_raises_exception():
    # arrange
    os.environ["AWP_ROOT241"] = "Bogus"

    # act, assert
    with pytest.raises(FileNotFoundError) as excinfo:
        launch_server(0)
    assert "Cannot find " in str(excinfo.value)


@pytest.mark.skipif(os.name == "posix", reason="Test only valid on Windows")
@patch("subprocess.Popen")
def test_launch_server_calls_popen_as_expected_win(mock_popen):
    # arrange
    tmpdir = tempfile.TemporaryDirectory()
    mock_process = Mock()
    attrs = {"poll.return_value": None}
    mock_process.configure_mock(**attrs)
    mock_popen.return_value = mock_process
    os.environ["AWP_ROOT241"] = tmpdir.name
    exe_path = os.path.join(tmpdir.name, "Additive", "additive_grpc", "Additive.Grpc.exe")
    os.makedirs(os.path.dirname(exe_path), exist_ok=True)
    Path(exe_path).touch(mode=0o777, exist_ok=True)

    # act
    launch_server(0, tmpdir.name)

    # assert
    mock_popen.assert_called_once_with(
        '"' + exe_path + '"' + " --port 0",
        shell=False,
        cwd=tmpdir.name,
        stdout=ANY,
        stderr=subprocess.STDOUT,
    )
    assert len(glob.glob(os.path.join(tmpdir.name, "additive_server_*.log"))) == 1


@pytest.mark.skipif(os.name == "nt", reason="Test only valid on linux")
@patch("os.path.exists")
@patch("os.path.isdir")
@patch("subprocess.Popen")
def test_launch_server_calls_popen_as_expected_linux(mock_popen, mock_isdir, mock_exists):
    # arrange
    tmpdir = tempfile.TemporaryDirectory()
    mock_process = Mock()
    attrs = {"poll.return_value": None}
    mock_process.configure_mock(**attrs)
    mock_popen.return_value = mock_process
    mock_isdir.return_value = True
    mock_exists.return_value = True
    exe_path = "/usr/ansys_inc/v241/Additive/additive_grpc/Additive.Grpc"

    # act
    launch_server(0, tmpdir.name)

    # assert
    mock_popen.assert_called_once_with(
        '"' + exe_path + '"' + " --port 0",
        shell=True,
        cwd=tmpdir.name,
        stdout=ANY,
        stderr=subprocess.STDOUT,
    )
    assert len(glob.glob(os.path.join(tmpdir.name, "additive_server_*.log"))) == 1


@pytest.mark.skipif(os.name == "posix", reason="Test only valid on Windows")
@patch("subprocess.Popen")
def test_launch_server_raises_exception_if_process_fails_to_start_win(mock_popen):
    # arrange
    tmpdir = tempfile.TemporaryDirectory()
    os.environ["AWP_ROOT241"] = tmpdir.name
    mock_process = Mock()
    attrs = {"poll.return_value": 1}
    mock_process.configure_mock(**attrs)
    mock_popen.return_value = mock_process
    exe_path = os.path.join(tmpdir.name, "Additive", "additive_grpc", "Additive.Grpc.exe")
    os.makedirs(os.path.dirname(exe_path), exist_ok=True)
    Path(exe_path).touch(mode=0o777, exist_ok=True)

    # act, assert
    with pytest.raises(Exception) as excinfo:
        launch_server(0, tmpdir.name)
    assert "Server exited with code" in str(excinfo.value)


@pytest.mark.skipif(os.name == "nt", reason="Test only valid on linux")
@patch("os.path.exists")
@patch("os.path.isdir")
@patch("subprocess.Popen")
def test_launch_server_raises_exception_if_process_fails_to_start_linux(
    mock_popen, mock_isdir, mock_exists
):
    # arrange
    tmpdir = tempfile.TemporaryDirectory()
    mock_process = Mock()
    attrs = {"poll.return_value": 1}
    mock_process.configure_mock(**attrs)
    mock_popen.return_value = mock_process
    mock_isdir.return_value = True
    mock_exists.return_value = True

    # act, assert
    with pytest.raises(Exception) as excinfo:
        launch_server(0, tmpdir.name)
    assert "Server exited with code" in str(excinfo.value)


def test_find_open_port_returns_valid_port():
    # act
    port = find_open_port()

    # assert
    assert port > 1024 and port < 65535