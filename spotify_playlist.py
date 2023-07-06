import spotipy
from spotipy.oauth2 import SpotifyOAuth
from Credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

# Set up Spotify API credentials
scope = "playlist-modify-public"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, scope=scope))

# Prompts user for artists, playlist name, and number of songs
artists = input("Enter the artists you want to include in the playlist (separated by commas): ")
playlist_name = input("Enter playlist name: ")
num_songs = int(input("Enter the number of songs you want to add: "))

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
