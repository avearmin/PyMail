import curses
from password_manager import PasswordManager
from gmail_authenticator import GmailAuthenticator
from email_client import EmailClient
from cli.login_window import LoginWindow


class EmailService:
    def __init__(self, email):
        self.stdscr = curses.initscr()
        self.login_win = LoginWindow(self.stdscr)
        self.pass_manager = PasswordManager(self.stdscr)
        self.email_client = EmailClient(email)
    
    def start(self):
        self.pass_manager.setup()
        self.login_win.display()
        password = self.login_win.get_password_input()
        while not self.pass_manager.verify_password(password):
            self.login_win.window.addstr(4, 10, "Incorrect password: try again")
            self.login_win.window.refresh()
            password = self.login_win.get_password_input()
        self.login_win.close()
        key = self.pass_manager.get_derived_key(password)
        self.authenticator = GmailAuthenticator(key)
    
    def login(self):
        access_token = self.authenticator.authenticate()
        self.email_client.connect_to_email(access_token)
        return self.email_client.get_mailbox()
    
    def logout(self):
        self.email_client.disconnect_from_email()