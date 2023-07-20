import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import requests

# Spotify credentials
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'

# YouTube search URL
YOUTUBE_SEARCH_URL = 'https://www.youtube.com/results'
YOUTUBE_SEARCH_PARAMS = {'search_query': ''}

# Create Spotipy client
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,
                                                                          client_secret=SPOTIFY_CLIENT_SECRET))

# Function to search YouTube for a song and get the first video URL
def get_youtube_url(song_name):
    YOUTUBE_SEARCH_PARAMS['search_query'] = song_name
    response = requests.get(YOUTUBE_SEARCH_URL, params=YOUTUBE_SEARCH_PARAMS)
    soup = BeautifulSoup(response.text, 'html.parser')
    video_url = soup.find('a', {'href': '/watch'})['href']
    return f'https://www.youtube.com{video_url}'

# Main function
def main():
    playlist_id = 'your_spotify_playlist_id'  # Replace with your Spotify playlist ID

    # Get playlist tracks from Spotify
    results = sp.playlist_tracks(playlist_id)

    # Extract song names
    song_names = [track['track']['name'] for track in results['items']]

    # Find YouTube URLs for each song
    youtube_urls = {}
    for song_name in song_names:
        youtube_url = get_youtube_url(song_name)
        youtube_urls[song_name] = youtube_url

    # Save the YouTube URLs to a text file
    with open('youtube_urls.txt', 'w') as file:
        for song_name, youtube_url in youtube_urls.items():
            file.write(f'{song_name}: {youtube_url}\n')

if __name__ == '__main__':
    main()
