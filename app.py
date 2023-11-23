import os

import moviepy.editor as mp
import speech_recognition as sr
from flask import Flask, render_template, request
from pydub import AudioSegment

app = Flask(__name__)

# Function to convert video to audio and return the path to the audio file


def extract_audio_from_video(video_path):
    video = mp.VideoFileClip(video_path)
    audio = video.audio
    audio_path = "temp_audio.wav"
    audio.write_audiofile(audio_path)
    video.close()  # Close the video file
    return audio_path

# Function to convert MP3 to WAV using PyDub


def convert_mp3_to_wav(mp3_file, wav_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")


# Set up the speech recognizer
r = sr.Recognizer()
easter_egg_trigger = "The weather is lovely today"
random_phrase = "I heard there might be rain later"


@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = ""
    if request.method == 'POST':
        input_type = request.form.get('input_type')

        if input_type == 'microphone':
            # Microphone input
            with sr.Microphone() as source:
                print("Say something...")
                audio = r.listen(source, timeout=5)
                try:
                    transcript = r.recognize_google(audio)
                    if easter_egg_trigger.lower() in transcript.lower():
                        transcript = "VANI"
                except sr.UnknownValueError:
                    transcript = "Speech Recognition could not understand audio"
                except sr.RequestError as e:
                    transcript = f"Could not request results from Google Web Speech API; {e}"

        elif input_type == 'audio_file':
            # Audio file input (provide the path to your MP3 audio file)
            mp3_file_path = request.files['audio_file']
            if mp3_file_path:
                mp3_file_path.save("temp_audio.mp3")
                convert_mp3_to_wav("temp_audio.mp3", "temp_audio.wav")

                with sr.AudioFile("temp_audio.wav") as source:
                    audio = r.record(source)

                try:
                    transcript = r.recognize_google(audio)
                except sr.UnknownValueError:
                    transcript = "Speech Recognition could not understand audio"
                except sr.RequestError as e:
                    transcript = f"Could not request results from Google Web Speech API; {e}"
                finally:
                    if os.path.exists("temp_audio.mp3"):
                        os.remove("temp_audio.mp3")
                    if os.path.exists("temp_audio.wav"):
                        os.remove("temp_audio.wav")

        elif input_type == 'video_file':
            # Video file input (provide the path to your video file)
            video_file = request.files['video_file']
            if video_file:
                video_file_path = "temp_video.mp4"  # You can save the file temporarily
                video_file.save(video_file_path)

                # Extract audio from video and get the audio file path
                audio_file_path = extract_audio_from_video(video_file_path)

                with sr.AudioFile(audio_file_path) as source:
                    audio = r.record(source)

                try:
                    transcript = r.recognize_google(audio)
                except sr.UnknownValueError:
                    transcript = "Speech Recognition could not understand audio"
                except sr.RequestError as e:
                    transcript = f"Could not request results from Google Web Speech API; {e}"
                finally:
                    if os.path.exists(video_file_path):
                        os.remove(video_file_path)
                    if os.path.exists(audio_file_path):
                        os.remove(audio_file_path)

    return render_template('index.html', transcript=transcript)


@app.route('/save_transcript', methods=['POST'])
def save_transcript():
    transcript = request.form.get('transcript')
    filename = 'transcript.txt'
    i = 1
    while os.path.exists(filename):
        base, ext = os.path.splitext(filename)
        filename = f"{base}_{i}{ext}"
        i += 1
    with open(filename, 'w') as f:
        f.write(transcript)
    return 'Transcript saved.'


if __name__ == '__main__':
    app.run(debug=True)
