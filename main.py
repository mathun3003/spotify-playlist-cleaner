import os
from turtledemo.minimal_hanoi import play
from playlist_cleaner import SpotifyPlaylistCleaner
from auth import SpotifyAuthorizer

# instantiate SpotifyAuthorizer for OAuth
authorizer = SpotifyAuthorizer()
# instantiate SpotifyPlaylistCleaner
spc = SpotifyPlaylistCleaner()

# refresh access token and submit to SpotifyPlaylistCleaner instance
spc.access_token = authorizer.refresh_access_token()
# get JSON data from source playlist
playlist_json = spc.get_playlist_json_data()
# collect songs from source playlist
tracks = spc.collect_songs(playlist_json)
# calculate time differences between today and the date when the songs were added
tracks = spc.calc_time_dif(tracks, 'added_at')
# filter and remove songs that were added 550 days ago
removed_songs = spc.remove_songs_from_playlist(tracks,
                                               time_dif_col='time_dif',
                                               num_days=550)
# add songs to destination playlist and collect all status codes
status_codes = spc.add_songs_to_playlist(removed_songs)

# TODO: add logs
