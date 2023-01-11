from pynput.keyboard import Key, Controller
from random import randint
from time import sleep
import string
import random
import mouse


def windows_leiste():
# Drückt Buttons auf der Tastatur

    key = Controller()

# win taste drücken
    key.tap(Key.cmd)
    sleep(1)
    letters = string.ascii_lowercase

# zufällige Buchstaben: 5 Stück
    for i in range(5):
        let = ''.join(random.choice(letters))
        key.press(let)
        key.release(let)
    sleep(0.2)
    key.press(Key.enter)
    key.release(Key.enter)

    sleep(3)

# alt + f4
    key.press(Key.alt_l)
    key.press(Key.f4)
    sleep(2)
    key.release(Key.alt_l)
    key.release(Key.f4)


def random_klicks():
# Maus wird zufällig bewegt und geklickt

    rep = randint(1, 5)

    # Schleife mit 1-5 Wiederholungen
    for i in range(rep):
        # Maus wird in zufällige richtung bewegt und es wird ein mal 'gelinkst klickt'
        mouse.move(randint(-1000, 1000), randint(-1000, 1000), absolute=False, duration=0.2)
        sleep(randint(0, 1) / 10)
        mouse.click('left')

def randomizer_windows():
    a = randint(1,2)
    if a == 1:
        windows_Leiste()
        
    if a == 2:
        random_Klicks()
        
