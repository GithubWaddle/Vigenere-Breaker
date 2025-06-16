from flask import Flask, render_template, request, jsonify
from .vigenere_cipher import vigenere_encrypt, vigenere_decrypt

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		data = request.get_json();
		print(data)
		return jsonify("index.html", {
			"response": "Totally decrypted text!",
			"plaintext": vigenere_decrypt(data.get("ciphertext"), "BANANA"),
		})

	return render_template("index.html")
