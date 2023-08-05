import imaplib, requests, webbrowser, json
from email_api.email_api_base import EmailAPIBase


class GmailAPI(EmailAPIBase):
    """Extends the EmailAPIBase and provides methods specific to
    interacting with the Gmail API."""

    def __init__(self, email, client_id, client_secret):
        super().__init__(
            email,
            client_id,
            client_secret,
            "https://accounts.google.com/o/oauth2/token",
        )

    def get_authorization_code(self):
        auth_url = (
            "https://accounts.google.com/o/oauth2/auth?"
            f"client_id={self.client_id}"
            "&redirect_uri=urn:ietf:wg:oauth:2.0:oob"
            "&scope=https://mail.google.com/"
            "&response_type=code"
        )
        webbrowser.open(auth_url)
        authorization_code = input("Enter the authorization code: ")
        return authorization_code

    def get_token(self, authorization_code):
        auth_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": "urn:ietf:wg:oauth:2.0:oob",
        }
        response = requests.post(self.token_endpoint, data=auth_data)
        if response.status_code // 100 != 2:
            print("Token request failed with status code:", response.status_code)
            return None
        try:
            token = response.json()
            return token
        except json.JSONDecodeError:
            print("Failed to parse response as JSON")
            return None

    def connect_to_email(self, access_token):
        auth_string = (
            "user=" + self.email + "\x01auth=Bearer " + access_token + "\x01\x01"
        )
        imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        imap_server.authenticate(mechanism="XOAUTH2", authobject=lambda x: auth_string)
        return imap_server

    def disconnect_from_email(self, imap_server):
        imap_server.close()
        imap_server.logout()

    def get_mailbox(self, imap_server):
        status, data = imap_server.select(mailbox="INBOX")
        return status, data[0].decode()
