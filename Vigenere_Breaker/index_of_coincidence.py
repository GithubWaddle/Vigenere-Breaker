from collections import Counter
from typing import Union
from .vigenere_cipher import clean_text

DEFAULT_MAXIMUM_KEY_LENGTH = 20
ENGLISH_LANGUAGE_INDEX_OF_COINCIDENCE = 0.067

def calculate_index_of_coincidence(text: Union[str, bytes]) -> float:
	if isinstance(text, bytes):
		text = text.decode('utf-8')
	cleaned_text = clean_text(text)

	if len(cleaned_text) <= 1:
		return 0.0

	letter_frequencies = Counter(cleaned_text)
	total_characters = len(cleaned_text)
	total_possible_pairs = total_characters * (total_characters - 1)

	matching_character_pairs = sum(
		frequency * (frequency - 1) for frequency in letter_frequencies.values()
	)

	return matching_character_pairs / total_possible_pairs if total_possible_pairs > 0 else 0.0


def divide_ciphertext_into_groups(ciphertext: str, key_length: int) -> list[str]:
	groups = ['' for _ in range(key_length)]
	for index, character in enumerate(ciphertext):
		group_index = index % key_length
		groups[group_index] += character
	return groups


def find_most_likely_vigenere_key_length(ciphertext: str, maximum_key_length: int = DEFAULT_MAXIMUM_KEY_LENGTH) -> int:
	cleaned_ciphertext = clean_text(ciphertext)
	most_likely_key_length = 0
	smallest_index_difference = float('inf')

	for candidate_key_length in range(1, maximum_key_length + 1):
		caesar_shifted_groups = divide_ciphertext_into_groups(cleaned_ciphertext, candidate_key_length)
		group_indexes_of_coincidence = [
			calculate_index_of_coincidence(group) for group in caesar_shifted_groups
		]

		average_index_of_coincidence = sum(group_indexes_of_coincidence) / len(group_indexes_of_coincidence)
		difference_from_english_ic = abs(ENGLISH_LANGUAGE_INDEX_OF_COINCIDENCE - average_index_of_coincidence)

		print(candidate_key_length, average_index_of_coincidence)
		if difference_from_english_ic < smallest_index_difference:
			smallest_index_difference = difference_from_english_ic
			most_likely_key_length = candidate_key_length

	return most_likely_key_length
