# 🎬 Video Downloader

A simple video downloader built with Python and [yt-dlp](https://github.com/yt-dlp/yt-dlp). Just paste a link and download the video (or only the audio) to your device.

## ✨ Features

- Download from YouTube and thousands of other sites supported by yt-dlp
- Option to select video quality (best, 1080p, 720p, 480p, ...)
- Option to download audio only (MP3 / M4A)
- Playlist download support
- Shows download progress
- Works on Windows, Linux, macOS, and Android (Termux)

## 📋 Requirements

- Python 3.9 or newer
- yt-dlp
- FFmpeg (for merging video + audio and for MP3 conversion)
- Node.js or Deno (some sites require yt-dlp to have a JS runtime)

## 🚀 Installation

### Windows / Linux / macOS

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
pip install -U yt-dlp
```

Install FFmpeg:

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

Then paste the video link when the program prompts you, and choose the quality / format.

> Note: Replace `main.py` with the name of your own main script.

## 🔄 Updating yt-dlp

Websites frequently change their systems, so if a download fails, the first thing to do is update yt-dlp:

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
- [ ] In-app button to update yt-dlp
- [ ] Integration with Node.js / Deno runtime support
- [ ] Download history

## ⚠️ Disclaimer

This tool is intended for personal and educational use only. Only download content that you own or have permission to download. Responsibility for copyright and website Terms of Service lies with the user.

## 🤝 Contributing

Issues and pull requests are welcome. If you find a bug or have an idea, please open an issue.
