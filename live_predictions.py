import os
import keras
import librosa
import numpy as np
from config import MODEL_DIR_PATH

class LivePredictions:
    def __init__(self, file):
        self.file = file
        self.path = os.path.join(MODEL_DIR_PATH, 'Emotion_Voice_Detection_Model1.h5')
        self.loaded_model = keras.models.load_model(self.path)

    def make_predictions(self):
        data, sampling_rate = librosa.load(self.file, sr=None)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=0)
        x = np.expand_dims(x, axis=-1)
        predictions = np.argmax(self.loaded_model.predict(x), axis=-1)[0]
        return self.convert_class_to_emotion(predictions)

    @staticmethod
    def convert_class_to_emotion(pred):
        label_conversion = {
            0: 'neutral', 1: 'calm', 2: 'happy', 3: 'sad',
            4: 'angry', 5: 'fearful', 6: 'disgust', 7: 'surprised'
        }
        return label_conversion.get(pred, "Unknown")
