import string
from .vigenere_cipher import vigenere_decrypt
from langid.langid import LanguageIdentifier, model

WORDS_FILE_PATH: str = "./static/words.txt"
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def break_vigenere_cipher_dictionary_attack(ciphertext: str):
	words = []
	with open(WORDS_FILE_PATH, 'r') as words_file:
		words = words_file.readlines()

	possible_plaintexts = []
	for word in words:
		word = word.strip()
		possible_plaintext: str = decode(ciphertext, word)
		language, confidence = identifier.classify(possible_plaintext)
		if not (language == "en" and confidence > 0.9999999):
			continue

		possible_plaintexts.append({
			"key": word,
			"possible_plaintext": possible_plaintext
		})

	return possible_plaintexts
