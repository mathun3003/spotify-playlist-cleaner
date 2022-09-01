import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
import requests
load_dotenv()

# set scope
scope = "user-library-read user-follow-read user-top-read playlist-read-private"


class SpotifyPlaylistCleaner:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.playlist_id = os.getenv('PLAYLIST_ID')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.refresh_token = os.getenv('REFRESH_TOKEN')
        self.bearer_token = os.getenv('BEARER_TOKEN')

    def refresh_access_token(self):
        """
        Refresh Access Token by overwriting it
        ======================================
        :return: Refreshed access_token
        """
        url = "https://accounts.spotify.com/api/token"

        response = requests.post(url,
                                 params={'grant_type': 'refresh_token',
                                         'refresh_token': self.refresh_token},
                                 headers={'Authorization': f"Basic {self.bearer_token}",
                                          'Content-Type': 'application/x-www-form-urlencoded'})
        response_json = response.json()

        # refresh access token by overwriting it
        self.access_token = response_json['access_token']

        return response_json['access_token']

    def get_playlist_json_data(self):
        """
        # TODO: fill me
        :return:
        """
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"

        response = requests.get(url,
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {self.access_token}"})
        response_json = response.json()
        return response_json, response.status_code

    def collect_songs(self, json_data):
        """
        # TODO: fill me
        :param self:
        :param json_data:
        :return:
        """
        num_tracks = json_data['total']
        url = f"https://api.spotify.com/v1/playlists/{self.playlist_id}/tracks"

        """
        necessary fields
        df['tracks']['items'][0]['track']['artists'][0]['name']  
        df['tracks']['items'][0]['added_at']
        df['tracks']['items'][0]['track']['name']
        df['tracks']['items'][0]['track']['id']
        """

        # initialize empty lists in order to collect songs
        artists, added_at, tracks, track_ids = [], [], [], []
        # collect songs
        for batch in range(0, num_tracks, 100):
            response = requests.get(url,
                                    headers={"Content-Type": "application/json",
                                             "Authorization": f"Bearer {self.access_token}"},
                                    params={'offset': str(batch)})
            tracks_batch = response.json()
            batch_len = len(tracks_batch['items'])
            for num in range(0, batch_len):
                artists.append(tracks_batch['items'][num]['track']['artists'][0]['name'])
                added_at.append(tracks_batch['items'][num]['added_at'])
                tracks.append(tracks_batch['items'][num]['track']['name'])
                track_ids.append(tracks_batch['items'][num]['track']['id'])
        # convert to df
        tracks_df = pd.DataFrame(data={'track_id': track_ids,
                                       'track': tracks,
                                       'artists': artists,
                                       'added_at': added_at})

        tracks_df['added_at'] = tracks_df['added_at'].apply(lambda date: date.split("T")[0])
        # FIXME convert datetime string to datetime object
        tracks_df['added_at'] = tracks_df['added_at'].apply(lambda date: datetime.strptime(date, '%y-%m-%d'))
        tracks_df.sort_values(by='added_at', ascending=True, inplace=True)
        return tracks_df

    def calc_time_dif(self, df: pd.DataFrame, date_column: str):
        """
        # TODO: fill me
        :param self:
        :param df:
        :param date_column:
        :return:
        """
        # FIXME
        df['time_dif'] = df[date_column].apply(lambda date: datetime.now() - date)
        return

    def add_songs_to_playlist(self):
        # TODO
        return

    def remove_songs_from_playlist(self):
        # TODO
        return


