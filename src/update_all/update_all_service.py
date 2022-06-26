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
from update_all.base_path_relocator import BasePathRelocator
from update_all.certificates_fix import CertificatesFix
from update_all.db_gateway import DbGateway
from update_all.external_drives_repository import ExternalDrivesRepositoryFactory
from update_all.file_downloader import make_file_downloader_factory
from update_all.file_filter import FileFilterFactory
from update_all.file_system import FileSystemFactory
from update_all.full_run_service import FullRunService
from update_all.os_utils import LinuxOsUtils
from update_all.storage_priority_resolver import StoragePriorityResolver
from update_all.linux_updater import LinuxUpdater
from update_all.local_repository import LocalRepository
from update_all.migrations import migrations
from update_all.offline_importer import OfflineImporter
from update_all.online_importer import OnlineImporter
from update_all.path_resolver import PathResolverFactory
from update_all.reboot_calculator import RebootCalculator
from update_all.store_migrator import StoreMigrator
from update_all.waiter import Waiter


class UpdateAllServiceFactory:
    def __init__(self, logger, local_repository_provider):
        self._logger = logger
        self._local_repository_provider = local_repository_provider

    def create(self, config):
        return UpdateAllService(self._logger, self._local_repository_provider)

class UpdateAllService:
    def __init__(self, logger, local_repository_provider):
        self._logger = logger
        self._local_repository_provider = local_repository_provider

    def full_run(self):
        return 0
