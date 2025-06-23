from flask import current_app
from .vigenere_cipher import clean_text
from collections import Counter
from math import log10

TRIGRAM_FILE_PATH: str = "static/english_trigrams.txt"

class NGramScore:
    def __init__(self, ngram_file, sep=' '):
        self.ngrams = {}

        with open(current_app.root_path + "/" + ngram_file, 'r') as f:
            for line in f:
                key, count = line.strip().split(sep)
                self.ngrams[key] = int(count)

        self.N = sum(self.ngrams.values())
        self.L = len(next(iter(self.ngrams)))

        for key in self.ngrams:
            self.ngrams[key] = log10(self.ngrams[key] / self.N)

        self.floor = log10(0.01 / self.N)

    def score(self, text):
        score = 0.0
        for i in range(len(text) - self.L + 1):
            ngram = text[i:i + self.L]
            score += self.ngrams.get(ngram, self.floor)
        return score


class NBest:
    def __init__(self, N=1000):
        self.N = N
        self.store = []

    def add(self, item):
        self.store.append(item)
        self.store.sort(reverse=True)
        self.store = self.store[:self.N]

    def __getitem__(self, index):
        return self.store[index]

    def __len__(self):
        return len(self.store)


#ENGLISH_LETTER_FREQUENCIES: dict[str, float] = {
#    'E': 0.127, 'T': 0.091, 'A': 0.082, 'O': 0.075, 'I': 0.07, 'N': 0.067,
#    'S': 0.063, 'H': 0.061, 'R': 0.06, 'D': 0.043, 'L': 0.04, 'C': 0.028,
#    'U': 0.028, 'M': 0.024, 'W': 0.024, 'F': 0.022, 'G': 0.02, 'Y': 0.02,
#    'P': 0.019, 'B': 0.015, 'V': 0.0098, 'K': 0.0077, 'J': 0.0015, 'X': 0.0015,
#    'Q': 0.0095, 'Z': 0.00074
#}


#def get_chi_squared_error_score(text: str) -> float:
#	cleaned_text = clean_text(text)
#	text_length: int = len(cleaned_text)
#
#	text_letter_frequency: dict[str, int] = Counter(cleaned_text)
#	expected_letter_frequency: dict[str, int] = {
#		letter: (decimal * text_length)
#		for letter, decimal in ENGLISH_LETTER_FREQUENCIES.items()
#	}
#
#	normalized_squared_letter_frequency_difference: dict[str, float] = {}
#	for letter in expected_letter_frequency:
#		difference = text_letter_frequency.get(letter, 0) - expected_letter_frequency[letter]
#		squared_difference = difference ** 2
#		normalized_squared_difference = squared_difference / expected_letter_frequency[letter]
#		normalized_squared_letter_frequency_difference[letter] = normalized_squared_difference
#
#	return sum(normalized_squared_letter_frequency_difference.values())
