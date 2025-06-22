from .vigenere_cipher import clean_text
from collections import Counter
from typing import Dict, List, Tuple

ENGLISH_LETTER_FREQUENCIES: Dict[str, float] = {
	'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
	'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
	'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
	'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
	'Q': 0.10, 'Z': 0.07
}

most_common_letter_order: str = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
uppercase_alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_chi_squared_error_test(text: str) -> None:
	cleaned_text = clean_text(text)
	text_length: int = len(cleaned_text)
	text_letter_frequency: dict[str, int] = Counter(cleaned_text)
	print(text_length)
	print(text_letter_frequency)
	expected_letter_frequency = {
		letter: ((percent / 100) * text_length)
		for letter, percent in ENGLISH_LETTER_FREQUENCIES.items()
	}
	print(expected_letter_frequency)
	print(sum(expected_letter_frequency.values()))
	normalized_squared_letter_frequency_difference: dict[str, int] = {
		letter: (
			((text_letter_frequency[letter] - expected_letter_frequency[letter]) ** 2) 
			/ expected_letter_frequency[letter])
		for letter, percent in expected_letter_frequency.items()
	}

	return sum(normalized_squared_letter_frequency_difference.values())

