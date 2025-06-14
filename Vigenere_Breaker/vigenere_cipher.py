import random
import string

def generate_key(length):
    return ''.join(random.choices(string.ascii_letters, k=length))

def vigenere_encrypt(plaintext, key=None):
    if key is None:
        key = generate_key(len([c for c in plaintext if c.isalpha()]))

    counter = 0
    encoded_text = ""
    for char in plaintext:
        if char.isalpha():
            vig_key = key[counter % len(key)]
            vig_key_val = ord(vig_key.lower()) - ord('a')

            if char.islower():
                vig_char = chr(((ord(char) - ord("a") + vig_key_val) % 26) + ord("a"))
            else:
                vig_char = chr(((ord(char) - ord("A") + vig_key_val) % 26) + ord("A"))

            counter += 1
        else:
            vig_char = char

        encoded_text += vig_char

    return encoded_text, key


def vigenere_decrypt(encodedtext, key):
    counter = 0
    decoded_text = ""
    for char in encodedtext:
        if char.isalpha():
            vig_key = key[counter % len(key)]
            vig_key_val = ord(vig_key.lower()) - ord('a')

            if char.islower():
                vig_char = chr(((ord(char) - ord("a") - vig_key_val) % 26) + ord("a"))
            else:
                vig_char = chr(((ord(char) - ord("A") - vig_key_val) % 26) + ord("A"))

            counter += 1
        else:
            vig_char = char

        decoded_text += vig_char

    return decoded_text