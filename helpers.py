import requests
import json
import pandas as pd

def get_user_id(access_token):

    # Create authorization header for API
    auth_header = {"Authorization": f"Bearer {access_token}"}

    # Grab user data using auth_header
    url = f"https://api.spotify.com/v1/me"
    resp = requests.get(url, headers=auth_header)
    raw_user_data = resp.json()

    # Locate user ID
    user_id = raw_user_data['id']
    return user_id

def get_liked_tracks(access_token):

    # Create authorization header for API
    auth_header = {"Authorization": f"Bearer {access_token}"}

    # Grab liked using auth_header
    url = f"https://api.spotify.com/v1/me/tracks?offset=0&limit=50"
    resp = requests.get(url, headers=auth_header)
    raw_songs_data = resp.json()

    # Grab total number of tracks
    total_tracks = int(raw_songs_data['total'])
    
    if total_tracks == 0:
        return "no_tracks"
    elif total_tracks > 50:
        total_tracks = 50

    # Create liked_songs data frame
    rows = []
    for i in range(total_tracks):
        rows.append([raw_songs_data['items'][i]['track']['name'], 
                    raw_songs_data['items'][i]['track']['artists'][0]['name'],
                    raw_songs_data['items'][i]['track']['album']['images'][0]['url']])
    liked_songs = pd.DataFrame(rows, columns=["title", "artist", "artwork_url"])

    # Arrange alphabetically by song title
    liked_songs.sort_values(by=['title'], inplace=True)
    liked_songs.index = range(total_tracks)

    # Return data frame
    return liked_songs


