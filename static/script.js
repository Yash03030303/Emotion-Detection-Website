const emojiMap = {
  "neutral": "😐",
  "calm": "😌",
  "happy": "😄",
  "sad": "😢",
  "angry": "😠",
  "fearful": "😨",
  "disgust": "🤢",
  "surprised": "😲",
  "unknown": "❓"
};

function displayResult(emotion, accuracy) {
  const emoji = emojiMap[emotion.toLowerCase()] || "❓";
  const capitalized = emotion.charAt(0).toUpperCase() + emotion.slice(1);

  // Main Result Display
  document.getElementById("result").innerHTML = `
    <div>Detected Emotion:</div>
    <div class="emoji">${emoji} ${capitalized}</div>
    <div>Model Accuracy: ${accuracy}%</div>
  `;

  // Add to Report Section
  const report = document.getElementById("reportBody");
  const timestamp = new Date().toLocaleString();
  const newRow = document.createElement("tr");
  newRow.innerHTML = `
    <td>${timestamp}</td>
    <td>${capitalized}</td>
    <td>${emoji}</td>
    <td>${accuracy}%</td>
  `;
  report.appendChild(newRow);
}

Dropzone.options.audioDropzone = {
  paramName: "file",
  maxFilesize: 10,
  acceptedFiles: ".wav,.mp3,.flac",
  init: function () {
    this.on("success", function (file, response) {
      const emotion = response.emotion.toLowerCase();
      const accuracy = response.accuracy; // Get accuracy from response
      displayResult(emotion, accuracy); // Display both emotion and accuracy

      // Load the uploaded audio file dynamically into WaveSurfer
      const fileUrl = URL.createObjectURL(file); // Create a URL for the uploaded file
      wavesurfer.load(fileUrl); // Load the uploaded file into WaveSurfer
    });

    this.on("error", function (file, errorMessage) {
      const msg = typeof errorMessage === 'string' ? errorMessage : errorMessage.error || "Upload error.";
      document.getElementById("result").innerHTML = `<p style="color: red;">Error: ${msg}</p>`;
    });
  }
};

// Dark mode toggle
document.getElementById('darkModeToggle').addEventListener('change', () => {
  document.body.classList.toggle('dark-mode');
});

// Initialize WaveSurfer
const wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: '#3498db',
  progressColor: '#1abc9c',
  height: 80,
  responsive: true
});

// Play/Pause functionality for audio control
document.getElementById('playPauseBtn').addEventListener('click', () => {
  wavesurfer.playPause();
});

// Optionally, add a seek functionality on the waveform
wavesurfer.on('seek', (progress) => {
  console.log('Seek position:', progress); // This logs the seek progress (0 to 1)
});

// Optional: You can adjust the waveform's appearance or interaction logic based on your needs
wavesurfer.on('ready', () => {
  console.log('Waveform is ready!');
  // You can auto-play or auto-start the waveform if needed
  // wavesurfer.play();
});
