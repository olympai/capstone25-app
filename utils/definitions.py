import string
import random

def zufallskombination(k=10):
    # Buchstaben a-z als Pool für die zufällige Auswahl
    buchstaben_pool = string.ascii_lowercase
    # Zufällige Auswahl von zehn Buchstaben aus dem Pool
    zufalls_kombination = ''.join(random.choices(buchstaben_pool, k=k))
    return zufalls_kombination

def zufall_extended(k=10):
    # Buchstaben a-z, A-Z und Zahlen 0-9 als Pool für die zufällige Auswahl
    buchstaben_pool = string.ascii_letters + string.digits
    # Zufällige Auswahl von zehn Buchstaben aus dem Pool
    zufalls_kombination = ''.join(random.choices(buchstaben_pool, k=k))
    return zufalls_kombination
