# 🎬 Video Downloader

Python aur [yt-dlp](https://github.com/yt-dlp/yt-dlp) par bana hua aik simple video downloader. Sirf link paste karein aur video (ya sirf audio) apne device par download karein.

## ✨ Features

- YouTube aur yt-dlp ki support wali hazaron sites se download
- Video quality select karne ka option (best, 1080p, 720p, 480p, ...)
- Sirf audio (MP3 / M4A) download karne ka option
- Playlist download support
- Download progress dikhata hai
- Windows, Linux, macOS aur Android (Termux) par chalta hai

## 📋 Requirements

- Python 3.9 ya us se naya
- yt-dlp
- FFmpeg (video + audio merge karne aur MP3 conversion ke liye)
- Node.js ya Deno (kuch sites ke liye yt-dlp ko JS runtime chahiye hota hai)

## 🚀 Installation

### Windows / Linux / macOS

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -U yt-dlp
```

FFmpeg install karein:

```bash
# Windows (winget)
winget install ffmpeg

# Ubuntu / Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### Android (Termux)

```bash
pkg update && pkg upgrade
pkg install python ffmpeg nodejs git
pip install -U yt-dlp
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
termux-setup-storage
```

## ▶️ Usage

```bash
python main.py
```

Phir program ke kehne par video ka link paste karein aur quality / format choose karein.

> Note: `main.py` ki jagah apni main script ka naam likhein.

## 🔄 yt-dlp Update Karna

Sites aksar apna system change karti rehti hain, is liye agar download fail ho to sab se pehle yt-dlp update karein:

```bash
pip install -U yt-dlp
```

## 📁 Project Structure

```
<repo-name>/
├── main.py            # Main script
├── requirements.txt   # Dependencies
└── README.md
```

## 🗺️ Roadmap

- [ ] Android APK version
- [ ] App ke andar se yt-dlp update ka button
- [ ] Node.js / Deno runtime support ke saath integration
- [ ] Download history

## ⚠️ Disclaimer

Ye tool sirf personal aur educational use ke liye hai. Sirf wohi content download karein jis ka aap ko haq ho ya jis ki ijazat ho. Copyright aur websites ki Terms of Service ki zimmedari user par hai.

## 🤝 Contributing

Issues aur pull requests ka khair-maqdam hai. Koi bug mile ya idea ho to issue open karein.
