from .vt100 import ESC, CSI

DCS = ESC + 'P'
ST = ESC + '\\'
OSC = ESC + ']'


# VT400 and up

DECCARA = (CSI + '{};{};{};{};{}$r', ('top', 'left', 'bottom', 'right', 'attribute'))  # Change attribute in rectangle [xterm only]
DECCRARA = (CSI + '{};{};{};{};{}$t', ('top', 'left', 'bottom', 'right', 'attribute'))  # Reverse attribute in rectangle [xterm only]
DECFRA = (CSI + '{};{};{};{};{}$x', ('character', 'top', 'left', 'bottom', 'right'))  # Fill rectangle with character [xterm only]
DECERA = (CSI + '{};{};{};{}$z', ('top', 'left', 'bottom', 'right'))  # Erase rectangle with character [xterm only]

# VT420 and up

DECBI = ESC + '6'  # Back index
DECFI = ESC + '9'  # Forward index


# CSI functions

CHA = (CSI + '{}G', ('value',))  # Move cursor to specified column
SU = (CSI + '{}S', ('value',))  # Scroll up Ps line(s)
SD = (CSI + '{}T', ('value',))  # Scroll down Ps line(s)

ICH = (CSI + '{}@', ('value',))  # Insert Ps blank characters
NLD = (CSI + '{}E', ('value',))  # Move cursor down Ps line(s) and to the first column
NLU = (CSI + '{}F', ('value',))  # Move cursor up Ps line(s) and to the first column

IL = (CSI + '{}L', ('value',))  # Insert Ps Line(s)
DL = (CSI + '{}M', ('value',))  # Delete Ps Line(s)
DCH = (CSI + '{}P', ('value',))  # Delete Ps Character(s)
ECH = (CSI + '{}X', ('value',))  # Erase Ps Character(s)

TABBACK = (CSI + '{}Z', ('value',))  # Move tab stops backward
TABFORWARD = (CSI + '{}I', ('value',))  # Move tab stops backward

HPR = (CSI + '{}a', ('value',))  # Move character position [relative]
HPA = (CSI + '{}`', ('value',))  # Move character position [absolute]

VPR = (CSI + '{}e', ('value',))  # Move cursor to line [relative]
VPA = (CSI + '{}d', ('value',))  # Move cursor to line [absolute]

SAVEDEC = (CSI + '?{}s', ('value',))  # Save DEC private mode value
RESETDEC = (CSI + '?{}r', ('value',))  # Save DEC private mode value

DECPEX_set   = CSI + '?19h'  # Set print extent to full screen
DECPEX_reset = CSI + '?19l'  # Limit print to scrolling area
DECTECEM_set   = CSI + '?25h'  # Show cursor
DECTECEM_reset = CSI + '?25l'  # Hide cursor
SCROLLBAR_set   = CSI + '?30h'  # Show scrollbar
SCROLLBAR_reset = CSI + '?30l'  # Hide scrollbar
DECLRMM_set   = CSI + '?69h'  # Enable left and right margin mode
DECLRMM_reset = CSI + '?69l'  # Disable left and right margin mode

ALTBUFF_set   = CSI + '?1047h'  # Use alternative screen buffer
ALTBUFF_reset = CSI + '?1047l'  # Use regular screen buffer

ALTBUFF_set   = CSI + '?1049h'  # Use alternative screen buffer, store cursor first
ALTBUFF_reset = CSI + '?1049l'  # Use regular screen buffer, then reset cursor

SGR1_unset = CSI + '22m'  # Turn bold mode on
SGR4_unset = CSI + '24m'  # Turn underline mode on
SGR5_unset = CSI + '25m'  # Turn blinking mode on
SGR7_unset = CSI + '27m'  # Turn reverse video on
SGR8_unset = CSI + '28m'  # Turn invisible text mode on

DECSCUSR_blink_block = CSI + '0 q'  # Set cursor to a blinking block
DECSCUSR_steady_block = CSI + '2 q'  # Set cursor to a steady block
DECSCUSR_blink_line = CSI + '3 q'  # Set cursor to blinking underline
DECSCUSR_steady_line = CSI + '4 q'  # Set cursor to steady underline
DECSCUSR_blink_bar = CSI + '5 q'  # Set cursor to blinking vertical bar (xterm only)
DECSCUSR_steady_bar = CSI + '6 q'  # Set cursor to steady vertical bar (xterm only)

DECSLRM = (CSI + '{};{}s', ('left', 'right'))  # Set left and right margins

