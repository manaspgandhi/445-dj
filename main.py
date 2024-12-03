import sys
import librosa
import soundfile as sf

def change_tempo(input_file, output_file, tempo):
    """
    Change the tempo of an audio file without changing the pitch.
    
    :param input_file: Path to the input audio file
    :param output_file: Path to save the output audio file
    :param tempo: Tempo adjustment factor (e.g., 1.5 for 150% tempo)
    """
    # Load the audio file
    audio, sample_rate = librosa.load(input_file, sr=None)

    # Adjust tempo
    adjusted_audio = librosa.effects.time_stretch(audio, rate=tempo)

    # Save the modified audio to a new file
    sf.write(output_file, adjusted_audio, sample_rate)
    print(f"Tempo-adjusted audio saved to: {output_file}")

def main():
    if len(sys.argv) != 4:
        print("Usage: python change_tempo.py <input_file> <output_file> <tempo_factor>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    tempo = float(sys.argv[3])

    try:
        change_tempo(input_file, output_file, tempo)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
