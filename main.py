from pydub import AudioSegment
import argparse

class WavTempoEditor:
    def __init__(self, input_file, output_file, speed):
        """
        Initialize the WavTempoEditor with input and output file paths and speed factor.

        Parameters:
        input_file (str): Path to the input .wav file.
        output_file (str): Path to save the output .wav file.
        speed (float): Speed factor to adjust tempo. Values > 1 increase tempo, < 1 decrease tempo.
        """
        self.input_file = input_file
        self.output_file = output_file
        self.speed = speed

    def load_audio(self):
        """Load the .wav file."""
        return AudioSegment.from_wav(self.input_file)

    def change_tempo(self, audio):
        """
        Change the tempo of the loaded .wav file without changing the pitch.

        Parameters:
        audio (AudioSegment): The original audio segment.

        Returns:
        AudioSegment: The modified audio segment with adjusted tempo.
        """
        # Adjust the playback speed by changing frame rate
        new_frame_rate = int(audio.frame_rate * self.speed)
        modified_audio = audio._spawn(audio.raw_data, overrides={'frame_rate': new_frame_rate})
        return modified_audio.set_frame_rate(audio.frame_rate)

    def save_audio(self, audio):
        """Save the modified audio to the output file."""
        audio.export(self.output_file, format="wav")

    def process_audio(self):
        """Load, modify, and save the .wav file with the new tempo."""
        audio = self.load_audio()
        modified_audio = self.change_tempo(audio)
        self.save_audio(modified_audio)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Edit the tempo of a .wav file.")
    parser.add_argument("input_file", type=str, help="Path to the input .wav file.")
    parser.add_argument("output_file", type=str, help="Path to save the output .wav file.")
    parser.add_argument("speed", type=float, help="Speed factor for tempo adjustment (e.g., 1.5 for 50% faster).")

    args = parser.parse_args()

    editor = WavTempoEditor(args.input_file, args.output_file, args.speed)
    editor.process_audio()
    print(f"Tempo adjusted and saved to {args.output_file}")