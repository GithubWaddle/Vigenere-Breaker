# breaking a vigenere cipher without knowing the key

from flask import current_app
from .vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from .index_of_coincidence import find_most_likely_vigenere_key_length, divide_ciphertext_into_groups
import re
import itertools
import string

from langid.langid import LanguageIdentifier, model

MAXIMUM_BRUTE_FORCE_KEY_LENGTH: int = 4
WORDS_FILE_PATH: str = "./static/WORDS.txt"

breaking_tracking = {
  "breaking_progress_percentage": {
	"numerator": 0,
	"denominator": 0,
  },
  "possible_key_plaintexts": [],
  "is_breaking": 0,
}
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)


def set_breaking_progress_percentage_numerator(numerator: bool) -> None:
	global breaking_tracking
	breaking_tracking["breaking_progress_percentage"]["denominator"] = numerator


def set_breaking_progress_percentage_denominator(denominator: bool) -> None:
	global breaking_tracking
	breaking_tracking["breaking_progress_percentage"]["denominator"] = denominator


def set_possible_key_plaintexts(value: list[dict[str, str]]) -> None:
	global breaking_tracking
	breaking_tracking["possible_key_plaintexts"] = value


def append_to_possible_key_plaintexts(plaintext: str, key: str) -> None:
	global breaking_tracking
	breaking_tracking["possible_key_plaintexts"].append({
		"plaintext": plaintext, 
		"key": key
	})


def set_is_breaking(is_breaking: bool)-> None:
	global breaking_tracking
	breaking_tracking["is_breaking"] = is_breaking


def normalize_uppercase_text(text):
    text = text.lower()

    def capitalize_sentence(match):
        return match.group(1) + match.group(2).upper()

    normalized = re.sub(r'(^\s*|[.!?]\s+)([a-z])', capitalize_sentence, text)

    return normalized


def is_probably_english(text):
	language, confidence = identifier.classify(normalize_uppercase_text(text))
	if confidence > 0.9999999:
		return True
	return False


def vigenere_start_breaking(ciphertext: str, is_key_english_word: bool) -> None:
	set_is_breaking(True)
	set_possible_key_plaintexts([])
	set_breaking_progress_percentage_numerator(0)
	set_breaking_progress_percentage_denominator(0)
	
	if is_key_english_word:
		break_cipher_dictionary_attack(ciphertext)
		return

	if len(ciphertext) < 25:
		break_cipher_brute_force_attack(ciphertext)
		return

	key_length = find_most_likely_vigenere_key_length(ciphertext)
	break_cipher_statistical_attack(ciphertext, key_length)


def vigenere_stop_breaking() -> None:
	set_is_breaking(False)


def break_cipher_brute_force_attack(ciphertext: str, maximum_key_length: int = MAXIMUM_BRUTE_FORCE_KEY_LENGTH) -> None:
	set_breaking_progress_percentage_denominator(26 ** key_length)
	index = 0

	for key_length in range(maximum_key_length + 1):
		for key_chars in itertools.permutations(string.ascii_uppercase, key_length):
			index += 1
			set_breaking_progress_percentage_numerator(index)

			if not breaking_tracking["is_breaking"]:
				return

			key = ''.join(key_chars)
			decrypted_text = vigenere_decrypt(ciphertext, key)
			if not is_probably_english(possible_plaintext):
				continue
			
			append_to_possible_key_plaintexts(possible_plaintext, key)


def break_cipher_dictionary_attack(ciphertext: str) -> None:
	words = []
	print(current_app.root_path)
	with open(current_app.root_path + "/" + WORDS_FILE_PATH, 'r') as words_file:
		words = words_file.readlines()
	words_amount = len(words)
	current_word_index = 0
	global breaking_tracking
	set_breaking_progress_percentage_denominator(words_amount)

	for word in words:
		current_word_index += 1
		set_breaking_progress_percentage_numerator(current_word_index)
		if not breaking_tracking["is_breaking"]:
			return
		word = word.strip()
		possible_plaintext: str = vigenere_decrypt(ciphertext, word)
		if not is_probably_english(possible_plaintext):
			continue

		append_to_possible_key_plaintexts(possible_plaintext, word)


def break_cipher_statistical_attack(ciphertext: str, key_length: int) -> None:
	caesar_shifted_groups = divide_ciphertext_into_groups(ciphertext, key_length)
	
