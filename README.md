# 🎵 Audio Processing Project

## 📖 Introduction
This project is an audio processing application built using the MVVM (Model-View-ViewModel) architecture. It provides functionalities for audio playback, equalization, and spectrum analysis.

## 🚀 Features
- 🎵 **Audio Player**: Play and manage audio files.
- 🎚️ **Equalizer**: Adjust audio frequencies for better sound quality.
- 📊 **Spectrum Analysis**: Visualize the audio spectrum.
- 🔧 **Core DSP Functions**: FFT, IIR, and FIR filtering.

## 🏗 Project Structure
```
MVVM/
│── model/                  # Data models
│   ├── __init__.py
│   ├── audio_player_model.py
│   ├── equalizer_model.py
│   ├── spectrum_model.py
│
│── view/                   # UI components
│   ├── __init__.py
│   ├── audio_player_view.py
│   ├── equalizer_view.py
│   ├── spectrum_view.py
│
│── modelview/              # Business logic
│   ├── __init__.py
│   ├── audio_player_viewmodel.py
│   ├── equalizer_viewmodel.py
│
│── core/                   # Core DSP processing
│   ├── fft.py
│   ├── iir.py
│   ├── fir.py
│
│── main.py                 # Application entry point
│── requirements.txt        # Dependencies
```

## 📦 Installation
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/audio-processing.git
cd audio-processing
```

### 2️⃣ Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## ▶️ Running the Application
```bash
python main.py
```

## 🛠 Core Functionalities
- `fft.py`: Implements Fast Fourier Transform for spectrum analysis.
- `iir.py`: Implements Infinite Impulse Response filters.
- `fir.py`: Implements Finite Impulse Response filters.

## 🧪 Running Unit Tests
```bash
pytest tests/
```

## 📌 Contribution
1. Fork the repository 🍴
2. Create a new branch (`git checkout -b feature/your-feature`) 🌱
3. Commit your changes (`git commit -m "Add new feature"`) ✅
4. Push to the branch (`git push origin feature/your-feature`) 🚀
5. Create a Pull Request 🔥

## 📜 License
This project is licensed under the [MIT License](LICENSE).

---
💡 **Contact:** If you have any questions, feel free to open an issue on GitHub! 🚀