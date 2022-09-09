import os
from dotenv import load_dotenv
import requests
import webbrowser


class SpotifyAuthorizer:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.redirect_uri = os.getenv('REDIRECT_URI')
        self.bearer_token = os.getenv('BEARER_TOKEN')
        self.access_token = os.getenv('ACCESS_TOKEN')
        self.refresh_token = os.getenv('REFRESH_TOKEN')

    def invoke_code_url(self, scopes: list()) -> str:
        """
        Invoke the authorization URL in order to receive the first
        valid token. A browser login window will be opened.
        ============================================================
        :param scopes: Spotify API scopes. Pick from playlist scopes:
               - playlist-read-collaborative
               - playlist-modify-public
               - playlist-read-private
               - playlist-modify-private
        :return: Login URL
        """
        # create scope string
        scope_string = f'{scopes[0]}' + ''.join(['%20' + scope for scope in scopes[1:]])

        # generate code_url
        code_url = f"""
                    https://accounts.spotify.com/authorize?client_id={self.client_id}
                        &response_type=code
                        &redirect_uri={self.redirect_uri}
                        &scope={scope_string}
                    """

        # invoke generated URL
        webbrowser.open(code_url, new=0, autoraise=True)

        return code_url

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
        os.environ["ACCESS_TOKEN"] = str(response_json["access_token"])

        return response_json['access_token']
