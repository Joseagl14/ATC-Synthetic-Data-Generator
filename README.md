# ATC Synthetic Data Generator ✈️

This repository contains the Python-based generation engine developed for my Bachelor's Thesis: *"Development of an AI Assistant for ATC based on Speech Recognition and Machine Learning"*. 

It generates labeled synthetic Air Traffic Control (ATC) conversational pairs, specifically tailored for En-Route (cruise) operations. The output is optimized for training and evaluating Automatic Speech Recognition (ASR) and Natural Language Understanding (NLU) models.

A sample dataset created using this tool can be found at: https://huggingface.co/jacktol/whisper-large-v3-finetuned-for-ATC

## Features
* **Template-based Generation:** Dynamic injection of aeronautical variables (callsigns, waypoints and flight levels) into standard ATC phraseology.
* **Text-to-Speech (TTS):** Integration with `edge-tts` for realistic, multi-speaker voice synthesis.
* **Dual-Channel Output:** Generates perfectly synchronized but isolated audio tracks for Controller and Pilot communications via `pydub`.
* **Automatic Labeling:** Outputs a `.csv` file with Ground-Truth labels for Intent and Caller entities.

## Dataset Availability
The complete synthetic dataset generated for this project (> 6 hours of audio) is publicly available on Zenodo:
**[Link to your Zenodo/HuggingFace Dataset will go here]**

### ⚠️ System Requirements: FFmpeg
This project uses `pydub` for audio manipulation, which requires **FFmpeg** to be installed on your system and added to your environment PATH.
* **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add the `bin` folder to your system PATH.
* **macOS:** Run `brew install ffmpeg`
* **Linux:** Run `sudo apt install ffmpeg`

## 🛠️ Installation

**1. Clone the repository**
git clone https://github.com/Joseagl14/ATC-Synthetic-Data-Generator.git
cd ATC-Synthetic-Data-Generator

**2. Install Python dependencies**
Make sure you have Python installed. Then, install the required libraries using `pip`:
pip install -r requirements.txt

**3. System Requirements (FFmpeg)**
This project uses the `pydub` library for audio manipulation, which strictly requires **FFmpeg** to be installed on your system and added to your environment PATH. If you skip this step, the audio generation scripts will crash.
* **Windows:** Download from https://www.gyan.dev/ffmpeg/builds/ and add the `bin` folder to your system PATH.
* **macOS:** Run `brew install ffmpeg`
* **Linux:** Run `sudo apt install ffmpeg`

## 📖 Usage
First, run the text generation script to create the conversational pairs:
python 1_generate_text_dataset.py

Then, generate the synchronized stereo audio files:
python 2_generate_audio_dual_track.py

*(Note: If you prefer a single master audio track, run `3_generate_audio_single_track.py` instead).*

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
