import string
from sys import maxsize
from typing import List, Dict
from .frequency_analysis import get_letter_counts

EN_IC = 0.67

def calculate_index_of_coincidence(letter_frequencies: Dict[str, int]) -> float:
    numerator: int = sum([
        letter_frequencies[letter] * (letter_frequencies[letter] - 1)
        for letter in string.ascii_uppercase
    ])
    total_letters: int = sum(letter_frequencies.values())
    denominator: int = total_letters * (total_letters - 1)
    return numerator / denominator if denominator != 0 else 0


def get_blocks(text, size):
    blocks = [text[i:i+size] for i in range(0, len(text)-size, size)]
    return blocks


def get_columns(text_blocks):
    group_size = len(text_blocks[0])
    columns = []
    for letter_count in range(group_size):
        column = ''
        for group_count in range(len(text_blocks)):
            column += text_blocks[group_count][letter_count]
        columns.append(column)
    return columns


def find_likely_key_length(ciphertext: str, maximum_key_length: int) -> int:
    minimum_difference_from_english_ic: float = maxsize
    most_likely_key_length: int = 0

    for candidate_key_length in range(1, maximum_key_length + 1):
        character_blocks: List[str] = get_blocks(ciphertext, candidate_key_length)
        transposed_columns: List[str] = get_columns(character_blocks)

        column_index_of_coincidences: List[float] = [
            calculate_index_of_coincidence(
                get_letter_counts(column)
            )
            for column in transposed_columns
        ]

        average_index_of_coincidence: float = sum(column_index_of_coincidences) / len(column_index_of_coincidences)
        difference_from_expected_ic: float = abs(EN_IC - average_index_of_coincidence)

        if difference_from_expected_ic < minimum_difference_from_english_ic:
            minimum_difference_from_english_ic = difference_from_expected_ic
            most_likely_key_length = candidate_key_length

        print('KEY_LENGTH: ' + str(candidate_key_length) + '\n')
        print('Index of Coincidence by column: ' + str(column_index_of_coincidences))
        print('Average Index of Coincidence: ' + str(average_index_of_coincidence) + '\n')

    return most_likely_key_length


def main():
    # Replace this with a real ciphertext encrypted using a Vigenère cipher
    ciphertext = (
        "JLBVRBBNNNNSUHRYNRFSBAJETOZELAZ"
    )

    max_key_length = 10
    likely_key_length = find_likely_key_length(ciphertext, max_key_length)
    print(f"Most likely key length: {likely_key_length}")


if __name__ == "__main__":
    main()
