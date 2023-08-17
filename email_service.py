from urwid import ExitMainLoop
from getpass import getpass
from password_manager import PasswordManager
from gmail_authenticator import GmailAuthenticator
from email_client import EmailClient
from email_menu import EmailMenu


class EmailService:
    def __init__(self, email):
        self.pass_manager = PasswordManager()
        self.email_client = EmailClient(email)
        self.email_menu = EmailMenu(self.key_handler)
    
    def start(self):
        self.login()
        self.email_client.select_mailbox("INBOX")
        page_1 = self.email_client.get_page_of_emails(1)
        self.display_menu(page_1)

    def login(self):
        self.pass_manager.setup()
        password = getpass()
        while not self.pass_manager.verify_password(password):
            print("Enter the correct password.")
            password = getpass()
        key = self.pass_manager.get_derived_key(password)
        self.authenticator = GmailAuthenticator(key)
        access_token = self.authenticator.authenticate()
        self.email_client.connect_to_email(access_token)
    
    def logout(self):
        self.email_client.disconnect_from_email()
    
    def display_menu(self, choices):
        self.email_menu.set_menu_view(choices)
    
    def key_handler(self, key_press):
        if key_press == 'ctrl x':
            if self.email_menu.view_name == "MENU":
                self.logout()
                raise ExitMainLoop()
            if self.email_menu.view_name == "READ":
                self.display_menu(self.email_client.current_choices)
    
