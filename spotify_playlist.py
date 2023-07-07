import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Spotify Playlist Generator")
        self.setGeometry(100, 100, 400, 300)

        self.artists_label = QLabel("Artists:", self)
        self.artists_label.move(20, 20)

        self.artists_text = QLineEdit(self)
        self.artists_text.setGeometry(100, 20, 280, 30)

        self.playlist_label = QLabel("Playlist Name:", self)
        self.playlist_label.move(20, 70)

        self.playlist_text = QLineEdit(self)
        self.playlist_text.setGeometry(130, 70, 250, 30)

        self.songs_label = QLabel("Number of Songs:", self)
        self.songs_label.move(20, 120)

        self.songs_text = QLineEdit(self)
        self.songs_text.setGeometry(150, 120, 230, 30)

        self.generate_button = QPushButton("Generate Playlist", self)
        self.generate_button.setGeometry(120, 180, 160, 30)
        self.generate_button.clicked.connect(self.generate_playlist)

    def generate_playlist(self):
        artists = self.artists_text.text()
        playlist_name = self.playlist_text.text()
        num_songs = int(self.songs_text.text())

        # Set up Spotify API credentials
        scope = "playlist-modify-public"
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

        # Performs a search for songs related to the provided artists
        tracks = []
        for artist in artists.split(','):
            remaining_songs = num_songs
            offset = 0
            while remaining_songs > 0:
                # Limit the number of songs to search in each request to a maximum of 50
                limit = min(remaining_songs, 50)
                result = sp.search(q=f"artist:{artist}", type='track', limit=limit, offset=offset)
                for track in result['tracks']['items']:
                    tracks.append(track['uri'])
                remaining_songs -= limit
                offset += limit

        # Create a new playlist
        playlist = sp.user_playlist_create(user=sp.current_user()['id'], name=playlist_name, public=True)

        # Divide the song list into groups of 100 songs
        chunk_size = 100
        track_chunks = [tracks[i:i+chunk_size] for i in range(0, len(tracks), chunk_size)]

        # Add the songs to the playlist in groups
        for chunk in track_chunks:
            sp.playlist_add_items(playlist_id=playlist['id'], items=chunk)

        print("Playlist generated successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
