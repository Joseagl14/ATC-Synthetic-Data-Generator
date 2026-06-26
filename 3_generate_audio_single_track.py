import pandas as pd
import random
import os
import asyncio
import edge_tts
from pydub import AudioSegment
from pydub.generators import WhiteNoise

# Voices configuration
VOICE_ATC = "en-GB-RyanNeural"

VOICES_PILOTS = [
    "en-US-GuyNeural", 
    "en-IE-ConnorNeural", 
    "en-AU-WilliamNeural", 
    "en-CA-LiamNeural",
    "en-NZ-MitchellNeural",
    "en-GB-ThomasNeural",
    "en-US-EricNeural"
]

# Voice modulation
def generar_audio_tts(texto, voz, ruta_salida):
    communicate = edge_tts.Communicate(texto, voz, rate="+10%")
    asyncio.run(communicate.save(ruta_salida))      # Async in order to wait for the previous audio and don't overlap interactions

# Sequence audio generation
print("Generating conversation audio...")
df = pd.read_csv("dataset_atc_turnos.csv")

if not os.path.exists("temp_audio"):
    os.makedirs("temp_audio")

asignacion_voces = {}
audio_maestro = AudioSegment.empty()        # All interactions go inside the same audio to simulate a segment

# Iterate through the csv for the sentences
for index, row in df.iterrows():
    texto = row['text']
    speaker = row['speaker']
    callsign = row['target_callsign']
    
    # Assign voice
    if speaker == "CONTROLLER":
        voz_actual = VOICE_ATC
    else:
        # For pilot random voice
        if callsign not in asignacion_voces:
            asignacion_voces[callsign] = random.choice(VOICES_PILOTS)
        voz_actual = asignacion_voces[callsign]
        
    temp_path = f"temp_audio/msg_{index}.wav"
    
    # Generate and temporally save the audio segment
    generar_audio_tts(texto, voz_actual, temp_path)
    audio_limpio = AudioSegment.from_file(temp_path)
    
    # Append audio segment to "master" audio with random silence gaps
    audio_maestro += audio_limpio
    pausa = random.randint(500, 2500)
    audio_maestro += AudioSegment.silent(duration=pausa)
    
    if (index + 1) % 10 == 0:
        print(f"Completadas {index + 1}/{len(df)}...")

# Save final result
salida = "simulacion_radar_limpia.wav"
audio_maestro.export(salida, format="wav")
print("Syntetic audio completely generated")