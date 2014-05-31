import re
import fcntl
import os
import tty
import termios

"""
The code for `raw` and `nonblocking` is taken directly from Tom Ballingers[0] blog.

[0]: http://ballingt.com/2014/03/01/nonblocking-stdin-in-python-3.html
"""


class raw(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.original_stty = termios.tcgetattr(self.stream)
        tty.setcbreak(self.stream)

    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)


class nonblocking(object):
    def __init__(self, stream):
        self.stream = stream
        self.fd = self.stream.fileno()

    def __enter__(self):
        self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)

    def __exit__(self, *args):
        fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)


def rmsplit(string, splits):
    cut = max(map(string.rfind, splits))
    if cut >= 0:
        return string[:cut], string[cut+1:]
    else:
        return string, ''


def word_wrap(string, columns, whitespaces=' \t'):
    """Segment the string into a list of rows, each row is no longer than
       the length specified with the columns argument. When splitting the
       row it will always attempt to split it at one of the characters in
       the whitespaces string."""
    rows = []
    while string:
        row, string = string[:columns], string[columns:]
        if '\n' in row:
            row, rest = row.split('\n', 1)
            string = rest + string
            rows.append(row.rstrip(whitespaces))
            continue
        elif string and string[0] not in whitespaces and row[-1] not in whitespaces:
            first, second = rmsplit(row, whitespaces)
            if first:
                row = first
                string = second + string
        rows.append(row.rstrip(whitespaces))
        string = string.lstrip(whitespaces)
    return rows
