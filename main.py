import os
import string
from evdev import InputDevice, categorize, ecodes

from play_sound import PlaySound

dev = InputDevice('/dev/input/event4')


def play(letter):
    print(letter)
    PlaySound(os.getcwd() + f'/sounds/{letter}.wav', "1").start()


ACCENTS = {
    "a": "ą",
    "c": "ć",
    "e": "ę",
    "l": "ł",
    "n": "ń",
    "o": "ó",
    "s": "ś",
    "x": "ź",
    "z": "ż",
}

LETTERS_CODES = [getattr(ecodes, f'KEY_{letter}') for letter in string.ascii_uppercase]

for event in dev.read_loop():
    active_keys = dev.active_keys()
    if event.type == ecodes.EV_KEY:
        c_event = categorize(event)

        if c_event.keystate == c_event.key_down:
            if c_event.scancode not in LETTERS_CODES:
                continue

            letter = c_event.keycode[-1].lower()
            if ecodes.KEY_RIGHTALT in active_keys:
                try:
                    play(ACCENTS[letter])
                except KeyError:
                    pass
            else:
                play(letter)
