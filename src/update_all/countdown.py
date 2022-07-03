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
import math
import sys
import termios
import time
import tty
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import unique, IntEnum, auto
from io import StringIO
from multiprocessing import Process
from threading import Thread


@unique
class CountdownOutcome(IntEnum):
    CONTINUE = auto()
    SETTINGS_SCREEN = auto()


class Countdown(ABC):
    @abstractmethod
    def execute_count(self, n) -> CountdownOutcome:
        """Runs a countdown for 'n' seconds, and returns the outcome"""


class ReadCharactersData:
    def __init__(self):
        self.character: str = ''
        self.ends: bool = False
        try:
            import msvcrt
        except:
            import tty, sys
            self.fd = sys.stdin.fileno()


def read_characters(data: ReadCharactersData):
    while not data.ends:
        data.character = _getch()
        time.sleep(1.0 / 120.0)


class CountdownImpl(Countdown):
    def execute_count(self, count) -> CountdownOutcome:
        print()
        print(" *Press <UP>, To enter the SETTINGS screen.")
        print(" *Press <DOWN>, To continue now.")
        print()

        #os_stdio = _PrepareStdio()
        #os_stdio.save_state()

        read_characters_data = ReadCharactersData()
        read_characters_task = Process(target=read_characters, args=(read_characters_data,))
        read_characters_task.daemon = True
        read_characters_task.start()

        result = CountdownOutcome.CONTINUE
        begin = time.time()
        end = begin + float(count)
        now = begin
        latest_seconds = -1
        while now < end:
            seconds = math.floor(end - now) + 1
            if seconds != latest_seconds:
                seconds_str = f'{seconds} seconds' if seconds >= 10 else f' {seconds} seconds'
                print(f'                                        \rStarting in {seconds_str}.', end='')
                for _ in range(count - seconds + 1):
                    print('.', end='')
                sys.stdout.flush()
                latest_seconds = seconds

            if read_characters_data.character == 'A':
                result = CountdownOutcome.SETTINGS_SCREEN
                break
            elif read_characters_data.character == 'B':
                break

            time.sleep(1.0 / 120.0)
            now = time.time()

        read_characters_data.ends = True
        #os_stdio.restore_state()
        time.sleep(1.0 / 60.0)

        read_characters_task.terminate()

        return result


class _Getch:
    def __init__(self):
        try:
            self._impl = _GetchWindows()
        except ImportError:
            self._impl = _GetchUnix()

    def __call__(self): return self._impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


_getch = _Getch()


class _PrepareStdio:
    def __init__(self):
        try:
            self._impl = _PrepareLinux()
        except ImportError:
            self._impl = _PrepareLinux()

    def save_state(self): return self._impl.prepare()
    def restore_state(self): return self._impl.cleanup()


class _PrepareLinux:
    def __init__(self):
        import tty, sys
        self._fd = None
        self._old_settings = None

    def prepare(self):
        self._fd = sys.stdin.fileno()
        #self._old_settings = termios.tcgetattr(self._fd)

    def cleanup(self):
        #termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old_settings)
        with open(self._fd, 'w') as f:
            f.write('\n')
            f.flush()

        #termios.tcflush(self._fd, termios.TCIOFLUSH)

class _PrepareWindows:
    def __init__(self):
        import msvcrt

    def prepare(self):
        pass

    def cleanup(self):
        pass
