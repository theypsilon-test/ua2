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

import traceback
import sys
from pathlib import Path

from update_all.config import ConfigReader
from update_all.local_repository import LocalRepositoryProvider
from update_all.logger import FileLoggerDecorator, PrintLogger
from update_all.update_all_service import UpdateAllServiceFactory


def main(env):
    local_repository_provider = LocalRepositoryProvider()
    logger = FileLoggerDecorator(PrintLogger(), local_repository_provider)
    logger.print('START!')
    logger.print()
    # noinspection PyBroadException
    try:
        exit_code = execute_update_all(
            UpdateAllServiceFactory(logger, local_repository_provider=local_repository_provider),
            ConfigReader(logger, env)
        )
    except Exception as _:
        logger.print(traceback.format_exc())
        exit_code = 1

    logger.finalize()
    return exit_code


def execute_update_all(update_all_service, config_reader):
    return update_all_service.create(config_reader.read_config()).full_run()

