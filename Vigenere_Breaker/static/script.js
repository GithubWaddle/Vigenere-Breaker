
var possibleKeyPlaintexts = [];
var promptingPossiblePlaintext = false;
var breakingProgressInterval = null;
var lastPossiblePlaintextIndex = 0

function cleanInput(str) {
  return str.toUpperCase().replace(/[^A-Z]/g, '');
}

function vigenereEncrypt(plaintext, key) {
  let result = '';
  let cleanKey = cleanInput(key);
  if (cleanKey.length === 0) return '';

  let keyIndex = 0;

  for (let i = 0; i < plaintext.length; i++) {
    let char = plaintext[i];
    if (/[A-Za-z]/.test(char)) {
      let isLower = char === char.toLowerCase();
      let p = char.toUpperCase().charCodeAt(0) - 65;
      let k = cleanKey.charCodeAt(keyIndex % cleanKey.length) - 65;
      let c = (p + k) % 26;
      let encryptedChar = String.fromCharCode(c + 65);
      result += isLower ? encryptedChar.toLowerCase() : encryptedChar;
      keyIndex++;
    } else {
      result += char;
    }
  }

  return result;
}

function vigenereDecrypt(ciphertext, key) {
  let result = '';
  let cleanKey = cleanInput(key);
  if (cleanKey.length === 0) return '';

  let keyIndex = 0;

  for (let i = 0; i < ciphertext.length; i++) {
    let char = ciphertext[i];
    if (/[A-Za-z]/.test(char)) {
      let isLower = char === char.toLowerCase();
      let c = char.toUpperCase().charCodeAt(0) - 65;
      let k = cleanKey.charCodeAt(keyIndex % cleanKey.length) - 65;
      let p = (c - k + 26) % 26;
      let decryptedChar = String.fromCharCode(p + 65);
      result += isLower ? decryptedChar.toLowerCase() : decryptedChar;
      keyIndex++;
    } else {
      result += char;
    }
  }

  return result;
}


function forceCapitalLetters(inputElement) {
  inputElement.addEventListener('input', () => {
    const original = inputElement.value;
    const transformed = original.replace(/[a-z]/g, char => char.toUpperCase());

    if (original !== transformed) {
      const selectionStart = inputElement.selectionStart;
      const selectionEnd = inputElement.selectionEnd;

      inputElement.value = transformed;

      // Restore cursor position
      inputElement.setSelectionRange(selectionStart, selectionEnd);
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
    ciphertext: document.getElementById("breaker-ciphertext-text-area").value,
	isKeyEnglishWord: document.querySelector('#is-key-english').checked,
  };

  const progressBarText = document.getElementById("possible-plaintext-prompt-popup-progress-bar");
  progressBarText.innerHTML = "Breaking... (0/0)"
  
  fetch("/startBreaking", {
    "method": "POST",
    "headers": {"Content-Type": "application/json"},
    "body": JSON.stringify(data),
  });

  const denyButton = document.getElementById("possible-plaintext-prompt-popup-deny");
  const confirmButton = document.getElementById("possible-plaintext-prompt-popup-confirm");

  denyButton.addEventListener("click", onDenyButtonPressed);
  confirmButton.addEventListener("click", onConfirmButtonPressed);

  openPossiblePlaintextPopup();
  breakingProgressInterval = setInterval(getPossiblePlaintextProgess, 5000);
}

function onDenyButtonPressed() {
  promptNextPossiblePlaintext(lastPossiblePlaintextIndex, false);
}

function onConfirmButtonPressed() {
  promptNextPossiblePlaintext(lastPossiblePlaintextIndex, true);
}

function getPossiblePlaintextProgess() {
  fetch("/breakingProgress")
    .then(response => response.json())
    .then(data => {
      console.log(data);
      progressPercentage = data.progress;
      newPossibleKeyPlaintexts = data.possibleKeyPlaintexts;

      const progressBarText = document.getElementById("possible-plaintext-prompt-popup-progress-bar");
      progressBarText.innerHTML = "Breaking... (" + data.progress.numerator + "/" + data.progress.denominator + ")"

      if (!Object.keys(newPossibleKeyPlaintexts).length) {
         return;
      }

      possibleKeyPlaintexts = newPossibleKeyPlaintexts;

      if (!promptingPossiblePlaintext) {
        promptPossiblePlaintext(lastPossiblePlaintextIndex);
      }
      
    });
}


function promptPossiblePlaintext(index) {
  console.log("Prompting possible plaintext index: " + index);
  promptingPossiblePlaintext = true;
  const possibleKeyText = document.getElementById("possible-plaintext-prompt-popup-possible-key");
  const possiblePlaintextText = document.getElementById("possible-plaintext-prompt-popup-possible-plaintext");
  const denyButton = document.getElementById("possible-plaintext-prompt-popup-deny");
  const confirmButton = document.getElementById("possible-plaintext-prompt-popup-confirm");


  if (index >= possibleKeyPlaintexts.length) {
    promptingPossiblePlaintext = false;
    possibleKeyText.value = "";
    possiblePlaintextText.value = "";
    denyButton.disabled = true;
    confirmButton.disabled = true;
    return;
  }

  denyButton.disabled = false;
  confirmButton.disabled = false;

  possiblePlaintext = possibleKeyPlaintexts[index].plaintext;
  possibleKey = possibleKeyPlaintexts[index].key;
  possibleKeyText.value = possibleKey;
  possiblePlaintextText.value = possiblePlaintext;
}


function promptNextPossiblePlaintext(index, isConfirmLast) {
  if (isConfirmLast) {
    console.log("Confirmed possible plaintext index: " + index);
    console.log(possibleKeyPlaintexts);
    finishBreaking(
      possibleKeyPlaintexts[index].key,
      possibleKeyPlaintexts[index].plaintext
    );
  }

  lastPossiblePlaintextIndex = index + 1;
  promptPossiblePlaintext(lastPossiblePlaintextIndex);
}


function finishBreaking(key, plaintext) {
  clearInterval(breakingProgressInterval);
  breakingProgressInterval = null;
  lastPossiblePlaintextIndex = 0;
  possibleKeyPlaintexts = [];
  promptingPossiblePlaintext = false;

  
  const denyButton = document.getElementById("possible-plaintext-prompt-popup-deny");
  const confirmButton = document.getElementById("possible-plaintext-prompt-popup-confirm");
  denyButton.removeEventListener("click", onDenyButtonPressed);
  confirmButton.removeEventListener("click", onConfirmButtonPressed);

  closePossiblePlaintextPopup();

  const breakerPlaintextOutput = document.getElementById('breaker-plaintext-text-area');
  const breakerKeyOutput = document.getElementById('breaker-key-text-area');

  breakerKeyOutput.value = key;
  breakerPlaintextOutput.value = plaintext;

  fetch("/foundPlaintext", {
    "method": "POST"
  })
}


function openPossiblePlaintextPopup() {
  document.getElementById("possible-plaintext-prompt-popup").style.display = "block";
}

function closePossiblePlaintextPopup() {
  document.getElementById("possible-plaintext-prompt-popup").style.display = "none";
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

    const plaintext = pocketEncoderDecoderPlaintextInput.value;
    const key = cleanInput(pocketEncoderDecoderKeyInput.value);
    const ciphertext = vigenereEncrypt(plaintext, key);

    pocketEncoderDecoderCiphertextInput.value = ciphertext;

    pocketEncoderDecoderPlaintextInput.value = plaintext.replace(/[a-z]/g, c => c.toUpperCase());

    isUpdating = false;
  }

  function updateFromCiphertext() {
    if (isUpdating) return;
      isUpdating = true;

    const ciphertext = pocketEncoderDecoderCiphertextInput.value;
    const key = cleanInput(pocketEncoderDecoderKeyInput.value);
    const plaintext = vigenereDecrypt(ciphertext, key);

    pocketEncoderDecoderPlaintextInput.value = plaintext;

    pocketEncoderDecoderCiphertextInput.value = ciphertext.replace(/[a-z]/g, c => c.toUpperCase());

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


