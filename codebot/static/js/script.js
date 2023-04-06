const startBtn = document.getElementById('start');
const stopBtn = document.getElementById('stop');
const transcription = document.getElementById('transcription');
const messageInput = document.getElementById('message');
const sendBtn = document.getElementById('send');
const recognition = new webkitSpeechRecognition();
recognition.continuous = true;
recognition.interimResults = true;
recognition.lang = 'en-US';
let recognitionResult = '';

startBtn.addEventListener('click', () => {
recognition.start();
startBtn.disabled = true;
stopBtn.disabled = false;
});

stopBtn.addEventListener('click', () => {
recognition.stop();
startBtn.disabled = false;
stopBtn.disabled = true;
messageInput.value = recognitionResult;
saveTranscription();
});

recognition.onresult = (event) => {
let interimTranscription = '';
for (let i = event.resultIndex; i < event.results.length; i++) {
  const transcript = event.results[i][0].transcript;
  if (event.results[i].isFinal) {
    recognitionResult += transcript;
  } else {
    interimTranscription += transcript;
    messageInput.value = recognitionResult;
  }
}
transcription.innerHTML = interimTranscription;
};

recognition.onerror = (event) => {
console.error(`Speech recognition error: ${event.error}`);
};
function getCookie(name) {
let cookieValue = null;
if (document.cookie && document.cookie !== '') {
  const cookies = document.cookie.split(';');
  for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
      }
  }
}
return cookieValue;
}

function saveTranscription() {
console.log(`Transcription: ${recognitionResult}`);
const data = { transcription: recognitionResult };
fetch('/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: JSON.stringify(data)
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
recognitionResult = '';
}

sendBtn.addEventListener('click', (event) => {
event.preventDefault();
const code = messageInput.value.trim();
const lang = document.querySelector('[name="lang"]').value;
const action = document.querySelector('[name="action"]').value;
const csrftoken = getCookie('csrftoken');
fetch('/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-CSRFToken': csrftoken
  },
  body: JSON.stringify({ code, lang, action })
})
  .then(response => response.json())
  .then(data => {
    console.log(data);
    messageInput.value = '';
    transcription.innerHTML = '';
    recognitionResult = '';


  })
  .catch(error => console.error(error));
  document.getElementById('message-form').submit();

});

recognition.onend = () => {
stopBtn.disabled = true;
startBtn.disabled = false;
};

recognition.onstart = () => {
console.log('Speech recognition started');
};