import string


def clean_text(text: str) -> str:
    return ''.join(filter(str.isalpha, text.upper()))


def vigenere_encrypt(plaintext: str, key: str) -> str:
    key = clean_text(key)
    if not key:
        return ""

    encrypted_text = []
    key_index = 0

    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            encrypted_char = chr((ord(char) - base + shift) % 26 + base)
            encrypted_text.append(encrypted_char)
            key_index += 1
        else:
            encrypted_text.append(char)

    return ''.join(encrypted_text)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    key = clean_text(key)
    if not key:
        return ""

    decrypted_text = []
    key_index = 0

    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            decrypted_char = chr((ord(char) - base - shift) % 26 + base)
            decrypted_text.append(decrypted_char)
            key_index += 1
        else:
            decrypted_text.append(char)

    return ''.join(decrypted_text)
