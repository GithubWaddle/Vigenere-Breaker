import string
import itertools
from collections import Counter
import langid

WORDS_FILE_PATH = "WORDS.txt"

ENGLISH_FREQ = {
    'A': 0.08167, 'B': 0.01492, 'C': 0.02782, 'D': 0.04253, 'E': 0.12702,
    'F': 0.02228, 'G': 0.02015, 'H': 0.06094, 'I': 0.06966, 'J': 0.00153,
    'K': 0.00772, 'L': 0.04025, 'M': 0.02406, 'N': 0.06749, 'O': 0.07507,
    'P': 0.01929, 'Q': 0.00095, 'R': 0.05987, 'S': 0.06327, 'T': 0.09056,
    'U': 0.02758, 'V': 0.00978, 'W': 0.02360, 'X': 0.00150, 'Y': 0.01974,
    'Z': 0.00074
}


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


def monogram_score(text):
    freq = Counter(text)
    N = len(text)
    return sum((freq.get(c, 0) / N) * ENGLISH_FREQ.get(c, 0) for c in string.ascii_uppercase) if N > 0 else 0


def combined_score(text):
    mono = monogram_score(text)
    lang, conf = langid.classify(text)
    return mono + (conf * 0.2) if lang == 'en' else mono * 0.5


def index_of_coincidence(text):
    freqs = Counter(text)
    N = len(text)
    return sum(f * (f - 1) for f in freqs.values()) / (N * (N - 1)) if N > 1 else 0


def estimate_key_length(ciphertext):
    avg_ics = {}
    for key_len in range(1, 11):
        chunks = [ciphertext[i::key_len] for i in range(key_len)]
        ics = [index_of_coincidence(chunk) for chunk in chunks]
        avg_ics[key_len] = sum(ics) / len(ics)
    return max(avg_ics, key=avg_ics.get)


def brute_force(ciphertext, key_len, top_n=5):
    results = []
    for key_tuple in itertools.product(string.ascii_uppercase, repeat=key_len):
        key = ''.join(key_tuple)
        plain = vigenere_decrypt(ciphertext, key)
        if len(plain) < 5:
            continue
        score = combined_score(plain)
        results.append((plain, key, score))
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_n]


def dictionary_attack(ciphertext, dictionary_words, top_n=5):
    results = []
    for key in dictionary_words:
        plain = vigenere_decrypt(ciphertext, key)
        if len(plain) < 5:
            continue
        score = combined_score(plain)
        results.append((plain, key, score))
    results.sort(key=lambda x: x[2], reverse=True)
    return results[:top_n]


def statistical_attack(ciphertext, top_n=5):
    key_len = estimate_key_length(ciphertext)
    return frequency_attack(ciphertext, key_len, top_n)


def frequency_attack(ciphertext, key_len, top_n=5):
    key = ""
    for i in range(key_len):
        segment = ciphertext[i::key_len]
        shift = best_shift_for_segment(segment)
        key += chr(shift + ord('A'))
    plain = vigenere_decrypt(ciphertext, key)
    score = combined_score(plain)
    return [(plain, key, score)]


def best_shift_for_segment(segment):
    min_chi_sq = float('inf')
    best_shift = 0
    for shift in range(26):
        shifted = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A')) for c in segment)
        freq = Counter(shifted)
        N = len(shifted)
        chi_sq = sum(
            ((freq.get(chr(i + ord('A')), 0) / N - ENGLISH_FREQ[chr(i + ord('A'))]) ** 2)
            for i in range(26)
        )
        if chi_sq < min_chi_sq:
            min_chi_sq = chi_sq
            best_shift = shift
    return best_shift


def break_cipher(ciphertext, dictionary_words=None):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    key_len = estimate_key_length(ciphertext)

    if key_len < 5:
        return brute_force(ciphertext, key_len)[0][0]
    elif dictionary_words:
        return dictionary_attack(ciphertext, dictionary_words)[0][0]
    elif len(ciphertext) > 100:
        return statistical_attack(ciphertext)[0][0]
    else:
        return frequency_attack(ciphertext, key_len)[0][0]


def break_with_polling(ciphertext, dictionary_words=None, top_n=5):
    ciphertext = ''.join(filter(str.isalpha, ciphertext.upper()))
    key_len = estimate_key_length(ciphertext)

    if key_len < 5:
        results = brute_force(ciphertext, key_len, top_n)
    elif dictionary_words:
        results = dictionary_attack(ciphertext, dictionary_words, top_n)
    elif len(ciphertext) > 100:
        results = statistical_attack(ciphertext, top_n)
    else:
        results = frequency_attack(ciphertext, key_len, top_n)

    log = [{"key": k, "plaintext": p, "score": round(s, 4)} for (p, k, s) in results]
    return {"plaintexts": log, "log": log}


def main():
    with open(WORDS_FILE_PATH, 'r') as words_file:
        dictionary_words = [word.strip().upper() for word in words_file]

    MY_CIPHERTEXT = "MBDWHVOPHSHFRHWMHVSDJEZRW"
    plaintext = break_cipher(MY_CIPHERTEXT, dictionary_words)
    print(f"Decrypted text: {plaintext}")


if __name__ == "__main__":
    main()
