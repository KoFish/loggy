import sys
import shutil
import term
import math
from output import Output

from time import sleep
from utils import word_wrap


class Console(object):
    def __init__(self):
        if not isinstance(sys.stdout, Output):
            sys.stdout = Output(self, sys.stdout)
        if not isinstance(sys.stderr, Output):
            sys.stderr = Output(self, sys.stderr)
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self._last_log = (None, -1, 0)
        self.stdout.write_raw(term.screen.store_dec('auto_wrap'))
        self.stdout.write_raw(term.screen.reset_dec('auto_wrap'))

    def __del__(self):
        self.stdout.write_raw(term.screen.restore_dec('auto_wrap'))
        self.stdout.write_raw('Reset terminal\n')

    def get_size(self):
        size = shutil.get_terminal_size()
        return size.lines, size.columns

    def get_current_position(self, **kw):
        return term.get_cursor_position(**kw)

    def _log_str(self, *a, **kw):
        sep = kw.get('sep', ' ')
        width = kw.get('width', None)
        string = sep.join(map(str, a))
        if width:
            return '\n'.join(word_wrap(string, width)) + '\n'
        else:
            return string + '\n'

    def log(self, *a, **kw):
        sleep(0.5)
        rows, columns = self.get_size()
        s = self._log_str(*a, **dict(kw, width=columns-10))
        row = self.stdout.get_current_row()
        last_row, last_row_nr, last_row_count = self._last_log
        if s == last_row and last_row_nr == row:
            count = last_row_count + 1
            indsize = math.floor(math.log10(count)) + 1
            string = "{0:>{1}}".format(count, indsize)
            operations = [term.cursor.up(1),
                          term.cursor.place_col(columns - indsize),
                          term.attribute.bold,
                          term.attribute.color(term.color.WHITE, term.color.RED),
                          '{}',
                          term.attribute.reset]
            self.stdout.write_raw(term.reset_position(''.join(map(str, operations))).format(string[:6]))
            self.stdout.flush()
            self._last_log = (s, row, count)
        else:
            self.stdout.write(s)
            self._last_log = (s, row + 1, 1)

    def add_progress_bar(self, min=0, max=100):
        p = ProgressBar(self, min, max)
        return p


class ProgressBar(object):
    def __init__(self, owner, min, max):
        self._owner = owner
        self.min = min
        self.max = max
        self.current = min
        self._start_row = self._owner.stdout.get_current_row()
        self._owner.stdout.write('\n')
        self.draw(current_row=self._start_row + 1)

    def _get_percent(self):
        rcur = self.current - self.min
        rmax = self.max - self.min
        return rcur/rmax

    def draw(self, console_size=None, current_row=None):
        rows, columns = console_size or self._owner.get_size()
        crow = current_row or self._owner.stdout.get_current_row()
        if self._start_row is None:
            self._start_row = crow

        operations = []
        if crow > self._start_row:
            operations += [term.cursor.up(crow - self._start_row), term.cursor.place_col(1)]
        operations += [term.clear.line]
        percent = min(self._get_percent(), 1.0)
        finished = int((columns - 2) * percent)
        operations += ['[' + '=' * finished + '-' * ((columns - 2) - finished) + ']']
        self._owner.stdout.write_raw(term.reset_position(''.join(map(str, operations))))

    def update(self, steps=1):
        self.current += 1
        self.draw()


console = Console()
