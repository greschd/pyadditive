# Copyright (C) 2023 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from enum import IntEnum
from os.path import exists

from ansys.api.additive.v0.additive_domain_pb2 import BuildFileMachineType


class MachineType(IntEnum):
    NONE = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_NONE
    ADDITIVE_INDUSTRIES = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_AI
    SLM = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_SLM
    RENISHAW = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_RENISHAW
    EOS = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_EOS
    TRUMPF = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_TRUMPF
    HB3D = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_HB3D
    SISMA = BuildFileMachineType.BUILD_FILE_MACHINE_TYPE_SISMA


class BuildFile:
    """Provides the build file description."""

    def __init__(self, type: MachineType, path: str):
        if not isinstance(type, MachineType):
            raise ValueError("Invalid machine type")
        if not exists(path):
            raise ValueError(f"File does not exist, {path}")
        self._type = type
        self._path = path

    def __repr__(self):
        repr = (
            type(self).__name__
            + "\n"
            + f"type: {MachineType(self._type).name}\n"
            + f"path: {self._path}\n"
        )
        return repr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BuildFile):
            return False
        for k in self.__dict__:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    @property
    def type(self) -> MachineType:
        """Additive manufacturing machine type this file is for."""
        return self._type

    @type.setter
    def type(self, value: MachineType):
        """Set machine type."""
        if not isinstance(value, MachineType):
            raise ValueError("Attempted to assign type with invalid value")
        self._type = value

    @property
    def path(self) -> str:
        """Path of the ZIP file containing the build instruction file, geometry
        STL file, and optional support STL files."""
        return self._path

    @path.setter
    def path(self, value: str):
        """Set file path."""
        if not isinstance(value, str):
            raise ValueError("Attempted to assign path with invalid value")
        if not exists(value):
            raise ValueError(f"File does not exist, {value}")
        self._path = value


class StlFile:
    """Container for the STL file definition."""

    def __init__(self, path: str):
        if not exists(path):
            raise ValueError(f"File does not exist, {path}")
        self._path = path

    def __repr__(self):
        repr = type(self).__name__ + "\n"
        for k in self.__dict__:
            repr += k.replace("_", "", 1) + ": " + str(getattr(self, k)) + "\n"
        return repr

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, StlFile):
            return False
        for k in self.__dict__:
            if getattr(self, k) != getattr(other, k):
                return False
        return True

    @property
    def path(self) -> str:
        """Path of the STL file."""
        return self._path

    @path.setter
    def path(self, value: str):
        """Set file path."""
        if not isinstance(value, str):
            raise ValueError("Attempted to assign path with invalid value")
        if not exists(value):
            raise ValueError(f"File does not exist, {value}")
        self._path = value
