from flask import Flask, render_template, request, jsonify
from vigenere_cipher import vigenere_encrypt, vigenere_decrypt
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        plain_text = request.form['plaintext']
        key = request.form.get('key')

        if not key:
            result, key = vigenere_encrypt(plain_text)
        else:
            result, _ = vigenere_encrypt(plain_text, key)

        return jsonify(result=result, key=key)

    elif request.method == 'GET':
        text = request.args.get('text')
        key = request.args.get('key')
        response_type = request.args.get('type', 'json')

        if not text:
            return jsonify(error="Text is required"), 400

        if not key:
            result, key = vigenere_encrypt(text)
        else:
            result, _ = vigenere_encrypt(text, key)

        if response_type == "json":
            return jsonify(result=result, key=key)
        else:
            return result

@app.route('/decrypt', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        encrypted_text = request.form['encryptedText']
        key = request.form['key']
        if not key:
            return jsonify(error="Key is required"), 400
        result = vigenere_decrypt(encrypted_text, key)
        return jsonify(result=result)

    elif request.method == 'GET':
        text = request.args.get('text')
        key = request.args.get('key')
        response_type = request.args.get('type', 'json')

        if not text or not key:
            return jsonify(error="Both text and key are required"), 400

        result = vigenere_decrypt(text, key)

        if response_type == "json":
            return jsonify(result=result)
        else:
            return result