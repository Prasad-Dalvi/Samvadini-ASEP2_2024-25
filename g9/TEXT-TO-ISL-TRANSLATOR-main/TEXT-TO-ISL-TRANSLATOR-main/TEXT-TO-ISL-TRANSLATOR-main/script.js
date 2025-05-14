// function convertToSign() {
//     let inputText = document.getElementById('textInput').value.toUpperCase().trim();
//     let output = document.getElementById('output');
//     output.innerHTML = '';  // Clear any previous content

//     // Split the input text into words
//     let words = inputText.split(/\s+/);

//     let wordIndex = 0;

//     // Function to play videos one by one
//     function playNextItem() {
//         if (wordIndex < words.length) {
//             let word = words[wordIndex];

//             // Display word as title
//             let wordTitle = document.createElement('div');
//             wordTitle.className = 'word-title';
//             wordTitle.textContent = word;

//             // Try to play the word video
//             let video = document.createElement('video');
//             video.src = `./videos/${word}.mp4`;  // Set video source dynamically
//             video.controls = false;  // Disable controls for clean display
//             video.autoplay = true;  // Start playing immediately
//             video.muted = true;  // Mute the video

//             // Handle cases when video file is not found
//             video.onerror = function () {
//                 // Fallback to display individual letter images
//                 let letterContainer = document.createElement('div');
//                 letterContainer.className = 'letter-container';

//                 for (let char of word) {
//                     if (char.match(/[A-Z]/)) {  // Only consider alphabetic characters
//                         let img = document.createElement('img');
//                         img.src = `./images/${char}.png`;  // Set the image source dynamically
//                         img.alt = `${char} sign`;  // Set the alt text dynamically
//                         letterContainer.appendChild(img);
//                     }
//                 }

//                 // Clear previous content and show letters
//                 output.innerHTML = '';
//                 output.appendChild(wordTitle);  // Show the word heading
//                 output.appendChild(letterContainer);

//                 // After 3 seconds, move to the next word
//                 setTimeout(function () {
//                     wordIndex++;
//                     playNextItem();
//                 }, 3000);
//             };

//             // On video end, play the next word's video or letters
//             video.onended = function () {
//                 wordIndex++;
//                 playNextItem();
//             };

//             // Clear previous content and append the video
//             output.innerHTML = '';
//             output.appendChild(wordTitle);  // Show the word heading
//             output.appendChild(video);
//         }
//     }

//     playNextItem();  // Start playing the first video or letters
// }

// // Function to handle 'Enter' key press for conversion
// function handleKeyPress(event) {
//     if (event.key === 'Enter') {
//         convertToSign();
//     }
// }

// // Generate random triangles
// document.addEventListener("DOMContentLoaded", function() {
//     const wrap = document.querySelector('.wrap');
//     const totalTriangles = 100;  // Number of triangles to be generated

//     for (let i = 0; i < totalTriangles; i++) {
//         const tri = document.createElement('div');
//         tri.classList.add('tri');
        
//         // Randomize initial positions
//         tri.style.top = `${Math.random() * 100}vh`;
//         tri.style.left = `${Math.random() * 100}vw`;

//         // Set a random animation duration
//         const duration = Math.random() * 10 + 5;  // Between 5s and 10s
//         tri.style.animation = `randomMovement ${duration}s infinite`;

//         wrap.appendChild(tri);
//     }

//     // Add event listener for mouse movement to move triangles away from the cursor
//     document.addEventListener('mousemove', function(e) {
//         const triangles = document.querySelectorAll('.tri');
//         triangles.forEach(triangle => {
//             const rect = triangle.getBoundingClientRect();
//             const dx = e.clientX - (rect.left + rect.width / 2);
//             const dy = e.clientY - (rect.top + rect.height / 2);
//             const dist = Math.sqrt(dx * dx + dy * dy);
            
//             if (dist > 150) {  // Move away if cursor is within 150px of triangle
//                 const angle = Math.atan2(dy, dx);
//                 const offsetX = Math.cos(angle) * -50;
//                 const offsetY = Math.sin(angle) * -50;
//                 triangle.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
//             }
//         });
//     });
// });
// // Speech recognition setup
// const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
// const recognition = new SpeechRecognition();

// function startSpeechRecognition() {
//     let mic = document.getElementById('mic');
//     mic.classList.add('glowing');  // Add glowing effect when mic is clicked

//     recognition.start();

//     recognition.onresult = function(event) {
//         let transcript = event.results[0][0].transcript;
//         document.getElementById('textInput').value = transcript;  // Set input to recognized text
//         mic.classList.remove('glowing');  // Remove glowing effect when speech recognition ends
//         convertToSign();  // Convert speech to sign language
//     };

//     recognition.onerror = function(event) {
//         console.error('Speech recognition error:', event.error);
//         mic.classList.remove('glowing');  // Remove glowing effect in case of error
//     };

//     recognition.onend = function() {
//         mic.classList.remove('glowing');  // Remove glowing effect when recognition stops
//    };
// }



function convertToSign() {
    let inputText = document.getElementById('textInput').value.toUpperCase().trim();
    let output = document.getElementById('output');
    output.innerHTML = '';  // Clear previous content

    let words = inputText.split(/\s+/);
    let wordIndex = 0;

    function playNextItem() {
        if (wordIndex < words.length) {
            let word = words[wordIndex];

            let wordTitle = document.createElement('div');
            wordTitle.className = 'word-title';
            wordTitle.textContent = word;

            let video = document.createElement('video');
            video.src = `./assets/${word}.mp4`;  // Load word video from assets folder
            video.controls = false;
            video.autoplay = true;
            video.muted = true;

            video.onerror = function () {
                // Fallback: play individual letter videos
                let letterContainer = document.createElement('div');
                letterContainer.className = 'letter-container';

                let letterIndex = 0;

                function playNextLetter() {
                    if (letterIndex < word.length) {
                        let char = word[letterIndex];
                        if (char.match(/[A-Z]/)) {
                            let letterVideo = document.createElement('video');
                            letterVideo.src = `./assets/${char}.mp4`;  // Load letter video from assets folder
                            letterVideo.controls = false;
                            letterVideo.autoplay = true;
                            letterVideo.muted = true;

                            letterVideo.onended = function () {
                                letterIndex++;
                                playNextLetter();
                            };

                            // Clear previous and show next letter video
                            letterContainer.innerHTML = '';
                            letterContainer.appendChild(letterVideo);
                        } else {
                            letterIndex++;
                            playNextLetter();
                        }
                    } else {
                        // After all letters, go to next word
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

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        convertToSign();
    }
}

// Generate random triangles
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

// Speech recognition setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

function startSpeechRecognition() {
    let mic = document.getElementById('mic');
    mic.classList.add('glowing');

    recognition.start();

    recognition.onresult = function(event) {
        let transcript = event.results[0][0].transcript;
        document.getElementById('textInput').value = transcript;
        mic.classList.remove('glowing');
        convertToSign();
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error:', event.error);
        mic.classList.remove('glowing');
    };

    recognition.onend = function() {
        mic.classList.remove('glowing');
    };
}
