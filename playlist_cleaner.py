import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime
import requests
import json


class SpotifyPlaylistCleaner:
    def __init__(self):
        load_dotenv()
        self.source_playlist_id = os.getenv('SOURCE_PLAYLIST_ID')
        self.destination_playlist_id = os.getenv('DESTINATION_PLAYLIST_ID')
        self.access_token = os.getenv('ACCESS_TOKEN')

    def get_playlist_json_data(self):
        """
        get JSON data of source playlist
        ================================
        :return: JSON data
        """
        url = f"https://api.spotify.com/v1/playlists/{self.source_playlist_id}/tracks"

        response = requests.get(url,
                                headers={"Content-Type": "application/json",
                                         "Authorization": f"Bearer {self.access_token}"})
        response_json = response.json()
        return response_json

    def collect_songs(self, json_data) -> pd.DataFrame:
        """
        collect all songs from source playlist
        =========================================
        :param self: self
        :param json_data: JSON data from playlist
        :return: songs as DataFrame
        """
        num_tracks = json_data['total']
        url = f"https://api.spotify.com/v1/playlists/{self.source_playlist_id}/tracks"

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
        # date formatting and sorting by added_at
        tracks_df['added_at'] = tracks_df['added_at'].apply(lambda date: date.split("T")[0])
        tracks_df['added_at'] = pd.to_datetime(tracks_df['added_at'], format='%Y-%m-%d')
        tracks_df.sort_values(by='added_at', ascending=True, inplace=True)
        return tracks_df

    def calc_time_dif(self, songs: pd.DataFrame, date_column: str) -> pd.DataFrame:
        """
        calculating time difference from current date
        =================================================================
        :param self: self
        :param songs: DataFrame containing the songs from source playlist
        :param date_column: Date Column from which the time
               difference should be calculated
        :return: Input DataFrame with an extra time_dif column
        """
        songs['time_dif'] = songs[date_column].apply(lambda date: datetime.today() - date)
        return songs

    def add_songs_to_playlist(self, outdated_songs: pd.DataFrame):
        """
        Add outdated songs to another playlist. Only adding songs that
        do not already exist in the destination playlist
        ==============================================================
        :param outdated_songs: outdated songs received
               from remove_songs_from_playlist function
        :return: status code list
        """
        if outdated_songs.empty:
            return None
        else:
            # receive number of tracks from destination playlist
            url = f"https://api.spotify.com/v1/playlists/{self.destination_playlist_id}/tracks"
            response = requests.get(url,
                                    headers={"Content-Type": "application/json",
                                             "Authorization": f"Bearer {self.access_token}"})
            response_json = response.json()
            num_tracks = response_json['total']

            # initialize empty list in order to collect track IDs
            track_ids = []
            # collect song ids from destination playlist
            for batch in range(0, num_tracks, 100):
                response = requests.get(url,
                                        headers={'Content-Type': 'application/json',
                                                 'Authorization': f'Bearer {self.access_token}'},
                                        params={'offset': str(batch)})
                tracks_batch = response.json()
                batch_len = len(tracks_batch['items'])
                for num in range(0, batch_len):
                    track_ids.append(tracks_batch['items'][num]['track']['id'])
            # filter existing songs
            songs_to_add = outdated_songs[~outdated_songs['track_id'].isin(track_ids)]
            # add songs to destination playlist
            for uri in songs_to_add['track_id'].to_list():
                uri_string = f"spotify:track:{uri}"
                response_status_codes = list()
                response = requests.post(url,
                                         headers={'Accept': 'application/json',
                                                  'Content-Type': 'application/json',
                                                  'Authorization': f'Bearer {self.access_token}'},
                                         params={'uris': uri_string})
                response_status_codes.append(response.status_code)

            return response_status_codes

    def remove_songs_from_playlist(self, songs: pd.DataFrame, time_dif_col: str, num_days: int):
        """
        Remove Songs from source playlist
        ========================================================================
        :param songs: Songs from source playlist
        :param time_dif_col: Column expressing the time difference between today
               and added_at date
        :param num_days: Number of days after which the songs should be removed
        :return: DataFrame with the removed songs
        """
        # remove all songs older than the specified number of days
        songs_to_remove = songs[songs[time_dif_col] > pd.to_timedelta(f'{str(num_days)} days')]
        if songs_to_remove.empty:
            return songs_to_remove
        else:
            # create request body for DELETE request
            songs_to_remove_lst = []
            for uri in songs_to_remove['track_id'].to_list():
                uri_dict = {"uri": f"spotify:track:{uri}"}
                songs_to_remove_lst.append(uri_dict)
            # batch processing, since Spotify can only handle batches of size 100
            url = f"https://api.spotify.com/v1/playlists/{self.source_playlist_id}/tracks"
            num_tracks = len(songs_to_remove_lst)
            step_size = 100
            for batch in range(0, num_tracks, step_size):
                batch_lst = songs_to_remove_lst[batch:batch+step_size]
                request_body = {"tracks": batch_lst}
                response = requests.delete(url,
                                           headers={'Content-Type': 'application/json',
                                                    'Accept': 'application/json',
                                                    'Authorization': f'Bearer {self.access_token}'},
                                           data=json.dumps(request_body))
            return songs_to_remove


