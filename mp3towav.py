import os
import librosa
import soundfile as sf

def convert_mp3_to_wav_librosa(mp3_file_path, wav_file_path=None, sample_rate=22050):
    """
    Converts MP3 to WAV using librosa and soundfile.
    
    Args:
        mp3_file_path (str): Input MP3 file path
        wav_file_path (str, optional): Output WAV file path
        sample_rate (int): Target sample rate (default 22050)
    
    Returns:
        str: Path to converted WAV file
    """
    if not os.path.exists(mp3_file_path):
        raise FileNotFoundError(f"Input file not found: {mp3_file_path}")
    
    if wav_file_path is None:
        base = os.path.splitext(mp3_file_path)[0]
        wav_file_path = f"{base}.wav"
    
    try:
        # Load MP3 file with librosa
        y, sr = librosa.load(mp3_file_path, sr=sample_rate)
        
        # Save as WAV
        sf.write(wav_file_path, y, sr)
        
        return wav_file_path
    
    except Exception as e:
        raise Exception(f"Error converting MP3 to WAV: {str(e)}")
