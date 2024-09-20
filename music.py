from typing import Iterable
from math import log2, gcd
from fractions import Fraction
import itertools as it


def get_harmonic(i: int) -> float:
    return log2(i / (i - 1))

fifth = get_harmonic(3)


def iterate_notes() -> Iterable[int]:
    """ Warning: infinite iterator! """
    yield 0
    for i in it.count(start=1):
        yield i
        yield -i

def get_first_n_notes(n: int) -> Iterable[int]:
    return it.islice(iterate_notes(), n)


def get_note_name(note: int) -> str:
    name = 'FCGDAEB'[(note + 3) % 7]
    acc = (note + 3) // 7
    single, double = ('♯', '𝄪') if acc > 0 else ('♭', '𝄫')
    return name + double * (abs(acc) // 2) + single * (abs(acc) % 2)


class Edo:
    def __init__(self, number: int):
        self.number = number
        
        numerator_range = range((number + 1) // 2, number)
        numerator_candidates = (i for i in numerator_range if gcd(number, i) == 1)
        def distance(i: int) -> float:
            return abs(i / number - fifth)
        numerator = min(numerator_candidates, key=distance, default=1)
        self.fraction = Fraction(numerator, number)
        
        notes = get_first_n_notes(number)
        def note_x(note: int) -> Fraction:
            return self.fraction * note % 1
        self.notes = sorted(notes, key=note_x)
