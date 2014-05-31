import re
import sys
import termdefs.vt100 as vt
from termdefs import xterm
from time import time
from utils import raw, nonblocking


vt10x_re = r'(\033(?:\[(?:\?|)[0-9;]*(?:\$.| q|.)|[()].|[0-9]n|.))'

tokenize_string = lambda s: re.split(vt10x_re, s)
remove_escapes = lambda s: ''.join(filter(lambda ss: not ss.startswith('\033'), tokenize_string(s)))


class screen():
    DEC = {
        'cursor_key': 1,
        'ansi': 2,
        '132col': 3,
        'smooth_scroll': 4,
        'reverse_video': 5,
        'relative_origin': 6,
        'auto_wrap': 7,
        'auto_repeat': 8,
        'interlacing': 9,
        'full_screen_print': 19,  # Kind of missleading, reset limits to scrolling area
        'show_cursor': 25,
        'show_scrollbar': 30,
        'left_right_margin': 69,
        'alt_buffer': 1047,
        'alt_buffer_store': 1049
    }
    new_line_mode = vt.LMN_set
    line_feed_mode = vt.LMN_reset
    cursor_app_mode = vt.DECCKM_set
    cursor_term_mode = vt.DECCKM_reset
    reverse = vt.DECSCNM_set
    unreverse = vt.DECSCNM_reset
    auto_wrap_mode = vt.DECAWM_set
    no_wrap_mode = vt.DECAWM_reset
    auto_repeat_mode = vt.DECARM_set
    no_repeat_mode = vt.DECARM_reset
    alt_keypad_mode = vt.DECKPAM
    num_keypad_mode = vt.DECKPNM

    top_bottom_margins = vt.DECSTBM[0].format

    scroll_up = vt.IND
    scroll_down = vt.RI

    reset = vt.RIS

    @staticmethod
    def set_dec(name):
        if name in screen.DEC:
            return vt.DEC_set[0].format(screen.DEC[name])
        else:
            raise IndexError("No such DEC private mode variable")

    @staticmethod
    def reset_dec(name):
        if name in screen.DEC:
            return vt.DEC_reset[0].format(screen.DEC[name])
        else:
            raise IndexError("No such DEC private mode variable")

    @staticmethod
    def store_dec(name):
        if name in screen.DEC:
            return xterm.SAVEDEC[0].format(screen.DEC[name])
        else:
            raise IndexError("No such DEC private mode variable")

    @staticmethod
    def restore_dec(name):
        if name in screen.DEC:
            return xterm.RESETDEC[0].format(screen.DEC[name])
        else:
            raise IndexError("No such DEC private mode variable")


class color():
    BLACK = vt.BLACK
    RED = vt.RED
    GREEN = vt.GREEN
    YELLOW = vt.YELLOW
    BLUE = vt.BLUE
    MAGENTA = vt.MAGENTA
    CYAN = vt.CYAN
    WHITE = vt.WHITE


class attribute():
    reset = vt.SGR0
    bold = vt.SGR1
    low_intensity = vt.SGR2
    underline = vt.SGR4
    blinking = vt.SGR5
    reverse = vt.SGR7
    invisible = vt.SGR8

    @staticmethod
    def color(fg=None, bg=None):
        attrs = []
        if fg:
            attrs.append(30 + fg)
        if bg:
            attrs.append(40 + bg)
        return vt.color[0].format(';'.join(map(str, attrs)))


class cursor():
    up = vt.CUU[0].format
    down = vt.CUD[0].format
    right = vt.CUF[0].format
    left = vt.CUB[0].format
    place = vt.CUP[0].format
    place_col = xterm.CHA[0].format
    home = vt.cursorhome

    save = vt.DECSC_set
    restore = vt.DECSC_reset


class insert():
    characters = xterm.ICH[0].format
    lines = xterm.IL[0].format


class remove():
    characters = xterm.DCH[0].format
    lines = xterm.DL[0].format


class clear():
    up = vt.ED1
    down = vt.ED0
    right = vt.EL0
    left = vt.EL1
    line = vt.EL2
    screen = vt.ED2

    characters = xterm.ECH[0].format


def _request_term_info(request, until, out_stream=None, in_stream=None, timeout=0.5):
    _out = out_stream or sys.stdout
    _in = in_stream or sys.stdin
    with raw(_in):
        with nonblocking(_in):
            _out.write(request)
            _out.flush()
            resp = c = ''
            start = time()
            while not resp.endswith(until):
                c = _in.read(1)
                if c:
                    resp += c
                elif (time() - start) > timeout:
                    raise Exception("Request timed out")
    return resp


def get_cursor_position(**kw):
    string = _request_term_info(vt.DSR_cursor, 'R', **kw)
    return tuple([int(i) for i in string[2:-1].split(';')])


def get_term_caps(**kw):
    string = _request_term_info(vt.DA, 'c', **kw)
    return tuple([int(i) for i in string[3:-1].split(';')])


def get_device_status(**kw):
    string = _request_term_info(vt.DSR, 'n', **kw)
    return 'OK' if string[2:-1] == '0' else 'NOT OK'


def reset_position(string):
    return cursor.save + string + cursor.restore
