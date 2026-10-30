#!/usr/bin/env python3
"""
Video Downloader - PyQt5 GUI
-----------------------------
Backend: yt-dlp (YouTube, Facebook, Instagram, Twitter/X, Vimeo, waghera).

Install (agar pehle se nahi hai):
    pip install yt-dlp PyQt5

Run:
    python downloader_gui.py

NOTE: Sirf wahi video download karein jinke aap khud malik hain ya
jinhe download karne ki ijazat hai. Copyright-protected content bina
permission download karna platform ke ToS aur copyright law ke
khilaf ho sakta hai.
"""

import os
import sys

try:
    import yt_dlp
except ImportError:
    print("yt-dlp installed nahi hai. Pehle ye command chalayein:\n    pip install yt-dlp")
    sys.exit(1)

try:
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtWidgets import (
        QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
        QLineEdit, QPushButton, QComboBox, QTextEdit, QProgressBar,
        QFileDialog, QMessageBox, QGroupBox
    )
except ImportError:
    print("PyQt5 installed nahi hai. Pehle ye command chalayein:\n    pip install PyQt5")
    sys.exit(1)


# ----------------------------------------------------------------------
# Bundled resources (ffmpeg.exe / cookies.txt) — .py aur PyInstaller
# .exe dono cases me sahi path dhoond leta hai
# ----------------------------------------------------------------------
APP_DIR = os.path.dirname(os.path.abspath(__file__))


def get_resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(APP_DIR, filename)


FFMPEG_PATH = get_resource_path("ffmpeg.exe") if os.name == "nt" else ""
BUNDLED_COOKIES_PATH = get_resource_path("cookies.txt")


# ----------------------------------------------------------------------
# Background worker thread — GUI ko freeze hone se bachata hai
# ----------------------------------------------------------------------
class DownloadWorker(QThread):
    progress = pyqtSignal(int, str)     # percent, status text
    log = pyqtSignal(str)               # plain log line
    link_started = pyqtSignal(str, int, int)   # url, index, total
    link_done = pyqtSignal(str, bool, str)     # url, success, error msg
    all_done = pyqtSignal(int, int)     # successful, total

    def __init__(self, urls, quality, output_dir, cookies_file=None):
        super().__init__()
        self.urls = urls
        self.quality = quality
        self.output_dir = output_dir
        self.cookies_file = cookies_file
        self._stop_requested = False

    def stop(self):
        self._stop_requested = True

    def _progress_hook(self, d):
        if self._stop_requested:
            raise Exception("Cancelled by user")
        if d.get("status") == "downloading":
            percent_str = d.get("_percent_str", "0%").strip().replace("%", "")
            try:
                percent = int(float(percent_str))
            except ValueError:
                percent = 0
            speed = d.get("_speed_str", "").strip()
            eta = d.get("_eta_str", "").strip()
            self.progress.emit(percent, f"{percent}%  |  speed: {speed}  |  ETA: {eta}")
        elif d.get("status") == "finished":
            self.progress.emit(100, "Processing / merging...")

    def _build_opts(self):
        if self.quality == "audio":
            format_str = "bestaudio/best"
            postprocessors = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
            merge_fmt = None
        elif self.quality == "best":
            format_str = "bestvideo+bestaudio/best"
            postprocessors = []
            merge_fmt = "mp4"
        elif self.quality == "worst":
            format_str = "worstvideo+worstaudio/worst"
            postprocessors = []
            merge_fmt = "mp4"
        else:
            format_str = f"bestvideo[height<={self.quality}]+bestaudio/best[height<={self.quality}]"
            postprocessors = []
            merge_fmt = "mp4"

        opts = {
            "format": format_str,
            "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
            "postprocessors": postprocessors,
            "progress_hooks": [self._progress_hook],
            "quiet": True,
            "no_warnings": True,
            "js_runtimes": {"deno": {}, "node": {}},
        }
        if merge_fmt:
            opts["merge_output_format"] = merge_fmt

        # Bundled ffmpeg use karein agar mojood ho (.exe ke andar se)
        if os.path.exists(FFMPEG_PATH):
            opts["ffmpeg_location"] = FFMPEG_PATH

        # Cookies: pehle user ne jo file manually di ho wo use karein,
        # warna agar app ke sath bundled cookies.txt mojood ho to wo use karein
        if self.cookies_file:
            opts["cookiefile"] = self.cookies_file
        elif os.path.exists(BUNDLED_COOKIES_PATH):
            opts["cookiefile"] = BUNDLED_COOKIES_PATH

        return opts

    def run(self):
        os.makedirs(self.output_dir, exist_ok=True)
        total = len(self.urls)
        successful = 0

        for i, url in enumerate(self.urls, start=1):
            if self._stop_requested:
                self.log.emit("⏹ Download rok diya gaya.")
                break

            self.link_started.emit(url, i, total)
            self.progress.emit(0, "Shuru ho raha hai...")
            try:
                with yt_dlp.YoutubeDL(self._build_opts()) as ydl:
                    ydl.download([url])
                self.link_done.emit(url, True, "")
                successful += 1
            except Exception as e:
                self.link_done.emit(url, False, str(e))

        self.all_done.emit(successful, total)


# ----------------------------------------------------------------------
# Main window
# ----------------------------------------------------------------------
class DownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "downloads")
        self.cookies_file = ""
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("Video Downloader Created by Mesam Raza")
        self.resize(560, 500)

        layout = QVBoxLayout()

        # --- URL input ---
        layout.addWidget(QLabel("Video links comma se separate karein agar multiple hon:"))
        self.url_input = QTextEdit()
        self.url_input.setPlaceholderText("https://... , https://...")
        self.url_input.setFixedHeight(70)
        layout.addWidget(self.url_input)

        # --- Options row ---
        opts_box = QGroupBox("Options")
        opts_layout = QHBoxLayout()

        opts_layout.addWidget(QLabel("Quality:"))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems(["best", "1080", "720", "480", "360", "worst", "audio"])
        opts_layout.addWidget(self.quality_combo)

        opts_layout.addWidget(QLabel("Save to:"))
        self.output_label = QLineEdit(self.output_dir)
        self.output_label.setReadOnly(True)
        opts_layout.addWidget(self.output_label)
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self._choose_output_dir)
        opts_layout.addWidget(browse_btn)

        opts_box.setLayout(opts_layout)
        layout.addWidget(opts_box)

        # --- Cookies row (optional, for "sign in to confirm" errors) ---
        cookies_layout = QHBoxLayout()
        cookies_layout.addWidget(QLabel("Cookies file (optional):"))
        self.cookies_input = QLineEdit()
        self.cookies_input.setPlaceholderText("cookies.txt ka path (agar bot-check error aaye)")
        cookies_layout.addWidget(self.cookies_input)
        cookies_browse_btn = QPushButton("Browse...")
        cookies_browse_btn.clicked.connect(self._choose_cookies_file)
        cookies_layout.addWidget(cookies_browse_btn)
        layout.addLayout(cookies_layout)

        # --- Buttons ---
        btn_layout = QHBoxLayout()
        self.download_btn = QPushButton("⬇ Download")
        self.download_btn.clicked.connect(self._start_download)
        btn_layout.addWidget(self.download_btn)

        self.cancel_btn = QPushButton("⏹ Cancel")
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self._cancel_download)
        btn_layout.addWidget(self.cancel_btn)
        layout.addLayout(btn_layout)

        # --- Progress bar (percentage line) ---
        self.current_link_label = QLabel("")
        layout.addWidget(self.current_link_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Ready.")
        layout.addWidget(self.status_label)

        # --- Log area ---
        layout.addWidget(QLabel("Log:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        self.setLayout(layout)

    # ------------------------------------------------------------------
    def _choose_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Output folder chunein", self.output_dir)
        if directory:
            self.output_dir = directory
            self.output_label.setText(directory)

    def _choose_cookies_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "cookies.txt chunein", "", "Text Files (*.txt);;All Files (*)")
        if path:
            self.cookies_input.setText(path)

    def _log(self, text):
        self.log_output.append(text)

    # ------------------------------------------------------------------
    def _start_download(self):
        raw = self.url_input.toPlainText().strip()
        if not raw:
            QMessageBox.warning(self, "Link khali hai", "Pehle koi video link daalein.")
            return

        urls = [u.strip() for u in raw.split(",") if u.strip()]
        if not urls:
            QMessageBox.warning(self, "Link khali hai", "Koi valid link nahi mila.")
            return

        quality = self.quality_combo.currentText()
        cookies_file = self.cookies_input.text().strip() or None

        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.progress_bar.setValue(0)
        self.log_output.clear()
        self._log(f"Kul {len(urls)} link(s). Quality: {quality}")

        self.worker = DownloadWorker(urls, quality, self.output_dir, cookies_file)
        self.worker.progress.connect(self._on_progress)
        self.worker.link_started.connect(self._on_link_started)
        self.worker.link_done.connect(self._on_link_done)
        self.worker.all_done.connect(self._on_all_done)
        self.worker.start()

    def _cancel_download(self):
        if self.worker:
            self.worker.stop()
            self.cancel_btn.setEnabled(False)
            self.status_label.setText("Cancel ho raha hai...")

    # --- signal handlers ---
    def _on_link_started(self, url, index, total):
        self.current_link_label.setText(f"[{index}/{total}] {url}")
        self._log(f"\n--- [{index}/{total}] Shuru: {url}")

    def _on_progress(self, percent, status_text):
        self.progress_bar.setValue(percent)
        self.status_label.setText(status_text)

    def _on_link_done(self, url, success, error_msg):
        if success:
            self._log(f"✅ Mukammal: {url}")
        else:
            self._log(f"❌ Fail: {url}\n   Wajah: {error_msg}")

    def _on_all_done(self, successful, total):
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.status_label.setText(f"Khatam — {successful}/{total} kamyab.")
        self._log(f"\n=== Khatam: {successful}/{total} kamyab ===")
        QMessageBox.information(self, "Khatam", f"{successful}/{total} download kamyab hue.\nFolder: {self.output_dir}")


def main():
    app = QApplication(sys.argv)
    window = DownloaderApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
