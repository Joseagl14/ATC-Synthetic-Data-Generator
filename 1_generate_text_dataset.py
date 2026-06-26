import pandas as pd
import random
import os

# Read the callsigns list from the csv file
callsigns_path = "callsigns.csv" 
df_callsigns_full = pd.read_csv(callsigns_path)
callsigns = df_callsigns_full["text"].values

# Create a list of "spoken" waypoints
waypoints = ["arbek","balde","caspe","charlie lima echo","golf india romeo","lesbas","mike juliett victor","mopas","romeo echo sierra","salas","sierra lima lima","sopet","vibok","victor lima alpha","victor novembre victor"]

# Define random variables for instructions generation
flight_levels = ["one eight zero", "two two zero", "three five zero", "one zero zero", "two seven zero", "two four five"]
headings = ["zero niner zero", "one eight zero", "two seven zero", "three six zero", "zero one two", "zero seven niner", "one three five", "two four zero", "two eight seven", "two niner seven", "three four niner"]
speeds = ["two five zero", "three hundred", "two eight zero", "two hundred", "two one zero"]
descend_ratios = ["two thousand", "three thousand", "two thousand five hundred"]

# Messages generation templates
templates_pilot_greeting = [
    "{centro} {callsign} flight level {level} good morning",
    "good morning {centro} {callsign} maintaining flight level {level}",
    "hola {centro} {callsign} flight level {level}",
    "{centro} good morning {callsign} passing flight level {level} climbing flight level {level}",
    "{centro} {callsign} leaving flight level {level} for flight level {level} good afternoon",
    "{callsign} good morning passing flight level {level} descending flight level {level}",
    "{centro} {callsign} good morning flight level {level} direct to {waypoint}",
    "good afternoon {centro} {callsign} passing flight level {level} climbing flight level {level} direct {waypoint}",
    "{centro} {callsign} maintaining flight level {level} heading {heading} good morning",
    "{centro} {callsign} flight level {level} good evening",
    "good evening {centro} {callsign} maintaining flight level {level}",
    "{centro} {callsign} flight level {level} good night",
    "good night {centro} {callsign} maintaining flight level {level}",
]

templates_atc_greeting = [
    "{callsign} identified good morning",
    "good morning {callsign} identified"
]

templates_atc_other = [
    "{callsign} descend flight level {level}",
    "climb flight level {level} {callsign}",
    "{callsign} cleared direct to {waypoint}",
    "{callsign} speed {speed} knots",
    "{callsign} descend flight level {level} descend rate {rate} feet per minute"
]

templates_pilot_other = [
    "flight level {level} {callsign}",
    "direct to {waypoint} {callsign} thank you",
    "speed {speed} {callsign}",
    "descend rate {rate} {callsign}"
]

# Messages sequence generator
def generate_messages_sequence(num_sentences):
    dataset = []
    
    for _ in range(num_sentences):
        # 2 aircraft interacting - One greeting and another other communication
        avion_1 = random.choice(callsigns)
        avion_2 = random.choice([c for c in callsigns if c != avion_1])
        
        # Turn 1 - Pilot Greeting
        turn1 = []
        texto_p1_greet = random.choice(templates_pilot_greeting).format(centro="barcelona control", callsign=avion_1, level=random.choice(flight_levels), waypoint=random.choice(waypoints), heading=random.choice(headings))
        turn1.append({"speaker": "PILOT", "text": texto_p1_greet.upper(), "target_callsign": avion_1, "intent": "GREETING"})
        
        # Turn 1 - ATCo Greeting
        texto_atc_greet = random.choice(templates_atc_greeting).format(callsign=avion_1)
        turn1.append({"speaker": "CONTROLLER", "text": texto_atc_greet.upper(), "target_callsign": avion_1, "intent": "GREETING"})
        
        # Turn 2 - ATCo Other Order
        turn2 = []
        texto_atc_other = random.choice(templates_atc_other).format(
            callsign=avion_2, level=random.choice(flight_levels), waypoint=random.choice(waypoints), speed=random.choice(speeds), rate=random.choice(descend_ratios))
        turn2.append({"speaker": "CONTROLLER", "text": texto_atc_other.upper(), "target_callsign": avion_2, "intent": "OTHER"})
        
        # Turn 2 - Pilot Response
        texto_p2_other = random.choice(templates_pilot_other).format(
            callsign=avion_2, level=random.choice(flight_levels), waypoint=random.choice(waypoints), speed=random.choice(speeds), rate=random.choice(descend_ratios))
        turn2.append({"speaker": "PILOT", "text": texto_p2_other.upper(), "target_callsign": avion_2, "intent": "OTHER"})

        dataset.append(turn1)
        dataset.append(turn2)
    
    random.shuffle(dataset)     # This way we avoid pattern bias

    flat_dataset = []
    for turno in dataset:
        flat_dataset.extend(turno)

    return flat_dataset

# Generation of the dataset
print("Generating the syntetic dataset...")
datos = generate_messages_sequence(num_sentences=500) 
df_completo = pd.DataFrame(datos)

df_completo.to_csv("dataset_atc_turnos.csv", index=False)
print("Dataset correctly exported!")