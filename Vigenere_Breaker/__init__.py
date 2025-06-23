from flask import Flask, render_template, request, jsonify
from .vigenere_cipher_breaker import breaking_tracking, vigenere_start_breaking, vigenere_stop_breaking

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
	vigenere_stop_breaking()
	return render_template("index.html")


@app.route("/startBreaking", methods=["POST"])
def start_breaking():
	data = request.get_json();
	ciphertext = data.get("ciphertext")
	isKeyEnglishWord = data.get("isKeyEnglishWord")
	vigenere_start_breaking(ciphertext, isKeyEnglishWord)
	return jsonify({})


@app.route("/breakingProgress", methods=["GET"])
def get_breaking_progress():
	global breaking_tracking
	return jsonify({
		"progress": breaking_tracking["breaking_progress_percentage"],
		"possibleKeyPlaintexts": breaking_tracking["possible_key_plaintexts"]
		})


@app.route("/foundPlaintext", methods=["POST"])
def on_found_plaintext():
	vigenere_stop_breaking()
	return jsonify({})
