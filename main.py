from turtledemo.minimal_hanoi import play

from playlist_cleaner import SpotifyPlaylistCleaner
from auth import SpotifyAuthorizer

authorizer = SpotifyAuthorizer()
spc = SpotifyPlaylistCleaner()

playlist_json, status_code = spc.get_playlist_json_data()

if status_code != 200:
    spc.access_token = authorizer.refresh_access_token()
    playlist_json, _ = spc.get_playlist_json_data()

tracks = spc.collect_songs(playlist_json)
tracks = spc.calc_time_dif(tracks, 'added_at')
removed_songs = spc.remove_songs_from_playlist(df=tracks,
                                                 time_dif_col='time_dif',
                                                 num_days=425)
spc.add_songs_to_playlist(removed_songs)

# TODO: add logs


