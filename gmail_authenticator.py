import webbrowser
import requests
import json
from credentials_manager import GoogleCredentialsManager


class GmailAuthenticator:
    def __init__(self, key: bytes):
        self.key = key
        self.cred_manager = GoogleCredentialsManager()
        self.refresh_token = self.cred_manager.load_refresh_token(self.key)
        self.client_id = self.cred_manager.load_client_id(self.key)
        self.client_secret = self.cred_manager.load_client_secret(self.key)
        self.token_endpoint = 'https://accounts.google.com/o/oauth2/token'

    def authenticate(self):
        while self.client_id is None or self.client_secret is None:
            path = input('Paste the path to the credentials google gave you: ')
            self.cred_manager.import_credentials(self.key, path)
            self.client_id = self.cred_manager.load_client_id(self.key)
            self.client_secret = self.cred_manager.load_client_secret(self.key)
        if not self.refresh_token:
            auth_code = self.get_authorization_code()
            return self.get_token_by_authorization_code(auth_code)
        return self.get_token_by_refresh_token()

    def get_authorization_code(self) -> str:
        auth_url = (
            'https://accounts.google.com/o/oauth2/auth?'
            f'client_id={self.client_id}'
            '&redirect_uri=urn:ietf:wg:oauth:2.0:oob'
            '&scope=https://mail.google.com/'
            '&response_type=code'
        )
        webbrowser.open(auth_url)
        authorization_code = input('Enter the authorization code: ')
        return authorization_code

    def get_token_by_authorization_code(self, authorization_code: str) -> str:
        auth_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': 'urn:ietf:wg:oauth:2.0:oob',
        }
        response = requests.post(self.token_endpoint, data=auth_data)
        if response.status_code // 100 != 2:
            print('Token request failed with status code:', response.status_code)
            return None
        try:
            token = response.json()
            access_token = token.get('access_token')
            refresh_token = token.get('refresh_token')
            self.cred_manager.save_refresh_token(self.key, refresh_token)
            return access_token
        except json.JSONDecodeError:
            print('Failed to parse response as JSON')
            return None

    def get_token_by_refresh_token(self) -> str:
        auth_data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }
        response = requests.post(self.token_endpoint, data=auth_data)
        if response.status_code // 100 != 2:
            print('Token request failed with status code: ', response.status_code)
            return None
        try:
            token = response.json()
            access_token = token.get('access_token')
            return access_token
        except json.JSONDecodeError:
            print('Failed to parse response as JSON')
            return None
