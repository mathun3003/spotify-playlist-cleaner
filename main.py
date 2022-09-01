from playlist_cleaner import SpotifyPlaylistCleaner

spc = SpotifyPlaylistCleaner()
playlist_json, status_code = spc.get_playlist_json_data()

if status_code != 200:
    spc.refresh_access_token()
    playlist_json, _ = spc.get_playlist_json_data()

tracks = spc.collect_songs(playlist_json)

print(tracks.head())

