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

from update_all.store_migrator import StoreMigrator
from update_all.migrations import migrations
from update_all.local_repository import LocalRepository
from update_all.file_system import FileSystemFactory


class UpdateAllServiceFactory:
    def __init__(self, logger, local_repository_provider):
        self._logger = logger
        self._local_repository_provider = local_repository_provider

    def create(self, config):
        store_migrator = StoreMigrator(migrations(), self._logger)
        file_system = FileSystemFactory(config, {}, self._logger).create_for_system_scope()
        local_repository = LocalRepository(config, self._logger, file_system, store_migrator)
        self._local_repository_provider.initialize(local_repository)
        return UpdateAllService(self._logger, self._local_repository_provider, store_migrator)

class UpdateAllService:
    def __init__(self, logger, local_repository_provider, store_migrator):
        self._logger = logger
        self._local_repository_provider = local_repository_provider
        self._store_migrator = store_migrator

    def full_run(self):
        return 0
