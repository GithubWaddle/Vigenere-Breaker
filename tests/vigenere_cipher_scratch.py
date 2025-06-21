
from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def vigenere_decrypt(encodedtext, key):
    counter = 0
    decoded_chars = []

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
            vig_char = char  # Preserve non-alphabetic characters

        decoded_chars.append(vig_char)

    return ''.join(decoded_chars)

def vigenere_encrypt(plaintext, key=None):
    # Generate key only for alphabetic characters
    if key is None:
        key = generate_key(len([c for c in plaintext if c.isalpha()]))

    counter = 0
    encoded_chars = []

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
            vig_char = char  # Non-alphabetic characters are preserved

        encoded_chars.append(vig_char)

    return ''.join(encoded_chars), key


def main():
	print(identifier.classify("HELL IS FOREVER WHETHER YOU LIKE IT OR NOT."))


if __name__ == "__main__":
	main()