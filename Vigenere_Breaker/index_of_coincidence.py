import string
from sys import maxsize
from typing import List, Dict
from .frequency_analysis import get_letter_counts

EN_IC = 0.67

import re

def get_capital_letters(text):
	return re.sub(r'[^A-Z]', '', text)


def calculate_index_of_coincidence(letter_frequencies: Dict[str, int]) -> float:
	numerator: int = sum([
		letter_frequencies[letter] * (letter_frequencies[letter] - 1)
		for letter in string.ascii_uppercase
	])
	total_letters: int = sum(letter_frequencies.values())
	denominator: int = total_letters * (total_letters - 1)
	return numerator / denominator if denominator != 0 else 0


def get_keyed_groups(text, key_size):
	groups = [text[i:i+key_size] for i in range(0, len(text)-key_size, key_size)]
	return groups


def get_columns(text_groups):
	group_size = len(text_groups[0])
	columns = []
	for letter_count in range(group_size):
		column = ''
		for group_count in range(len(text_groups)):
			column += text_groups[group_count][letter_count]
		columns.append(column)
	return columns


def find_likely_key_length(ciphertext: str, maximum_key_length: int) -> int:
	if maximum_key_length == 0:
		maximum_key_length = len(ciphertext)
	
	cleaned_ciphertext = get_capital_letters(ciphertext)
	minimum_difference_from_english_ic: float = maxsize
	most_likely_key_length: int = 0

	for candidate_key_length in range(1, maximum_key_length + 1):
		keyed_groups: List[str] = get_keyed_groups(cleaned_ciphertext, candidate_key_length)
		transposed_columns: List[str] = get_columns(keyed_groups)

		column_index_of_coincidences: List[float] = [
			calculate_index_of_coincidence(
				get_letter_counts(column)
			)
			for column in transposed_columns
		]

		average_index_of_coincidence: float = sum(column_index_of_coincidences) / len(column_index_of_coincidences)
		difference_from_expected_index_of_coincidence: float = abs(EN_IC - average_index_of_coincidence)

		if not difference_from_expected_index_of_coincidence < minimum_difference_from_english_ic:
			continue

		minimum_difference_from_english_ic = difference_from_expected_index_of_coincidence
		most_likely_key_length = candidate_key_length

	return most_likely_key_length

