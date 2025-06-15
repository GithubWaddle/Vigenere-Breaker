from flask import Flask, render_template, request
from vigenere_cipher import vigenere_encrypt, vigenere_decrypt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    plain_text = request.form['plaintext']
    key = request.form.get('key')

    if not key:
        result, key = vigenere_encrypt(plain_text)
    else:
        result, _ = vigenere_encrypt(plain_text, key)

    return render_template('index.html', mode='encrypt', result=result, key=key, input_text=plain_text)

@app.route('/decrypt', methods=['POST'])
def decrypt():
    encrypted_text = request.form['encryptedText']
    key = request.form['key']

    if not key:
        error = "Key is required"
        return render_template('index.html', mode='decrypt', error=error, input_text=encrypted_text)

    result = vigenere_decrypt(encrypted_text, key)
    return render_template('index.html', mode='decrypt', result=result, key=key, input_text=encrypted_text)