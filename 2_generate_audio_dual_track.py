import pandas as pd
import random
import os
import asyncio
import edge_tts
from pydub import AudioSegment

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
    asyncio.run(communicate.save(ruta_salida))

# Sequence audio generation
print("Generating synchronized stereo conversation audio...")
df = pd.read_csv("dataset_atc_turnos.csv")

if not os.path.exists("temp_audio"):
    os.makedirs("temp_audio")

asignacion_voces = {}

# Speaker separated tracks
pista_pilotos = AudioSegment.empty()
pista_atc = AudioSegment.empty()

# Iterate through the csv for the sentences
for index, row in df.iterrows():
    texto = row['text']
    speaker = row['speaker']
    callsign = row['target_callsign']
    
    # Assign voice
    if speaker == "CONTROLLER":
        voz_actual = VOICE_ATC
    else:
        if callsign not in asignacion_voces:
            asignacion_voces[callsign] = random.choice(VOICES_PILOTS)
        voz_actual = asignacion_voces[callsign]
        
    temp_path = f"temp_audio/msg_{index}.wav"
    
    # Generate and temporally save the audio segment
    generar_audio_tts(texto, voz_actual, temp_path)
    audio_limpio = AudioSegment.from_file(temp_path)
    
    # Obtenemos la duración exacta de la frase hablada en milisegundos
    duracion_frase = len(audio_limpio)
    silencio_frase = AudioSegment.silent(duration=duracion_frase)
    
    # 2. LÓGICA DE SINCRONIZACIÓN
    if speaker == "PILOT":
        # Piloto habla, ATC calla
        pista_pilotos += audio_limpio
        pista_atc += silencio_frase
    elif speaker == "CONTROLLER":
        # ATC habla, Piloto calla
        pista_atc += audio_limpio
        pista_pilotos += silencio_frase
        
    # Append random silence gap to BOTH tracks to keep them synced
    pausa_ms = random.randint(500, 2500)
    silencio_pausa = AudioSegment.silent(duration=pausa_ms)
    
    pista_pilotos += silencio_pausa
    pista_atc += silencio_pausa
    
    if (index + 1) % 10 == 0:
        print(f"Completadas {index + 1}/{len(df)}...")

# Save results
salida_pilotos = "simulacion_pilotos_sync.wav"
salida_atc = "simulacion_controlador_sync.wav"

pista_pilotos.export(salida_pilotos, format="wav")
pista_atc.export(salida_atc, format="wav")

print(f"Syntetic audios perfectly synced and exported!")
print(f"-> {salida_pilotos}")
print(f"-> {salida_atc}")