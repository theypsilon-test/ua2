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

class LocalStore:
    def __init__(self, local_store):
        self._local_store = local_store
        self._dirty = False

    def unwrap_local_store(self):
        return self._local_store

    def mark_force_save(self):
        self._dirty = True

    def needs_save(self):
        return self._dirty


class LocalStoreProvider:
    _local_store: LocalStore

    def __init__(self):
        self._local_store = None

    def initialize(self, local_store: LocalStore) -> None:
        assert(self._local_store is None)
        self._local_store = local_store

    def get(self) -> LocalStore:
        assert(self._local_store is not None)
        return self._local_store
