from gmail_authenticator import GmailAuthenticator
from email_client import EmailClient


class EmailService:
    def __init__(self, key, email):
        self.authenticator = GmailAuthenticator(key)
        self.email_client = EmailClient(email)
    
    def login(self):
        access_token = self.authenticator.authenticate()
        email_connection = self.email_client.connect_to_email(access_token)
        status, mailbox = self.email_client.get_mailbox(email_connection)
        return email_connection
    
    def logout(self, email_connection):
        self.email_client.disconnect_from_email(email_connection)