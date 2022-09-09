# Spotify Playlist Cleaner 
![](https://images.unsplash.com/photo-1611339555312-e607c8352fd7?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1074&q=80)
Photo by <a href="https://unsplash.com/@alexbemore?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Alexander Shatov</a> on <a href="https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
---
## What I did
I own a Spotify Premium Account for several years now, and I add songs to my personal playlist that I really like and would like to listen to in the near future.
This behaviour comes with the big drawback that my playlist got veeeeeery long and I actually don't listen to all the songs in the playlist.

Recently, I had the idea that I would like to save only the songs I like to listen to lately in my personal playlist, and outsource the other ones from this playlist to another playlist.

Thus, I developed a short but lovely algorithm that takes the songs from my playlist that were added long ago and move those songs to another playlist. 
This way, I do not lose any songs I once listened to but keep my current favorite songs in my playlist.   

## How it works
I used the [Spotify Web-API](https://developer.spotify.com/documentation/web-api/) for this project. Since the Spotify Web-API uses OAuth, we need to get a temporary Access Token first.
All authorization mechanisms are handled by the `SpotifyAuthorizer` class in the `auth.py`. Mainly, this class is used to refresh the Access Token if this should be expired.

The necessary mechanism to receive the first Access Token is encapsulated in the `invoke_code_url()` method. Therefore, we need to specify the [scopes](https://developer.spotify.com/documentation/general/guides/authorization/scopes/) this token should be used for.
To invoke the URL, you need to hand over your Redirect URI to the environment variables (e.g., with a `.env` file) and your Client ID. Both are accessible in the respective Spotify App of your Spotify Web-API Account.
Please, take a look at the documentation regarding the Spotify OAuth process if you are not familiar with it, since I will not explain the details here. 

Once we received the Refresh Token, we can use this to refresh the Access Token with the `refresh_access_token()` method of the `SpotifyAuthorizer` class.

Besides that, we need to specify a Source Playlist, from which we will delete the songs, and a Destination Playlist, to which we will transfer the deleted songs.
This is done by the `SOURCE_PLAYLIST_ID` and `DESTINATION_PLAYLIST_ID` variables, respectively. How you can get your Playlist IDs is explained [here](https://clients.caster.fm/knowledgebase/110/How-to-find-Spotify-playlist-ID.html).

You can find all operations regarding the Spotify Playlist Cleaner in the ``playlsist_cleaner.py``.
Now, the first step is to get the Source Playlist Data via the `get_playlist_json_data()` method.
In the next step, all songs from the Source Playlist are collected and returned in a DataFrame.

I filtered my Source Playlist by the date where this song were added to my playlist. Sure, you define your own filter method, but this is a simple and easy approach that solves my problem pretty good.
Thus, the ```calc_time_dif()``` method is used to calculate the time difference between the `added_at` date and today's date.

Then, we filter all songs from my Source Playlist that are older than the specified number of days. For me, 550 days work pretty well.
Those songs are then transferred to the Destination Playlist with the ``add_songs_to_playlist()`` method.

And that's all! 

To make matters worse, I wrote a function to inform myself about changes in my Source Playlist via Email and print these logs to stdout.

## Hosting possibilities
To hold things simple, I used the GitHub Actions to host my gentle algorithm on GitHub. 
Thus, the ``.github/workflows/actions.yaml`` specifies the action workflow. For me, a monthly schedule worked out. 