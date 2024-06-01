import moviepy.editor as mp
import speech_recognition as sr
from datetime import timedelta
from art import *
from colorama import *
import tkinter as tk
from tkinter import filedialog, messagebox

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
def write_transcription_with_timestamps(transcription, timestamps, output_file, outer_put):
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

def open_file_dialog():
    filename = filedialog.askopenfilename()
    return filename

def process_files():
    video_path = video_path_entry.get()
    audio_path = "audio.wav"

    try:
        # Load video file
        video = mp.VideoFileClip(video_path)

        # Extract audio from video
        video.audio.write_audiofile(audio_path)

        # Transcribe audio
        transcription = transcribe_audio(audio_path)

        # Get audio duration
        audio_duration = video.duration

        # Extract timestamps for each word
        word_timestamps = extract_word_timestamps(transcription, audio_duration)

        # Write transcription with timestamps to files
        output_file = "full_words_with_time.txt"
        outer_put = 'full_words_without_time.txt'
        write_transcription_with_timestamps(transcription, word_timestamps, output_file, outer_put)

        messagebox.showinfo("Success", "Transcription completed. Files saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# GUI setup
root = tk.Tk()
root.title("LMC Video Transcriber")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

video_path_label = tk.Label(main_frame, text="Video Path:")
video_path_label.grid(row=0, column=0, sticky="w")

video_path_entry = tk.Entry(main_frame, width=50)
video_path_entry.grid(row=0, column=1)

browse_button = tk.Button(main_frame, text="Browse", command=lambda: video_path_entry.insert(tk.END, open_file_dialog()))
browse_button.grid(row=0, column=2)

process_button = tk.Button(main_frame, text="Process Files", command=process_files)
process_button.grid(row=1, column=1, pady=10)

root.mainloop()
