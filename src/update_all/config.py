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

import configparser
import json
import re
import time
from enum import IntEnum, unique
from pathlib import Path, PurePosixPath

from update_all.constants import K_BASE_PATH, K_ALLOW_REBOOT, K_ALLOW_DELETE, K_UPDATE_LINUX, K_VERBOSE, K_CONFIG_PATH, KENV_INI_PATH, \
    MEDIA_FAT, K_DEBUG, K_CURL_SSL, KENV_CURL_SSL, KENV_COMMIT, \
    K_FAIL_ON_FILE_ERROR, K_COMMIT, K_UPDATE_LINUX_ENVIRONMENT, K_DEFAULT_DB_ID, K_START_TIME
from update_all.ini_parser import IniParser


def config_with_base_path(config, base_path):
    result = config.copy()
    result[K_BASE_PATH] = base_path
    return result


@unique
class AllowDelete(IntEnum):
    NONE = 0
    ALL = 1
    OLD_RBF = 2


@unique
class AllowReboot(IntEnum):
    NEVER = 0
    ALWAYS = 1
    ONLY_AFTER_LINUX_UPDATE = 2


@unique
class UpdateLinuxEnvironment(IntEnum):
    TRUE = 0
    FALSE = 1
    ONLY = 2


def default_config():
    return {
        K_CONFIG_PATH: Path('/tmp/wrong_config_path.ini'),
        K_BASE_PATH: MEDIA_FAT,
        K_ALLOW_DELETE: AllowDelete.ALL,
        K_ALLOW_REBOOT: AllowReboot.ALWAYS,
        K_UPDATE_LINUX: True,
        K_VERBOSE: False,
        K_DEBUG: False,
        K_START_TIME: 0
    }


class ConfigReader:
    def __init__(self, logger, env):
        self._logger = logger
        self._env = env

    def read_config(self):
        config_path = self._env[KENV_INI_PATH]
        self._logger.print("Reading file: %s" % config_path)

        result = default_config()

        result[K_BASE_PATH] = str(Path(config_path).resolve().parent.parent)
        result[K_CURL_SSL] = self._valid_max_length(KENV_CURL_SSL, self._env[KENV_CURL_SSL], 50)
        result[K_COMMIT] = self._valid_max_length(KENV_COMMIT, self._env[KENV_COMMIT], 50)
        result[K_START_TIME] = time.time()
        result[K_CONFIG_PATH] = config_path

        self._logger.configure(result)

        self._logger.debug('env: ' + json.dumps(self._env, indent=4))
        self._logger.debug('config: ' + json.dumps(result, default=lambda o: o.__dict__, indent=4))

        result[K_CONFIG_PATH] = Path(result[K_CONFIG_PATH])

        return result

    def _valid_max_length(self, key, value, max_limit):
        if len(value) <= max_limit:
            return value

        raise InvalidConfigParameter("Invalid %s with value '%s'. Too long string (max is %s)." % (key, value, max_limit))


class InvalidConfigParameter(Exception):
    pass


