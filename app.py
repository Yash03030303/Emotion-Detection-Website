import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from live_predictions import LivePredictions
from mp3towav import convert_mp3_to_wav_librosa

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Store the ground truth and predictions (for demo purposes, using a list)
# In production, you might want to use a database.
predictions_list = []
ground_truths_list = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        ext = filename.rsplit('.', 1)[1].lower()

        # Convert MP3 to WAV if needed
        if ext == 'mp3':
            try:
                wav_path = convert_mp3_to_wav_librosa(filepath)
            except Exception as e:
                return jsonify({'error': f'MP3 conversion failed: {str(e)}'}), 500
        else:
            wav_path = filepath

        if not wav_path or not os.path.exists(wav_path):
            return jsonify({'error': 'Converted file not found'}), 500

        try:
            # Get model prediction
            prediction = LivePredictions(file=wav_path).make_predictions()

            # For real-time accuracy, you would need the ground truth
            # Let's assume you are receiving the true label from the frontend (or through user input).
            # For demonstration, you can assume a static value for the true label.
            # Replace with actual logic to obtain the ground truth.

            true_label = "happy"  # Replace this with dynamic ground truth

            # Store predictions and ground truth for accuracy calculation
            predictions_list.append(prediction)
            ground_truths_list.append(true_label)

            # Calculate accuracy
            correct_predictions = sum(1 for p, t in zip(predictions_list, ground_truths_list) if p == t)
            accuracy = (correct_predictions / len(predictions_list)) * 100

            return jsonify({'emotion': prediction, 'accuracy': accuracy})
        finally:
            # Clean up the uploaded and converted files
            if os.path.exists(wav_path):
                os.remove(wav_path)
            if ext == 'mp3' and os.path.exists(filepath):
                os.remove(filepath)

    return jsonify({'error': 'Invalid file type'}), 400

# Endpoint to fetch model accuracy
@app.route('/model_accuracy')
def model_accuracy():
    # Calculate the accuracy dynamically (assuming the backend stores predictions)
    if predictions_list:
        correct_predictions = sum(1 for p, t in zip(predictions_list, ground_truths_list) if p == t)
        accuracy = (correct_predictions / len(predictions_list)) * 100
        return jsonify({"accuracy": accuracy})
    else:
        return jsonify({"accuracy": 0})  # No predictions yet

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
