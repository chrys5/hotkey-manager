# USER-DEFINED KEYBOARD HOTKEYS
import keyboard

HOTKEYS = [
    ('alt+=', lambda: keyboard.write('-')),
    ('alt+shift+=', lambda: keyboard.write('_')),
    ('alt+9', lambda: keyboard.write('0')),
    ('alt+shift+9', lambda: keyboard.write(')')),
]