// Day/Night Mode Toggle
document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = document.getElementById('themeIcon');
    const body = document.body;

    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark-mode');
        themeIcon.textContent = '☀️';
    } else {
        themeIcon.textContent = '🌙';
    }

    themeToggle.addEventListener('click', function() {
        body.classList.toggle('dark-mode');
        if (body.classList.contains('dark-mode')) {
            themeIcon.textContent = '☀️';
            localStorage.setItem('theme', 'dark');
        } else {
            themeIcon.textContent = '🌙';
            localStorage.setItem('theme', 'light');
        }
    });
});

// G9: Text-to-ISL Converter
function convertToSign() {
    let inputText = document.getElementById('universalInput').value.toUpperCase().trim();
    let output = document.getElementById('islOutput');
    output.innerHTML = '';

    let words = inputText.split(/\s+/);
    let wordIndex = 0;

    function playNextItem() {
        if (wordIndex < words.length) {
            let word = words[wordIndex];

            let wordTitle = document.createElement('div');
            wordTitle.className = 'word-title';
            wordTitle.textContent = word;

            let video = document.createElement('video');
            video.src = `/static/videos/${word}.mp4`;
            video.controls = false;
            video.autoplay = true;
            video.muted = true;

            video.onerror = function () {
                let letterContainer = document.createElement('div');
                letterContainer.className = 'letter-container';

                let letterIndex = 0;

                function playNextLetter() {
                    if (letterIndex < word.length) {
                        let char = word[letterIndex];
                        if (char.match(/[A-Z]/)) {
                            let letterVideo = document.createElement('video');
                            letterVideo.src = `/static/videos/${char}.mp4`;
                            letterVideo.controls = false;
                            letterVideo.autoplay = true;
                            letterVideo.muted = true;

                            letterVideo.onended = function () {
                                letterIndex++;
                                playNextLetter();
                            };

                            letterContainer.innerHTML = '';
                            letterContainer.appendChild(letterVideo);
                        } else {
                            letterIndex++;
                            playNextLetter();
                        }
                    } else {
                        wordIndex++;
                        playNextItem();
                    }
                }

                output.innerHTML = '';
                output.appendChild(wordTitle);
                output.appendChild(letterContainer);
                playNextLetter();
            };

            video.onended = function () {
                wordIndex++;
                playNextItem();
            };

            output.innerHTML = '';
            output.appendChild(wordTitle);
            output.appendChild(video);
        }
    }

    playNextItem();
}

// G10: AI Voice Assistant
function askAssistant() {
    let query = document.getElementById('assistantInput').value.trim();
    if (!query) return;

    fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('assistantResponse').innerText = data.response;
        let audio = document.getElementById('assistantAudio');
        audio.src = data.audio;
        audio.style.display = 'block';
        audio.play();
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('assistantResponse').innerText = 'Error processing request.';
    });
}

function handleAssistantKeyPress(event) {
    if (event.key === 'Enter') {
        askAssistant();
    }
}

// G11: Text-to-Audio with Emotion Detection
function convertEmotionAudio() {
    let text = document.getElementById('universalInput').value.trim();
    if (!text) return;

    let formData = new FormData();
    formData.append('text', text);

    fetch('/text-to-audio', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            let emotions = data.emotions.map(e => `${e.emotion}: ${e.confidence.toFixed(2)}`).join(', ');
            let params = `Rate: ${data.speech_params.rate.toFixed(0)}, Volume: ${data.speech_params.volume.toFixed(2)}`;
            document.getElementById('emotionResults').querySelector('span').innerText = emotions;
            document.getElementById('speechParams').querySelector('span').innerText = params;
            let audio = document.getElementById('emotionAudio');
            audio.src = data.audio;
            audio.style.display = 'block';
            audio.play();
        } else {
            document.getElementById('emotionResults').querySelector('span').innerText = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('emotionResults').querySelector('span').innerText = 'Error processing request.';
    });
}

// G13: Speech-to-Text Translation with TTS
function translateSpeak() {
    let text = document.getElementById('universalInput').value.trim();
    let lang = document.getElementById('targetLang').value;
    if (!text) return;

    fetch('/translate-speak', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, lang: lang })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            document.getElementById('translateResult').querySelector('span').innerText = `${data.translated} (${data.lang})`;
            let audio = document.getElementById('translateAudio');
            audio.src = data.audio;
            audio.style.display = 'block';
            audio.play();
        } else {
            document.getElementById('translateResult').querySelector('span').innerText = 'Error: ' + data.message;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('translateResult').querySelector('span').innerText = 'Error processing request.';
    });
}

// Speech Recognition (updated for universal input)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;

function startSpeechRecognition(section) {
    if (!recognition) {
        alert("Speech recognition is not supported in your browser. Please use Chrome.");
        return;
    }

    let mic;
    let input;
    if (section === 'universal') {
        mic = document.getElementById('universalMic');
        input = document.getElementById('universalInput');
    } else if (section === 'assistant') {
        mic = document.getElementById('assistantMic');
        input = document.getElementById('assistantInput');
    }

    mic.classList.add('glowing');
    recognition.start();

    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        input.value = transcript;
        mic.classList.remove('glowing');
        if (section === 'assistant') {
            askAssistant();
        }
        // No automatic action for universal input; user will click the desired button
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        mic.classList.remove('glowing');
    };

    recognition.onend = function() {
        mic.classList.remove('glowing');
    };
}

// Background Triangles (G9)
document.addEventListener("DOMContentLoaded", function() {
    const wrap = document.querySelector('.wrap');
    const totalTriangles = 100;

    for (let i = 0; i < totalTriangles; i++) {
        const tri = document.createElement('div');
        tri.classList.add('tri');
        tri.style.top = `${Math.random() * 100}vh`;
        tri.style.left = `${Math.random() * 100}vw`;

        const duration = Math.random() * 10 + 5;
        tri.style.animation = `randomMovement ${duration}s infinite`;

        wrap.appendChild(tri);
    }

    document.addEventListener('mousemove', function(e) {
        const triangles = document.querySelectorAll('.tri');
        triangles.forEach(triangle => {
            const rect = triangle.getBoundingClientRect();
            const dx = e.clientX - (rect.left + rect.width / 2);
            const dy = e.clientY - (rect.top + rect.height / 2);
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 150) {
                const angle = Math.atan2(dy, dx);
                const offsetX = Math.cos(angle) * -50;
                const offsetY = Math.sin(angle) * -50;
                triangle.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
            } else {
                triangle.style.transform = '';
            }
        });
    });
});