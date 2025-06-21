# breaking a vigenere cipher without knowing the key

from flask import current_app
from .vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from .index_of_coincidence import find_most_likely_vigenere_key_length
import re
import itertools
import string

from langid.langid import LanguageIdentifier, model

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
	global breaking_tracking
	breaking_tracking["is_breaking"] = True
	breaking_tracking["possible_key_plaintexts"] = []
	breaking_tracking["breaking_progress_percentage"]["numerator"] = 0
	breaking_tracking["breaking_progress_percentage"]["denominator"] = 0
	
	if is_key_english_word:
		break_cipher_dictionary_attack(ciphertext)
		return

	key_length = find_most_likely_vigenere_key_length(ciphertext)
	if key_length < 5:
		break_cipher_brute_force_attack(ciphertext, key_length)
		return

	break_cipher_statistical_attack(ciphertext, key_length)


def vigenere_stop_breaking() -> None:
	global breaking_tracking
	breaking_tracking["is_breaking"] = False


def append_to_possible_key_plaintexts(key, plaintext) -> None:
	global breaking_tracking
	breaking_tracking["possible_key_plaintexts"].append({
		"key": key,
		"plaintext": plaintext
	});


def break_cipher_brute_force_attack(ciphertext: str, key_length: int) -> None:
	possible_results = []

	for key_chars in itertools.product(string.ascii_uppercase, repeat=key_length):
		if not breaking_tracking["is_breaking"]:
			return

		key = ''.join(key_chars)
		decrypted_text = vigenere_decrypt(ciphertext, key)
		if not is_probably_english(possible_plaintext):
			continue
		
		append_to_possible_key_plaintexts(word, possible_plaintext)


def break_cipher_dictionary_attack(ciphertext: str) -> None:
	words = []
	print(current_app.root_path)
	with open(current_app.root_path + "/" + WORDS_FILE_PATH, 'r') as words_file:
		words = words_file.readlines()
	words_amount = len(words)
	current_word_index = 0
	global breaking_tracking
	breaking_tracking["breaking_progress_percentage"]["denominator"] = words_amount

	for word in words:
		current_word_index += 1
		breaking_tracking["breaking_progress_percentage"]["numerator"] = current_word_index
		if not breaking_tracking["is_breaking"]:
			return
		word = word.strip()
		possible_plaintext: str = vigenere_decrypt(ciphertext, word)
		if not is_probably_english(possible_plaintext):
			continue

		append_to_possible_key_plaintexts(word, possible_plaintext)


def break_cipher_statistical_attack(ciphertext: str) -> None:
	pass