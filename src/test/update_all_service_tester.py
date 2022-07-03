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
from typing import Tuple

from test.countdown_stub import CountdownStub
from test.fake_filesystem import FileSystemFactory
from test.logger_tester import NoLogger
from test.spy_os_utils import SpyOsUtils
from update_all.config import ConfigReader, ConfigProvider, Config
from update_all.constants import KENV_COMMIT, KENV_CURL_SSL, KENV_INI_PATH, DEFAULT_INI_PATH, DEFAULT_CURL_SSL_OPTIONS, \
    DEFAULT_COMMIT
from update_all.countdown import Countdown
from update_all.file_system import FileSystem
from update_all.local_repository import LocalRepositoryProvider, LocalRepository
from update_all.local_store import LocalStoreProvider
from update_all.os_utils import OsUtils
from update_all.store_migrator import StoreMigrator
from update_all.update_all_service import UpdateAllServiceFactory, UpdateAllService


def default_env():
    return {
        KENV_INI_PATH: DEFAULT_INI_PATH,
        KENV_CURL_SSL: DEFAULT_CURL_SSL_OPTIONS,
        KENV_COMMIT: DEFAULT_COMMIT
    }


class UpdateAllServiceFactoryTester(UpdateAllServiceFactory):
    def __init__(self):
        super().__init__(NoLogger(), LocalRepositoryProvider())


class ConfigReaderTester(ConfigReader):
    def __init__(self, config: Config = None):
        self._config = config
        super().__init__(NoLogger(), default_env())

    def read_config(self) -> Tuple[Config, bool]:
        if self._config is not None:
            return self._config, True

        return super().read_config()


class StoreMigratorTester(StoreMigrator):
    def __init__(self):
        super().__init__([], NoLogger())


class LocalRepositoryTester(LocalRepository):
    def __init__(self, config_provider: ConfigProvider = None, file_system: FileSystem = None, store_migrator: StoreMigrator = None):
        super().__init__(
            config_provider=config_provider or ConfigProvider(),
            logger=NoLogger(),
            file_system=file_system or FileSystemFactory().create_for_system_scope(),
            store_migrator=store_migrator or StoreMigratorTester()
        )


class UpdateAllServiceTester(UpdateAllService):
    def __init__(self, config_reader: ConfigReader = None,
                 config_provider: ConfigProvider = None,
                 local_store_provider: LocalStoreProvider = None,
                 local_repository: LocalRepository = None,
                 store_migrator: StoreMigrator = None,
                 file_system: FileSystem = None,
                 os_utils: OsUtils = None,
                 countdown: Countdown = None):

        config_provider = config_provider or ConfigProvider()
        config_reader = config_reader or ConfigReaderTester()
        local_store_provider = local_store_provider or LocalStoreProvider()
        store_migrator = store_migrator or StoreMigratorTester()
        file_system = file_system or FileSystemFactory().create_for_system_scope()
        local_repository = local_repository or LocalRepositoryTester(config_provider=config_provider, file_system=file_system, store_migrator=store_migrator)

        super().__init__(
            config_reader=config_reader,
            config_provider=config_provider,
            local_store_provider=local_store_provider,
            logger=NoLogger(),
            local_repository=local_repository,
            store_migrator=store_migrator,
            file_system=file_system,
            os_utils=os_utils or SpyOsUtils(),
            countdown=countdown or CountdownStub()
        )
