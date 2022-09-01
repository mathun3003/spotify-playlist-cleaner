import pandas as pd
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import os
from datetime import datetime
import json
import requests
load_dotenv()

# get secrets
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
playlist_id = os.getenv('PLAYLIST_ID')
access_token = os.getenv('ACCESS_TOKEN')

# set scope
scope = "user-library-read user-follow-read user-top-read playlist-read-private"


class SpotifyPlaylistCleaner:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.playlist_id = playlist_id

    def get_playlist_json_data(self):
        """
        # TODO: fill me
        :return:
        """
        query = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

        response = requests.get(query,
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {access_token}"})
        response_json = response.json()
        return response_json

    def convert_json_data(self, json_data):
        """
        # TODO: fill me
        :param json_data:
        :return:
        """
        num_tracks = json_data['tracks']['total']

        """
        necessary fields
        df['tracks']['items'][0]['track']['artists'][0]['name']  
        df['tracks']['items'][0]['added_at']
        df['tracks']['items'][0]['track']['name']
        df['tracks']['items'][0]['track']['id']
        """

        artists, added_at, tracks, track_ids = [], [], [], []
        for batch in range(0, num_tracks, 100):
            tracks_batch = sp.playlist_items(playlist_id, offset=batch)
            for num in range(0, len(tracks_batch['items'])):
                artists.append(tracks_batch['items'][num]['track']['artists'][0]['name'])
                added_at.append(tracks_batch['items'][num]['added_at'])
                tracks.append(tracks_batch['items'][num]['track']['name'])
                track_ids.append(tracks_batch['items'][num]['track']['id'])

        tracks_df = pd.DataFrame()
        tracks_df['track_id'] = track_ids
        tracks_df['track'] = tracks
        tracks_df['artist'] = artists
        tracks_df['added_at'] = added_at

        # FIXME convert datetime string to datetime object
        tracks_df['added_at'] = tracks_df['added_at'].apply(lambda date: date.split("T")[0])
        tracks_df['added_at'] = tracks_df['added_at'].apply(lambda date: datetime.strptime(date, '%y-%m-%d'))
        tracks_df.sort_values(by='added_at', ascending=True, inplace=True)
        return tracks_df

    def calc_time_dif(self, df: pd.DataFrame, date_column: str):
        """
        # TODO: fill me
        :param df:
        :param date_column:
        :return:
        """
        # FIXME
        df['time_dif'] = df[date_column].apply(lambda date: datetime.now() - date)
        return

# TODO: implement method for get refresh token: https://www.youtube.com/watch?v=-FsFT6OwE1A
