ESC = '\033'
CSI = ESC + '['

LMN_set       = CSI + '20h'  # Set new line mode
LMN_reset     = CSI + '20l'  # Set line feed mode
DEC_set       = (CSI + '?{}h', ('decvar',))
DEC_reset     = (CSI + '?{}l', ('decvar',))
DECCKM_set    = CSI + '?1h'  # Set cursor key to application
DECCKM_reset  = CSI + '?1l'  # Set cursor key to cursor
DECANM_set    = ''           # Set ANSI (versus VT52)
DECANM_reset  = CSI + '?2l'  # Set VT52 (versus ANSI)
DECCOLM_set   = CSI + '?3h'  # Set number of columns to 132
DECCOLM_reset = CSI + '?3l'  # Set number of columns to 80
DECSCLM_set   = CSI + '?4h'  # Set smooth scrolling
DECSCLM_reset = CSI + '?4l'  # Set jump scrolling
DECSCNM_set   = CSI + '?5h'  # Set reverse video on screen
DECSCNM_reset = CSI + '?5l'  # Set normal video on screen
DECOM_set     = CSI + '?6h'  # Set origin to relative
DECOM_reset   = CSI + '?6l'  # Set origin to absolute
DECAWM_set    = CSI + '?7h'  # Set auto-wrap mode
DECAWM_reset  = CSI + '?7l'  # Reset auto-wrap mode
DECARM_set    = CSI + '?8h'  # Set auto-repeat mode
DECARM_reset  = CSI + '?8l'  # Reset auto-repeat mode
DECINLM_set   = CSI + '?9h'  # Set interlacing mode
DECINLM_reset = CSI + '?9l'  # Reset interlacing mode

DECKPAM = ESC + '='  # Set alternate keypad mode
DECKPNM = ESC + '>'  # Set numeric keypad mode

setukg0      = ESC + '(A'  # Set United Kingdom G0 character set
setukg1      = ESC + ')A'  # Set United Kingdom G1 character set
setusg0      = ESC + '(B'  # Set United States G0 character set
setusg1      = ESC + ')B'  # Set United States G1 character set
setspecg0    = ESC + '(0'  # Set G0 special chars. & line set
setspecg1    = ESC + ')0'  # Set G1 special chars. & line set
setaltg0     = ESC + '(1'  # Set G0 alternate character ROM
setaltg1     = ESC + ')1'  # Set G1 alternate character ROM
setaltspecg0 = ESC + '(2'  # Set G0 alt char ROM and spec. graphics
setaltspecg1 = ESC + ')2'  # Set G1 alt char ROM and spec. graphics

SS2 = ESC + 'N'  # Set single shift 2
SS3 = ESC + 'O'  # Set single shift 3

SGR0 = CSI + 'm'  # Turn off character attributes
# SGR0 = CSI + '0m'  # Turn off character attributes
SGR1 = CSI + '1m'  # Turn bold mode on
SGR2 = CSI + '2m'  # Turn low intensity mode on
SGR4 = CSI + '4m'  # Turn underline mode on
SGR5 = CSI + '5m'  # Turn blinking mode on
SGR7 = CSI + '7m'  # Turn reverse video on
SGR8 = CSI + '8m'  # Turn invisible text mode on

BOLD = 1
LOW_INTENSITY = 2
UNDERLINE = 4
BLINKING = 5
REVERSE = 7
INVISIBLE = 8

color = (CSI + '{}m', ('color',))  # Set current color attribute

BLACK = 0
RED = 1
GREEN = 2
YELLOW = 3
BLUE = 4
MAGENTA = 5
CYAN = 6
WHITE = 7
FG_COL = 30
BG_COL = 40

DECSTBM = (CSI + '{};{}r', ('top', 'bottom'))  # Set top and bottom lines of a window

CUU = (CSI + '{}A', ('value',))  # Move cursor up n lines
CUD = (CSI + '{}B', ('value',))  # Move cursor down n lines
CUF = (CSI + '{}C', ('value',))  # Move cursor right n lines
CUB = (CSI + '{}D', ('value',))  # Move cursor left n lines
cursorhome = CSI + 'H'  # Move cursor to upper left corner
# cursorhome = CSI + ';H'  # Move cursor to upper left corner
CUP = (CSI + '{};{}H', ('line', 'column'))  # Move cursor to screen location v,h
hvhome = CSI + 'f'  # Move cursor to upper left corner
# hvhome = CSI + ';f'  # Move cursor to upper left corner
CUP_alt = (CSI + '{};{}f', ('line', 'column'))  # Move cursor to screen location v,h
IND = ESC + 'D'  # Move/scroll window up one line
RI = ESC + 'M'  # Move/scroll window down one line
NEL = ESC + 'E'  # Move to next line
DECSC_set   = ESC + '7'  # Save cursor position and attributes
DECSC_reset = ESC + '8'  # Restore cursor position and attributes

HTS = ESC + 'H'  # Set a tab at the current column
TBC = CSI + 'g'  # Clear a tab at the current column
# TBC = CSI + '0g'  # Clear a tab at the current column
TBC_all = CSI + '3g'  # Clear all tabs

DECDHL_top    = ESC + '#3'  # Double-height letters, top half
DECDHL_bottom = ESC + '#4'  # Double-height letters, bottom half
DECSWL        = ESC + '#5'  # Single width, single height letters
DECDWL        = ESC + '#6'  # Double width, single height letters

EL0 = CSI + 'K'  # Clear line from cursor right
# EL0 = CSI + '0K'  # Clear line from cursor right
EL1 = CSI + '1K'  # Clear line from cursor left
EL2 = CSI + '2K'  # Clear entire line

ED0 = CSI + 'J'  # Clear screen from cursor down
# ED0 = CSI + '0J'  # Clear screen from cursor down
ED1 = CSI + '1J'  # Clear screen from cursor up
ED2 = CSI + '2J'  # Clear entire screen

DSR        = CSI + '5n'  # Device status report
DSR_ok     = CSI + '0n'  # Response: terminal is OK
DSR_not_ok = CSI + '3n'  # Response: terminal is not OK

DSR_cursor = CSI + '6n'  # Get cursor position
CPR_resp   = (CSI + '{};{}R', ('line', 'column'))  # Response: cursor is at v,h

DA      = CSI + 'c'  # Identify what terminal type
# DA      = CSI + '0c'  # Identify what terminal type (another)
DA_resp = (CSI + '?1;{}0c', ('value'))  # Response: terminal type code n

RIS = ESC + 'c'  # Reset terminal to initial state

DECALN = ESC + '#8'  # Screen alignment display
# DECTST = CSI + '2;1y'  # Confidence power up test
# DECTST = CSI + '2;2y'  # Confidence loopback test
# DECTST = CSI + '2;9y'  # Repeat power up test
# DECTST = CSI + '2;10y'  # Repeat loopback test

# DECLL0 = CSI + '0q'  # Turn off all four leds
# DECLL1 = CSI + '1q'  # Turn on LED #1
# DECLL2 = CSI + '2q'  # Turn on LED #2
# DECLL3 = CSI + '3q'  # Turn on LED #3
# DECLL4 = CSI + '4q'  # Turn on LED #4
