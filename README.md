# ATC Synthetic Data Generator ✈️

This repository contains the Python-based generation engine developed for my Bachelor's Thesis: *"Development of an AI Assistant for ATC based on Speech Recognition and Machine Learning"*. 

It generates labeled synthetic Air Traffic Control (ATC) conversational pairs, specifically tailored for En-Route (cruise) operations. The output is optimized for training and evaluating Automatic Speech Recognition (ASR) and Natural Language Understanding (NLU) models.

## Features
* **Template-based Generation:** Dynamic injection of aeronautical variables (callsigns, waypoints and flight levels) into standard ATC phraseology.
* **Text-to-Speech (TTS):** Integration with `edge-tts` for realistic, multi-speaker voice synthesis.
* **Dual-Channel Output:** Generates perfectly synchronized but isolated audio tracks for Controller and Pilot communications via `pydub`.
* **Automatic Labeling:** Outputs a `.csv` file with Ground-Truth labels for Intent and Caller entities.

## Dataset Availability
The complete synthetic dataset generated for this project (> 6 hours of audio) is publicly available on Zenodo:
**[Link to your Zenodo/HuggingFace Dataset will go here]**

## 🛠️ Installation
1. Clone this repository:
   ```bash
   git clone [https://github.com/Joseagl14/ATC-Synthetic-Data-Generator.git](https://github.com/Joseagl14/ATC-Synthetic-Data-Generator.git)
