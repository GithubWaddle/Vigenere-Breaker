function cleanInput(str) {
  return str.toUpperCase().replace(/[^A-Z]/g, '');
}


function vigenereEncrypt(plaintext, key) {
  let result = '';
  key = cleanInput(key);
  if (key.length === 0) return '';
  for (let i = 0; i < plaintext.length; i++) {
    let p = plaintext.charCodeAt(i) - 65;
    let k = key.charCodeAt(i % key.length) - 65;
    let c = (p + k) % 26;
    result += String.fromCharCode(c + 65);
  }
  return result;
}


function vigenereDecrypt(ciphertext, key) {
  let result = '';
  key = cleanInput(key);
  if (key.length === 0) return '';
  for (let i = 0; i < ciphertext.length; i++) {
    let c = ciphertext.charCodeAt(i) - 65;
    let k = key.charCodeAt(i % key.length) - 65;
    let p = (c - k + 26) % 26;
    result += String.fromCharCode(p + 65);
  }
  return result;
}


function forceCapitalLetters(inputElement) {
  inputElement.addEventListener('input', () => {
    const cleaned = cleanInput(inputElement.value);
    if (inputElement.value !== cleaned) {
      inputElement.value = cleaned;
    }
  });
}


function openMoreInformationPopup() {
  document.getElementById("more-information-popup").style.display = "block";
}


function closeMoreInformationPopup() {
  document.getElementById("more-information-popup").style.display = "none";
}


function breakVigenere() {
  const data = {
    ciphertext: document.getElementById("breaker-ciphertext-text-area").value
  };
  fetch("/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  })
  .then(response => response.json())
  .then(result => {
    console.log(result);
  })
  .catch(error => {
    console.error('Error:', error);
  });
}


function main() {
  const breakerCiphertextInput = document.getElementById('breaker-ciphertext-text-area');
  const pocketEncoderDecoderKeyInput = document.getElementById('pocket-encoder-decoder-key-text-area');
  const pocketEncoderDecoderPlaintextInput = document.getElementById('pocket-encoder-decoder-plaintext-text-area');
  const pocketEncoderDecoderCiphertextInput = document.getElementById('pocket-encoder-decoder-ciphertext-text-area');
  let isUpdating = false;

  [breakerCiphertextInput, pocketEncoderDecoderKeyInput, pocketEncoderDecoderPlaintextInput, pocketEncoderDecoderCiphertextInput].forEach(forceCapitalLetters);

  function updateFromPlaintext() {
    if (isUpdating) return;
    isUpdating = true;
    const plaintext = cleanInput(pocketEncoderDecoderPlaintextInput.value);
    const key = cleanInput(pocketEncoderDecoderKeyInput.value);
    pocketEncoderDecoderPlaintextInput.value = plaintext;
    pocketEncoderDecoderCiphertextInput.value = vigenereEncrypt(plaintext, key);
    isUpdating = false;
  }

  function updateFromCiphertext() {
    if (isUpdating) return;
    isUpdating = true;
    const ciphertext = cleanInput(pocketEncoderDecoderCiphertextInput.value);
    const key = cleanInput(pocketEncoderDecoderKeyInput.value);
    pocketEncoderDecoderCiphertextInput.value = ciphertext;
    pocketEncoderDecoderPlaintextInput.value = vigenereDecrypt(ciphertext, key);
    isUpdating = false;
  }

  function updateBoth() {
    updateFromPlaintext();
  }

  pocketEncoderDecoderKeyInput.addEventListener('input', updateBoth);
  pocketEncoderDecoderPlaintextInput.addEventListener('input', updateFromPlaintext);
  pocketEncoderDecoderCiphertextInput.addEventListener('input', updateFromCiphertext);
}

window.addEventListener('DOMContentLoaded', main);
