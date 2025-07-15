# 🧠 Image Caption App V2

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![CustomTkinter](https://img.shields.io/badge/CustomTkinter-GUI-brightgreen)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![GitHub Repo stars](https://img.shields.io/github/stars/Nahid305/image-caption-app-v2?style=social)](https://github.com/Nahid305/image-caption-app-v2)
[![Made With ❤️](https://img.shields.io/badge/Made%20with-%F0%9F%96%A4-red)](#)

> A smart desktop application that generates AI-based image captions from uploaded or webcam-captured photos, with voice interaction, multilingual TTS, and a modern GUI.

---

## 🚀 Features

- 🔐 **Secure Login/Signup** using bcrypt
- 🖼️ Upload or **capture images** from webcam
- 🤖 **AI-powered captions** via Hugging Face (Vision Encoder + GPT2)
- 🌍 **Multilingual text-to-speech** using gTTS + pygame
- 🎤 **Voice command** support
- 🕘 **Caption history log** in CSV
- 🎨 **Modern UI** with CustomTkinter
- 💻 **.exe bundling** with PyInstaller

---

## 📂 Folder Structure

```bash
image_caption_app_v2/
├── main.py                 ← Entry point
├── gui.py                  ← GUI screens (login, app)
├── auth.py                 ← Authentication logic
├── model.py                ← Caption generation model
├── tts.py                  ← Text-to-speech handler
├── voice_input.py          ← Speech recognition input
├── webcam.py               ← Webcam capture module
├── history.py              ← Caption logs manager
├── users.json              ← Login credentials
├── captions.csv            ← Caption history
├── requirements.txt
├── icon.ico                ← App icon
└── demo.gif                ← Demo video/gif

⚙️ Installation & Usage
1. Clone the Repository
  git clone https://github.com/Nahid305/image-caption-app-v2.git
  cd image-caption-app-v2
2. Install Requirements
  pip install -r requirements.txt
3. Run the App
  python main.py

🧠 Tech Stack
Frontend: CustomTkinter, Tkinter

Backend: Python, HuggingFace Transformers

TTS: gTTS + Pygame

Voice Input: SpeechRecognition

Camera: OpenCV

Security: bcrypt

📄 License
This project is licensed under the MIT License. See the LICENSE file.

👤 Author
Nahid Naushad Ansari
🔗 GitHub
💼 LinkedIn

⭐ Show Your Support
If you found this project useful, please ⭐ star the repo and share it!

📌 Future Ideas
⬆️ Cloud storage integration (Firebase, Drive)

📱 Convert into Android App (using Kivy)

📊 Real-time emotion-based captioning

🗂️ PDF caption export


