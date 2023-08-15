from getpass import getpass
from password_manager import PasswordManager
from gmail_authenticator import GmailAuthenticator
from email_client import EmailClient


class EmailService:
    def __init__(self, email):
        self.pass_manager = PasswordManager()
        self.email_client = EmailClient(email)
    
    def start(self):
        self.pass_manager.setup()
        password = getpass()
        while not self.pass_manager.verify_password(password):
            print("Enter the correct password.")
            password = getpass()
        key = self.pass_manager.get_derived_key(password)
        self.authenticator = GmailAuthenticator(key)
        access_token = self.authenticator.authenticate()
        self.email_client.connect_to_email(access_token)
        self.email_client.get_inbox()
    
    def login(self):
        access_token = self.authenticator.authenticate()
        self.email_client.connect_to_email(access_token)
        return self.email_client.get_mailbox()
    
    def logout(self):
        self.email_client.disconnect_from_email()