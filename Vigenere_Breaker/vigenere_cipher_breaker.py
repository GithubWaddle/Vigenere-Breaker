# breaking a vigenere cipher without knowing the key

def get_likely_key_length(ciphertext: str):
	pass


def break_cipher_brute_force_attack(ciphertext: str) -> str:
	pass


def vigenere_break(ciphertext: str, is_key_english_word: bool) -> str:
	plaintext: str = ""

	if is_key_english_word:
		plaintext = break_cipher_dictionary_attack(ciphertext)

	return plaintext

