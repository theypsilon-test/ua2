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
from update_all.constants import FILE_update_all_storage, FILE_update_all_log, K_BASE_PATH
from update_all.local_store_wrapper import LocalStoreWrapper
from update_all.other import UnreachableException, empty_store_without_base_path
from update_all.store_migrator import make_new_local_store


class LocalRepositoryProvider:
    def __init__(self):
        self._local_repository = None

    def initialize(self, local_repository):
        if self._local_repository is not None:
            raise LocalRepositoryProviderException("Shouldn't initialize self twice.")

        self._local_repository = local_repository

    @property
    def local_repository(self):
        if self._local_repository is None:
            raise LocalRepositoryProviderException("Can't get a local repository before initializing self.")

        return self._local_repository


class LocalRepository:
    def __init__(self, config, logger, file_system, store_migrator, external_drives_repository):
        self._config = config
        self._logger = logger
        self._file_system = file_system
        self._store_migrator = store_migrator
        self._storage_path_value = None
        self._logfile_path_value = None

    @property
    def _storage_path(self):
        if self._storage_path_value is None:
            self._storage_path_value = '%s/%s' % (self._config[K_BASE_PATH], FILE_update_all_storage)
        return self._storage_path_value

    @property
    def logfile_path(self):
        if self._logfile_path_value is None:
            self._logfile_path_value = '%s/%s' % (self._config[K_BASE_PATH], FILE_update_all_log)
        return self._logfile_path_value

    def set_logfile_path(self, value):
        self._logfile_path_value = value

    def load_store(self):
        self._logger.bench('Loading store...')

        if self._file_system.is_file(self._storage_path):
            try:
                local_store = self._file_system.load_dict_from_file(self._storage_path)
            except Exception as e:
                self._logger.debug(e)
                self._logger.print('Could not load store')
                local_store = make_new_local_store(self._store_migrator)
        else:
            local_store = make_new_local_store(self._store_migrator)

        self._store_migrator.migrate(local_store)  # exception must be fixed, users are not modifying this by hand

        return LocalStoreWrapper(local_store)

    def save_store(self, local_store_wrapper):
        if not local_store_wrapper.needs_save():
            self._logger.debug('Skipping local_store saving...')
            return

        local_store = local_store_wrapper.unwrap_local_store()

        self._file_system.make_dirs_parent(self._storage_path)
        self._file_system.save_json_on_zip(local_store, self._storage_path)

    def save_log_from_tmp(self, path):
        self._file_system.make_dirs_parent(self.logfile_path)
        self._file_system.copy(path, self.logfile_path)


class LocalRepositoryProviderException(Exception):
    pass
