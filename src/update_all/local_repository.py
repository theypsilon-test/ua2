# coding=utf-8
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
from update_all.config import Config
from update_all.other import GenericProvider
from update_all.constants import FILE_update_all_storage, FILE_update_all_log, FILE_update_all_ini, \
    FILE_downloader_temp_ini, DOWNLOADER_INI_STANDARD_PATH
from update_all.local_store import LocalStore
from update_all.store_migrator import make_new_local_store


class LocalRepositoryProvider:
    def __init__(self):
        self._local_repository = None

    def initialize(self, local_repository):
        assert(self._local_repository is None)
        self._local_repository = local_repository

    def get(self):
        assert(self._local_repository is not None)
        return self._local_repository


class LocalRepository:

    def __init__(self, config_provider: GenericProvider[Config], logger, file_system, store_migrator):
        self._config_provider = config_provider
        self._logger = logger
        self._file_system = file_system
        self._store_migrator = store_migrator
        self._storage_path_value = None
        self._logfile_path_value = None
        self._update_all_ini_path_value = None

    @property
    def _storage_path(self):
        if self._storage_path_value is None:
            self._storage_path_value = f'{self._config_provider.get().base_path}/{FILE_update_all_storage}'
        return self._storage_path_value

    @property
    def _update_all_ini_path(self):
        if self._update_all_ini_path_value is None:
            self._update_all_ini_path_value = f'{self._config_provider.get().base_path}/{FILE_update_all_ini}'
        return self._update_all_ini_path_value

    @property
    def logfile_path(self):
        if self._logfile_path_value is None:
            self._logfile_path_value = f'{self._config_provider.get().base_path}/{FILE_update_all_log}'
        return self._logfile_path_value

    @property
    def downloader_ini_path(self):
        return self._file_system.download_target_path(FILE_downloader_temp_ini if self._config_provider.get().temporary_downloader_ini else DOWNLOADER_INI_STANDARD_PATH)

    def set_logfile_path(self, value):
        self._logfile_path_value = value

    def load_store(self) -> LocalStore:
        self._logger.bench('Loading store...')

        if self._file_system.is_file(self._storage_path):
            try:
                local_store_props = self._file_system.load_dict_from_file(self._storage_path)
            except Exception as e:
                self._logger.debug(e)
                self._logger.print('Could not load store')
                local_store_props = make_new_local_store(self._store_migrator)
        else:
            local_store_props = make_new_local_store(self._store_migrator)

        self._store_migrator.migrate(local_store_props)  # exception must be fixed, users are not modifying this by hand

        return LocalStore(local_store_props)

    def save_store(self, local_store_wrapper: LocalStore):
        if not local_store_wrapper.needs_save():
            self._logger.debug('Skipping local_store saving...')
            return

        local_store = local_store_wrapper.unwrap_props()

        self._file_system.make_dirs_parent(self._storage_path)
        self._file_system.save_json_on_zip(local_store, self._storage_path)

        local_store_wrapper.mark_as_cleaned()

    def save_log_from_tmp(self, path):
        self._file_system.make_dirs_parent(self.logfile_path)
        self._file_system.copy(path, self.logfile_path)


class LocalRepositoryProviderException(Exception):
    pass
