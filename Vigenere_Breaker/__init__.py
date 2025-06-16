from flask import Flask, render_template, request, jsonify
from .index_of_coincidence import find_likely_key_length
from .vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from .vigenere_cipher_breaker import vigenere_break
from .brute_force_attack import break_vigenere_cipher_brute_force_attack
from .dictionary_attack import break_vigenere_cipher_dictionary_attack

MAXIMUM_KEY_LENGTH = 20

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		data = request.get_json();
		ciphertext = data.get("ciphertext")
		isKeyEnglishWord = data.get("isKeyEnglishWord")

		if isKeyEnglishWord == "on":
			return dictionary_attack(ciphertext)

		key_length = find_likely_key_length(MAXIMUM_KEY_LENGTH)
		if key_length < 5:
			return brute_force_attack(ciphertext, key_length)
		
		return jsonify("index.html", {
			"response": "Totally decrypted text!",
			"plaintext": vigenere_decrypt(data.get("ciphertext"), "BANANA"),
			"isKeyEnglishWord": data.get("isKeyEnglishWord"),
		})

	return render_template("index.html")


def dictionary_attack(ciphertext):
	possible_plaintexts = break_cipher_dictionary_attack(ciphertext)
	return jsonify("index.html", {
		"possible_plaintexts": possible_plaintexts
	})


def brute_force_attack(ciphertext, key_length):
	possible_plaintexts = break_cipher_dictionary_attack(ciphertext, key_length)
	return jsonify("index.html", {
		"possible_plaintexts": possible_plaintexts
	})


def statistical_attack(ciphertext, key_length):
	pass
