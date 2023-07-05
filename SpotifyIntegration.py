import spotipy
import spotipy.util as util

# Set up Spotify API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'  # Must match the redirect URI in your Spotify Developer Dashboard

# Set up user authentication
scope = 'user-modify-playback-state'
username = 'YOUR_SPOTIFY_USERNAME'

# Obtain an access token for the user
token = util.prompt_for_user_token(username=username,
                                   scope=scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)

# Create a spotipy client
sp = spotipy.Spotify(auth=token)

# Function to get the currently playing song
def get_currently_playing():
    current_track = sp.currently_playing()
    if current_track is not None and current_track['is_playing']:
        song_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        print(f"Currently playing: {song_name} by {artist_name}")
    else:
        print("No song is currently playing.")

# Function to skip to the next song
def skip_to_next_song():
    sp.next_track()
    print("Skipped to the next song.")

# Function to play or pause the playback
def play_pause():
    current_track = sp.current_playback()
    if current_track is not None and current_track['is_playing']:
        sp.pause_playback()
        print("Playback paused.")
    else:
        sp.start_playback()
        print("Playback started.")

# Example usage
get_currently_playing()
skip_to_next_song()
play_pause()
