import string


def clean_text(text: str) -> str:
    return ''.join(filter(str.isalpha, text.upper()))


def vigenere_encrypt(plaintext: str, key: str) -> str:
    plaintext = clean_text(plaintext)
    key = clean_text(key)

    if not key or not plaintext:
        return ""

    encoded_text = ""
    for i, char in enumerate(plaintext):
        key_char = key[i % len(key)]
        shift = ord(key_char) - ord('A')
        encrypted_char = chr(((ord(char) - ord('A') + shift) % 26) + ord('A'))
        encoded_text += encrypted_char

    return encoded_text


def vigenere_decrypt(encodedtext: str, key: str) -> str:
    encodedtext = clean_text(encodedtext)
    key = clean_text(key)

    if not key or not encodedtext:
        return ""

    decoded_text = ""
    for i, char in enumerate(encodedtext):
        key_char = key[i % len(key)]
        shift = ord(key_char) - ord('A')
        decrypted_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
        decoded_text += decrypted_char

    return decoded_text
