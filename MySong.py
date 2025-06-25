import os
import random
from gtts import gTTS
from pydub import AudioSegment
import numpy as np
import scipy.io.wavfile as wavfile

# List of Free Fire character names and motivational Sahur messages
FF_CHARACTERS = ["Kelly", "Maxim", "Moco", "Andrew", "Chrono"]
SAHUR_MESSAGES = [
    "Rise and shine, it's Sahur time!",
    "Grab your dates, don't be late!",
    "Fuel up for fasting, you're a champ!",
    "Sahur squad, let's do this!",
    "Time to eat before the dawn!"
]

def generate_drum_beat(duration_ms=1000, tempo="fast"):
    """Generate a simple drum beat as a WAV file using numpy."""
    sample_rate = 44100  # Hz
    t = np.linspace(0, duration_ms / 1000, int(sample_rate * duration_ms / 1000), False)
    freq = 100 if tempo == "fast" else 80  # Lower frequency for slower beat
    drum = 0.5 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 5)
    drum = (drum * 32767).astype(np.int16)  # Convert to 16-bit PCM
    wavfile.write("sounds/drum_beat.wav", sample_rate, drum)
    return AudioSegment.from_wav("sounds/drum_beat.wav")

def create_sahur_alarm(character, message, beat_style="fast"):
    """Create a Sahur alarm audio file with character voice, jingle, message, and drum beat."""
    # Create the "Tung Tung Tung" jingle
    tung_repeats = random.randint(2, 4)  # Randomize repetitions
    tung_chant = "Tung Tung Tung, " * tung_repeats
    jingle = f"The Tung Tung Sahur goes {tung_chant} The Tung Tung Sahur goes Tung Tung Tung, all through the town!"
    
    # Combine character greeting, jingle, and message
    script = f"Yo, this is {character}! {jingle} {message}"
    
    # Generate text-to-speech audio
    tts = gTTS(text=script, lang='en')
    tts.save("temp_tts.mp3")
    voice_audio = AudioSegment.from_mp3("temp_tts.mp3")
    
    # Load or generate drum beat
    drum_path = "sounds/drum_beat.wav"
    if os.path.exists(drum_path):
        drum_audio = AudioSegment.from_wav(drum_path)
    else:
        drum_audio = generate_drum_beat(tempo=beat_style)
    
    # Mix audio: overlay drum beat at the start and loop it softly in the background
    final_audio = AudioSegment.silent(duration=len(voice_audio) + 1000)
    final_audio = final_audio.overlay(drum_audio, position=0)
    final_audio = final_audio.overlay(voice_audio, position=500)
    
    # Add a softer drum loop in the background
    soft_drum = drum_audio - 10  # Reduce volume by 10dB
    for i in range(1, int(len(voice_audio) / len(drum_audio))):
        final_audio = final_audio.overlay(soft_drum, position=i * len(drum_audio))
    
    # Export the final alarm
    output_file = "tung_sahur_alarm.mp3"
    final_audio.export(output_file, format="mp3")
    print(f"Alarm saved as {output_file}")
    
    # Clean up temporary files
    if os.path.exists("temp_tts.mp3"):
        os.remove("temp_tts.mp3")
    if os.path.exists("sounds/drum_beat.wav"):
        os.remove("sounds/drum_beat.wav")

def main():
    print("Welcome to the Tung Tung Tung Sahur Alarm Generator!")
    print("Create a funny Sahur wake-up alarm with Free Fire vibes and a catchy jingle.")
    
    # Get user inputs
    character = input(f"Choose a Free Fire character ({', '.join(FF_CHARACTERS)}): ").strip()
    if character not in FF_CHARACTERS:
        character = random.choice(FF_CHARACTERS)
        print(f"Invalid character, using {character} instead.")
    
    message = input("Enter a motivational Sahur message (or press Enter for a random one): ").strip()
    if not message:
        message = random.choice(SAHUR_MESSAGES)
    
    beat_style = input("Choose beat style (fast/slow): ").strip().lower()
    if beat_style not in ["fast", "slow"]:
        beat_style = "fast"
        print("Invalid beat style, using fast beat.")
    
    # Create the alarm
    os.makedirs("sounds", exist_ok=True)
    create_sahur_alarm(character, message, beat_style)
    print("Upload this to GitHub and share the Sahur jingle with the world!")

if __name__ == "__main__":
    main()