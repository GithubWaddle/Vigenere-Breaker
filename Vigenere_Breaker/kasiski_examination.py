from math import sqrt
from typing import Dict, List, Tuple


def find_repeated_sequence_positions(text: str, sequence_length: int) -> List[Tuple[str, List[int]]]:
    sequence_positions: Dict[str, List[int]] = {}
    for index, character in enumerate(text):
        next_sequence = text[index:index + sequence_length]
        if next_sequence in sequence_positions:
            sequence_positions[next_sequence].append(index)
        else:
            sequence_positions[next_sequence] = [index]
    repeated_sequences = list(filter(lambda sequence: len(sequence_positions[sequence]) >= 2, sequence_positions))
    repeated_sequence_positions: List[Tuple[str, List[int]]] = [
        (sequence, sequence_positions[sequence]) for sequence in repeated_sequences
    ]
    return repeated_sequence_positions


def get_position_spacings(positions: List[int]) -> List[int]:
    return [positions[index + 1] - positions[index] for index in range(len(positions) - 1)]


def get_factors_of_number(number: int) -> List[int]:
    factors: set[int] = set()
    for divisor in range(1, int(sqrt(number)) + 1):
        if number % divisor == 0:
            factors.add(divisor)
            factors.add(number // divisor)
    return sorted(factors)


def find_candidate_key_lengths(
    list_of_factor_lists: List[List[int]],
    maximum_key_length: int
) -> List[int]:
    all_factors_flat = [
        list_of_factor_lists[list_index][factor_index]
        for list_index in range(len(list_of_factor_lists))
        for factor_index in range(len(list_of_factor_lists[list_index]))
    ]
    filtered_candidate_lengths = list(filter(lambda factor: factor <= maximum_key_length, all_factors_flat))
    sorted_candidate_lengths = sorted(
        set(filtered_candidate_lengths),
        key=lambda factor: all_factors_flat.count(factor),
        reverse=True
    )
    return sorted_candidate_lengths


def find_key_length(ciphertext: str, sequence_length: int, maximum_key_length: int) -> int:
    repeated_sequence_positions = find_repeated_sequence_positions(ciphertext, sequence_length)
    sequence_spacings: Dict[str, List[int]] = {
        sequence: get_position_spacings(positions) for sequence, positions in repeated_sequence_positions
    }

    list_of_factor_lists: List[List[int]] = []
    for spacings in sequence_spacings.values():
        for spacing in spacings:
            list_of_factor_lists.append(get_factors_of_number(spacing))

    candidate_key_lengths = find_candidate_key_lengths(list_of_factor_lists, maximum_key_length)
    likely_key_length: int = candidate_key_lengths[0]
    return likely_key_length
