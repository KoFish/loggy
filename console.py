import sys
import shutil
import term
import math
from output import Output

from time import sleep
from utils import word_wrap


class Console(object):
    def __init__(self):
        self._line_count = 0
        if not isinstance(sys.stdout, Output):
            sys.stdout = Output(self, sys.stdout)
        if not isinstance(sys.stderr, Output):
            sys.stderr = Output(self, sys.stderr)
        self.stdout = sys.stdout
        self.stderr = sys.stderr

        self._last_log = (None, -1, 0)
        self._items = []
        self.stdout.write_raw(term.screen.store_dec('auto_wrap'))
        self.stdout.write_raw(term.screen.reset_dec('auto_wrap'))

    def __del__(self):
        self.stdout.write_raw(term.screen.restore_dec('auto_wrap'))
        sys.stdout = self.stdout._out
        sys.stderr = self.stderr._out

    def get_size(self):
        size = shutil.get_terminal_size()
        return size.lines, size.columns

    def get_current_position(self, **kw):
        return term.get_cursor_position(**kw)

    def add_row_count(self, count):
        self._line_count += count

    def get_row_count(self):
        return self._line_count

    def update(self):
        console_size = self.get_size()
        current_row = self.get_row_count()
        for each in self._items:
            if each._done:
                self._items.remove(each)
            else:
                each._update(console_size, current_row)

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
        row = self.get_row_count()
        last_row, last_row_nr, counter = self._last_log
        if s == last_row and last_row_nr == row:
            counter.inc()
            self._last_log = (s, row, counter)
        else:
            self.stdout.write(s)
            c = Counter(offset=1, min_value=2, owner=self)
            c.inc()
            self._items.append(c)
            self._last_log = (s, row + 1, c)

    def add_progress_bar(self, min=0, max=100, **kw):
        p = ProgressBar(min, max, owner=self, **kw)
        self._items.append(p)
        return p

    def add_checkbox(self, text, **kw):
        cb = Checkbox(text, owner=self, **kw)
        self._items.append(cb)
        return cb


class RelTermItem(object):
    def __init__(self, offset=0, owner=None):
        self._owner = owner
        self._done = False
        self._start_row = self._owner.get_row_count() - offset

    def _update(self, console_size=None, current_row=None):
        if self._done:
            return
        rows, cols = console_size or self._owner.get_size()
        current_row = current_row or self._owner.get_row_count()
        diff = current_row - self._start_row
        if diff >= rows:
            self._done = True
            return
        operations = []
        if diff > 0:
            operations.append(term.cursor.up(diff))
        item_string = self.draw((rows, cols), current_row)
        if item_string is not None:
            operations.append(item_string)
            self._owner.stdout.write_raw(term.reset_position(''.join(operations)))
        self._owner.stdout.flush()

    @property
    def done(self):
        return self._done


class Counter(RelTermItem):
    def __init__(self, offset, min_value, owner):
        super(Counter, self).__init__(offset=offset, owner=owner)
        self.value = 0
        self._min_value = min_value

    def inc(self, count=1):
        self.value += count
        self._update()

    def draw(self, console_size, current_row):
        if self.value < self._min_value:
            return None
        rows, cols = console_size
        indsize = math.floor(math.log10(self.value)) + 1
        operations = [
            term.cursor.place_col(cols - indsize + 1),
            # term.cursor.place_col(0),
            term.attribute.bold,
            term.attribute.color(term.color.WHITE, term.color.RED),
            str(self.value),
            term.attribute.reset
        ]
        return ''.join(operations)


class ProgressBar(RelTermItem):
    def __init__(self, min_value, max_value, owner, width=0):
        super(ProgressBar, self).__init__(owner=owner)
        self.min = min_value
        self.max = max_value
        self.max_width = max(width, 0)
        self.current = min_value
        self._owner.stdout.write('\n')
        self._update(current_row=self._start_row + 1)

    def _get_percent(self):
        rcur = self.current - self.min
        rmax = self.max - self.min
        return rcur/rmax

    def draw(self, console_size, current_row):
        rows, columns = console_size or self._owner.get_size()
        operations = [
            term.cursor.place_col(1),
            term.clear.line
        ]
        width = min(self.max_width, columns)
        percent = min(self._get_percent(), 1.0)
        finished = int((width - 2) * percent)
        operations += ['[' + '=' * finished + '-' * ((width - 2) - finished) + ']']
        return ''.join(map(str, operations))

    def update(self, steps=1):
        self.current += 1
        self._update()


class Checkbox(RelTermItem):
    UNCHECKED = 0
    TRISTATE = 1
    CHECKED = 2

    def __init__(self, text, owner):
        super(Checkbox, self).__init__(owner=owner)
        self.state = Checkbox.UNCHECKED
        self.text = text
        self._owner.stdout.write('\n')
        self._update(current_row=self._start_row + 1)

    def draw(self, console_size, current_row):
        return ('[{}] '+self.text).format({0: ' ', 1: '-', 2: 'X'}.get(self.state, 'E'))

    def check(self, tristate):
        self.state = Checkbox.CHECKED if not tristate else Checkbox.TRISTATE
        self._update()
        self._done = True

console = Console()
