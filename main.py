import os
import logging
from datetime import datetime
from turtledemo.minimal_hanoi import play
from playlist_cleaner import SpotifyPlaylistCleaner
from auth import SpotifyAuthorizer
from send_email import send_email

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

# log status codes and removed songs to stdout in console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("cleaning_logs.log"),
        logging.StreamHandler()
    ]
)
if removed_songs.empty:
    logging.info(f"""
    Time: {datetime.now()}
    
    No Songs transferred
    """)
else:
    tracks = removed_songs['track'].to_list()
    artists = removed_songs['artists'].to_list()
    # create logs
    logging_info = f"""
    Time: {datetime.now()}
    
    Transferred songs: {' '.join(song + f'({artist}),' for song, artist in zip(tracks, artists))}
    Status Codes: {' '.join(status_code + ',' for status_code in status_codes)}
    """
    # logging
    logging.info(logging_info)
    # send email
    # FIXME send_email(logging_info)
