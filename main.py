import moviepy.editor as mp
import speech_recognition as sr
from datetime import timedelta
from art import *
from colorama import *

# Function to transcribe audio
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        transcription = recognizer.recognize_google(audio)
        return transcription
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

# Function to extract timestamps for each word
def extract_word_timestamps(transcription, audio_duration):
    words = transcription.split()
    word_duration = audio_duration / len(words)
    word_timestamps = [(timedelta(seconds=i * word_duration)).total_seconds() for i in range(len(words))]
    formatted_timestamps = [str(timedelta(seconds=timestamp)).split('.')[0] for timestamp in word_timestamps]
    return formatted_timestamps

# Function to write transcription with timestamps to a file
# Function to write transcription with timestamps to a file
def write_transcription_with_timestamps(transcription, timestamps, output_file,outer_put):
    with open(output_file, "w") as file:
        word_count = 0
        line = ""
        for word, timestamp in zip(transcription.split(), timestamps):
            line += f"{word} - {timestamp}   "
            word_count += 1
            if word_count == 20:
                file.write(line + "\n")
                print(Fore.GREEN)
                print("*", line)
                print(Fore.GREEN)
                line = ""
                word_count = 0
        # Write any remaining words if the total count is not a multiple of 20
        if line:
            file.write(line + "\n")
            print(Fore.GREEN)
            print("*", line)
            print(Fore.GREEN)
    with open(outer_put, "w") as file:
        word_count = 0
        line = ""
        for word, timestamp in zip(transcription.split(), timestamps):
            line += f"{word} "
            word_count += 1
            if word_count == 15:
                file.write(line + "\n")
                print(Fore.GREEN)
                print("*", line)
                print(Fore.GREEN)
                line = ""
                word_count = 0
        # Write any remaining words if the total count is not a multiple of 20
        if line:
            file.write(line + "\n")
            print(Fore.GREEN)
            print("*", line)
            print(Fore.GREEN)        



def main():
    print(Fore.MAGENTA)
    tprint('LMC Video Transcriber')
    # Load video file
    print(Fore.CYAN)
    video_path = input("Enter the video path: ")
    video = mp.VideoFileClip(video_path)
    print(Fore.BLUE)
    # Extract audio from video
    audio_path = "audio.wav"
    video.audio.write_audiofile(audio_path)
    print(Fore.BLACK)
    # Transcribe audio
    transcription = transcribe_audio(audio_path)

    # Get audio duration
    audio_duration = video.duration

    # Extract timestamps for each word
    word_timestamps = extract_word_timestamps(transcription, audio_duration)
    print(Fore.GREEN)
    # Write transcription with timestamps to a file
    output_file = "full_words_with_time.txt"
    outer_put = 'full_words_without_time.txt'
    write_transcription_with_timestamps(transcription, word_timestamps, output_file,outer_put)

    print("Transcription with timestamps saved to", output_file)
    input('Enter ....')

if __name__ == "__main__":
    main()
