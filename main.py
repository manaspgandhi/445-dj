import sys
import librosa
import soundfile as sf
import numpy as np

#To change tempo: python main.py change_tempo carnival.mp3 output.mp3 1.5
#To overlay songs: python main.py overlay_songs pimp.mp3 drill.mp3 output2.mp3

def change_tempo(input_file, output_file, tempo):
    """
    Change the tempo of an audio file without changing the pitch.
    
    :param input_file: Path to the input audio file
    :param output_file: Path to save the output audio file
    :param tempo: Tempo adjustment factor (e.g., 1.5 for 150% tempo)
    """
    #load audio file
    audio, sample_rate = librosa.load(input_file, sr=None)

    #adjust tempo
    adjusted_audio = librosa.effects.time_stretch(audio, rate=tempo)

    #save modified audio to output.py
    sf.write(output_file, adjusted_audio, sample_rate)
    print(f"Tempo-adjusted audio saved to: {output_file}")

def overlay_songs(song1, song2, output_file):
    """
    Overlay (mix) two audio files together.
    
    :param song1: Path to the first audio file
    :param song2: Path to the second audio file
    :param output_file: Path to save the resulting audio file
    """
    #load both audio files
    audio1, sr1 = librosa.load(song1, sr=None)
    audio2, sr2 = librosa.load(song2, sr=None)

    #resample to make sure both have the same sample rate
    if sr1 != sr2:
        audio2 = librosa.resample(audio2, orig_sr=sr2, target_sr=sr1)
        sr2 = sr1

    #match the lengths of audio files
    min_len = min(len(audio1), len(audio2))
    audio1 = audio1[:min_len]
    audio2 = audio2[:min_len]

    #overlay audio files by averaging their waveforms
    mixed_audio = (audio1 + audio2) / 2

    #save the mixed audio to a file
    sf.write(output_file, mixed_audio, sr1)
    print(f"Overlayed audio saved to: {output_file}")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python script.py change_tempo <input_file> <output_file> <tempo_factor>")
        print("  python script.py overlay_songs <song1> <song2> <output_file>")
        sys.exit(1)

    command = sys.argv[1]
    try:
        if command == "change_tempo":
            if len(sys.argv) != 5:
                print("Usage: python script.py change_tempo <input_file> <output_file> <tempo_factor>")
                sys.exit(1)
            input_file = sys.argv[2]
            output_file = sys.argv[3]
            tempo = float(sys.argv[4])
            change_tempo(input_file, output_file, tempo)

        elif command == "overlay_songs":
            if len(sys.argv) != 5:
                print("Usage: python script.py overlay_songs <song1> <song2> <output_file>")
                sys.exit(1)
            song1 = sys.argv[2]
            song2 = sys.argv[3]
            output_file = sys.argv[4]
            overlay_songs(song1, song2, output_file)

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
