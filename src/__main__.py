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

import os
from update_all.main import main
from update_all.constants import DEFAULT_CURL_SSL_OPTIONS, DEFAULT_INI_PATH \
    KENV_INI_PATH, KENV_CURL_SSL, KENV_COMMIT

if __name__ == '__main__':
    exit_code = main({
        KENV_INI_PATH: os.getenv(KENV_INI_PATH, DEFAULT_INI_PATH),
        KENV_CURL_SSL: os.getenv(KENV_CURL_SSL, DEFAULT_CURL_SSL_OPTIONS),
        KENV_COMMIT: os.getenv(KENV_COMMIT, 'unknown')
    })

    exit(exit_code)
