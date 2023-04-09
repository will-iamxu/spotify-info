from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QProgressBar
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
from io import BytesIO
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import sys

def read_credentials(file_name):
    if getattr(sys, 'frozen', False):
        current_dir = sys._MEIPASS
    else:
        current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, "r") as f:
        credentials = {}
        for line in f:
            key, value = line.strip().split("=")
            credentials[key] = value
    return credentials

credentials = read_credentials("client.txt") #if you dont want it named client.txt for the credentials feel free to change it

client_id = credentials["client_id"]
client_secret = credentials["client_secret"]
redirect_uri = "http://localhost:8080/callback" #change maybe
scope = "user-read-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope))

class SpotifyCurrentSongApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Spotify Current Song")
        self.setStyleSheet("QWidget { background-color: #2c2c2c; } QLabel { color: #ffffff; }") #change color

        self.song_info_label = QLabel("", self)
        self.song_info_label.setFont(QFont("Segoe UI", 14))
        self.song_info_label.setAlignment(Qt.AlignCenter)
        self.song_info_label.setWordWrap(True)

        self.cover_art_label = QLabel(self)
        self.cover_art_label.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 100000)
        self.progress_bar.setStyleSheet("QProgressBar { background-color: #3C3C3C; border: 1px solid #000000; } QProgressBar::chunk { background-color: #00FF00; }") 
        
        self.elapsed_time_label = QLabel("", self)
        self.elapsed_time_label.setFont(QFont("Segoe UI", 12))
        self.elapsed_time_label.setAlignment(Qt.AlignLeft)

        self.remaining_time_label = QLabel("", self)
        self.remaining_time_label.setFont(QFont("Segoe UI", 12))
        self.remaining_time_label.setAlignment(Qt.AlignRight)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.elapsed_time_label)
        time_layout.addWidget(self.remaining_time_label)

        layout = QVBoxLayout()
        layout.addWidget(self.cover_art_label)
        layout.addWidget(self.song_info_label)
        layout.addLayout(time_layout)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_song_info)
        self.update_timer.start(100)

        self.setFixedSize(400, 500)

    def update_song_info(self):
        try:
            current_playback = sp.current_playback()
            if current_playback and current_playback["is_playing"]:
                track = current_playback["item"]

                song_info = f"{track['name']}\n{track['artists'][0]['name']}\nAlbum: {track['album']['name']}"

                self.song_info_label.setText(song_info)

                cover_art_url = track["album"]["images"][0]["url"]
                cover_art_data = requests.get(cover_art_url).content
                cover_art_pixmap = QPixmap()
                cover_art_pixmap.loadFromData(BytesIO(cover_art_data).read())
                self.cover_art_label.setPixmap(cover_art_pixmap.scaled(375, 375, Qt.KeepAspectRatio, Qt.SmoothTransformation))

                progress = current_playback['progress_ms']
                self.progress_bar.setRange(0, current_playback['item']['duration_ms'])
                self.progress_bar.setValue(progress)

                elapsed_ms = current_playback['progress_ms']
                elapsed_min, elapsed_sec = divmod(elapsed_ms // 1000, 60)
                elapsed_formatted = f"{elapsed_min:02d}:{elapsed_sec:02d}"
                self.elapsed_time_label.setText(elapsed_formatted)

                time_left_ms = current_playback['item']['duration_ms'] - current_playback['progress_ms']
                time_left_min, time_left_sec = divmod(time_left_ms // 1000, 60)
                time_left_formatted = f"{time_left_min:02d}:{time_left_sec:02d}"
                self.remaining_time_label.setText(time_left_formatted)

            else:
                self.song_info_label.setText("No song currently playing.")
                self.cover_art_label.clear()
                self.elapsed_time_label.clear()
                self.remaining_time_label.clear()
                self.progress_bar.reset()

        except Exception as e:
            print(e)
            self.song_info_label.setText("Error: Unable to fetch song info.")
            self.cover_art_label.clear()
            self.elapsed_time_label.clear()
            self.remaining_time_label.clear()
            self.progress_bar.reset()

app = QApplication(sys.argv)
window = SpotifyCurrentSongApp()
window.show()
sys.exit(app.exec_())
