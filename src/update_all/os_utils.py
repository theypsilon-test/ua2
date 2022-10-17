#!/usr/bin/env python3
# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# You can download the latest version of this tool from:
# https://github.com/theypsilon-test/ua2

import subprocess
import time
from abc import ABC
from urllib.request import urlopen

from update_all.config import Config
from update_all.other import GenericProvider
from update_all.logger import Logger


class OsUtils(ABC):
    def sync(self) -> None:
        """send sync signal to the OS"""

    def reboot(self) -> None:
        """send reboot signal to the OS"""

    def execute_process(self, launcher, env) -> int:
        """execute launcher process with subprocess and the given env. output gets redirected to stdout"""

    def read_command_output(self, cmd, env) -> [int, str]:
        """executes command with the given env and returns output and success code"""

    def sleep(self, seconds) -> None:
        """waits given seconds"""

    def download(self, url) -> bytes:
        """downloads given url and returns content as string"""


class LinuxOsUtils(OsUtils):
    def __init__(self, config_provider: GenericProvider[Config], logger: Logger):
        self._config_provider = config_provider
        self._logger = logger

    def sync(self) -> None:
        subprocess.run(['sync'], shell=False, stderr=subprocess.STDOUT)

    def reboot(self) -> None:
        subprocess.run(['reboot', 'now'], shell=False, stderr=subprocess.STDOUT)

    def execute_process(self, launcher, env) -> int:
        proc = subprocess.Popen(['python3', launcher], env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        return_code = proc.poll()
        while return_code is None:
            if proc.stdout is not None:
                outline = proc.stdout.readline().decode()
                if len(outline):
                    self._logger.print(f'{outline}', end='')

            time.sleep(1.0 / 120.0)
            return_code = proc.poll()

        if proc.stdout is not None:
            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                outline = line.decode()
                if len(outline):
                    self._logger.print(f'{outline}', end='')

        return return_code

    def read_command_output(self, cmd, env) -> [int, str]:
        proc = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return proc.returncode, proc.stdout.decode()

    def sleep(self, seconds) -> None:
        time.sleep(seconds)

    def download(self, url) -> bytes:
        with urlopen(url) as webpage:
            return webpage.read()
