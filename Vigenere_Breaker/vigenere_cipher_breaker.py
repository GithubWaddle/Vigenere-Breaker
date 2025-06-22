# breaking a vigenere cipher without knowing the key

from flask import current_app
from .vigenere_cipher import vigenere_encrypt, vigenere_decrypt, clean_text
from .index_of_coincidence import find_most_likely_vigenere_key_length, divide_ciphertext_into_groups
from .frequency_analysis import get_chi_squared_error_test
import re
import itertools
import string
import sys

from langid.langid import LanguageIdentifier, model

MAXIMUM_BRUTE_FORCE_KEY_LENGTH: int = 4
MINIMUM_CIPHERTEXT_LENGTH_FOR_STATISTICAL_ATTACK: int = 50
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
	breaking_tracking["breaking_progress_percentage"]["numerator"] = numerator


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
		print("Dictionary Attack!")
		break_cipher_dictionary_attack(ciphertext)
		return

	if len(ciphertext) < MINIMUM_CIPHERTEXT_LENGTH_FOR_STATISTICAL_ATTACK:
		print("Brute-Force Attack!")
		break_cipher_brute_force_attack(ciphertext)
		return

	key_length = 4#find_most_likely_vigenere_key_length(ciphertext)
	print("Statistical Attack!")
	print("Key Length: ", key_length)
	break_cipher_statistical_attack(ciphertext, key_length)


def vigenere_stop_breaking() -> None:
	set_is_breaking(False)


def break_cipher_brute_force_attack(ciphertext: str, maximum_key_length: int = MAXIMUM_BRUTE_FORCE_KEY_LENGTH) -> None:
	set_breaking_progress_percentage_denominator(26 ** maximum_key_length)
	index = 0

	for key_length in range(maximum_key_length + 1):
		for key_chars in itertools.permutations(string.ascii_uppercase, key_length):
			index += 1
			set_breaking_progress_percentage_numerator(index)

			if not breaking_tracking["is_breaking"]:
				return

			key = ''.join(key_chars)
			decrypted_text = vigenere_decrypt(ciphertext, key)
			if not is_probably_english(decrypted_text):
				continue
			
			append_to_possible_key_plaintexts(decrypted_text, key)


def break_cipher_dictionary_attack(ciphertext: str) -> None:
	words = []
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
	def caesar_encrypt(text: str, text_shift: int) -> str:
		encrypted_text = ""

		for char in text:
			if char.isalpha():
				base = ord('A') if char.isupper() else ord('a')
				shifted = (ord(char) - base + text_shift) % 26 + base
				encrypted_text += chr(shifted)
			else:
				encrypted_text += char

		return encrypted_text

	clean_ciphertext: str = clean_text(ciphertext)
	caesar_shifted_groups: list[str] = divide_ciphertext_into_groups(clean_ciphertext, key_length)
	set_breaking_progress_percentage_numerator(0)
	set_breaking_progress_percentage_denominator(1)

	key_letter: list[str] = []

	for caesar_group in caesar_shifted_groups:
		print("CAESAR GROUP: ", caesar_group)
		possible_key: str = "A"
		lowest_chi_squared_error_test_value: float = sys.float_info.max
		for letter in string.ascii_uppercase:
			chi_squared_error_test_value: float = get_chi_squared_error_test(caesar_encrypt(caesar_group, ord(letter) - ord("A")))
			print(letter, chi_squared_error_test_value)
			if not chi_squared_error_test_value < lowest_chi_squared_error_test_value:
				continue
			lowest_chi_squared_error_test_value = chi_squared_error_test_value
			possible_key = letter
		
		key_letter.append(possible_key)


	set_breaking_progress_percentage_numerator(1)
	key = ''.join(key_letter)
	append_to_possible_key_plaintexts(vigenere_decrypt(ciphertext, key), key)
