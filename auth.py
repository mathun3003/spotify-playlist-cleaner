from base64 import b64encode
import os
from dotenv import load_dotenv
import requests
import webbrowser
load_dotenv()

# get secrets
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')
bearer_token = os.getenv('BEARER_TOKEN')
code = os.getenv('CODE')

# encode client_id and client_secret to base64 byte
# bearer_token = b64encode(f'{client_id}:{client_secret}'.encode('utf-8'))

# curl https://accounts.spotify.com/authorize?client_id=5eb98124ca35416cb33192b9dda1d5c7&response_type=code&redirect_uri=http://localhost:9001/callback&scope=user-library-read%20playlist-read-private


access_token_link = f"""
                  https://accounts.spotify.com/authorize
                  ?client_id={client_id}
                    &response_type=code
                    &redirect_uri={redirect_uri}
                    &scope=user-library-read%20playlist-read-private
                    """

refresh_token_link = f"""
                    curl -H "Authorization: Basic {bearer_token}"
                    -d grant_type=authorization_code
                    -d code=...
                    -d redirect_uri={b64encode(redirect_uri.encode('utf-8'))} 
                    https://accounts.spotify.com/api/token
                    """


def invoke_code_url(client_id: str, redirect_uri: str, scopes: list()) -> str:
    # generate code_url
    code_url = f"""
                https://accounts.spotify.com/authorize?client_id={client_id}
                    &response_type=code
                    &redirect_uri={redirect_uri}
                    &scope=
                """
    # adjust scopes dynamically
    for scope in scopes:
        if len(scopes) < 2:
            code_url += scope
        else:
            code_url += scope + "%20"
    if len(scopes) >= 2:
        code_url = code_url[:-3]

    # invoke generated URL
    webbrowser.open(code_url, new=0, autoraise=True)

    return code_url


def refresh_access_token(url: str) -> str:
    """
    Function to refresh the Access Token
    ====================================
    :param url: Refresh URL
    :return: refreshed Access Token
    """
    try:
        response = requests.post(url)
        content = response.content
    except ConnectionError as e:
        print(e)

    return


url = invoke_code_url(client_id, redirect_uri, scopes=['user-library-read', 'playlist-read-private'])
print(url)