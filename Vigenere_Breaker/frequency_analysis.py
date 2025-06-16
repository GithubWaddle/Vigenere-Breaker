from typing import Dict, List, Tuple

english_letter_frequencies: Dict[str, float] = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.29, 'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.10, 'Z': 0.07
}

most_common_letter_order: str = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
uppercase_alphabet: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def get_letter_counts(message: str) -> Dict[str, int]:
    letter_counts: Dict[str, int] = {letter: 0 for letter in uppercase_alphabet}
    for character in message.upper():
        if character in uppercase_alphabet:
            letter_counts[character] += 1
    return letter_counts


def get_first_element_of_tuple(tuple_value: Tuple[int, str]) -> int:
    return tuple_value[0]


def get_letter_frequency_order(message: str) -> str:
    letter_frequencies: Dict[str, int] = get_letter_counts(message)
    frequency_to_letters: Dict[int, str] = {}

    for letter in uppercase_alphabet:
        frequency = letter_frequencies[letter]
        if frequency not in frequency_to_letters:
            frequency_to_letters[frequency] = [letter]
        else:
            frequency_to_letters[frequency].append(letter)

    for frequency in frequency_to_letters:
        frequency_to_letters[frequency].sort(
            key=most_common_letter_order.find,
            reverse=True
        )
        frequency_to_letters[frequency] = ''.join(frequency_to_letters[frequency])

    frequency_pairs: List[Tuple[int, str]] = list(frequency_to_letters.items())
    frequency_pairs.sort(key=get_first_element_of_tuple, reverse=True)

    frequency_ordered_letters: List[str] = [pair[1] for pair in frequency_pairs]
    return ''.join(frequency_ordered_letters)


def get_english_frequency_match_score(message: str) -> int:
    message_letter_order: str = get_letter_frequency_order(message)
    match_score: int = 0

    for common_letter in most_common_letter_order[:6]:
        if common_letter in message_letter_order[:6]:
            match_score += 1

    for uncommon_letter in most_common_letter_order[-6:]:
        if uncommon_letter in message_letter_order[-6:]:
            match_score += 1

    return match_score
