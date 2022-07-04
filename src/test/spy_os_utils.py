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

from update_all.os_utils import OsUtils


class SpyOsUtils(OsUtils):
    def __init__(self):
        super().__init__()
        self.calls_to_sync = 0
        self.calls_to_reboot = 0
        self.calls_to_sleep = []
        self.calls_to_execute_process = []
        self.calls_to_download = []

    def sync(self):
        self.calls_to_sync += 1

    def reboot(self):
        self.calls_to_reboot += 1

    def sleep(self, seconds):
        self.calls_to_sleep.append(seconds)

    def execute_process(self, launcher, env):
        self.calls_to_execute_process.append((launcher, env))
        return 0

    def download(self, url) -> bytes:
        self.calls_to_download.append(url)
        return bytes()
