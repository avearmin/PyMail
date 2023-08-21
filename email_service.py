import subprocess
import tempfile
from urwid import ExitMainLoop
from getpass import getpass
from password_manager import PasswordManager
from gmail_authenticator import GmailAuthenticator
from email_client import EmailClient
from email_menu import EmailMenu


class EmailService:
    def __init__(self, email: str):
        self.email = email
        self.pass_manager = PasswordManager()
        self.email_client = EmailClient(email)
        self.email_menu = EmailMenu(self.key_handler)
    
    def start(self):
        self.login()
        self.email_client.select_mailbox('INBOX')
        page_1 = self.email_client.get_page_of_emails()
        self.display_menu(page_1)
        self.email_menu.loop.run()

    def login(self):
        self.pass_manager.setup()
        password = getpass()
        while not self.pass_manager.verify_password(password):
            print('Enter the correct password.')
            password = getpass()
        key = self.pass_manager.get_derived_key(password)
        self.authenticator = GmailAuthenticator(key)
        access_token = self.authenticator.authenticate()
        self.email_client.connect_to_email(access_token)
    
    def logout(self):
        self.email_client.disconnect_from_email()
    
    def display_menu(self, emails: list):
        self.email_menu.set_menu_view(emails)
    
    def key_handler(self, key_press: str):
        if key_press == 'ctrl x':
            self.handle_ctrl_x()
        if key_press == 'right':
            self.handle_right_arrow()
        if key_press == 'left':
            self.handle_left_arrow()
        if key_press == 'ctrl r':
            self.handle_ctrl_r()
    
    def handle_ctrl_x(self):
        if self.email_menu.view_name == 'MENU':
            self.logout()
            raise ExitMainLoop()
        if self.email_menu.view_name == 'READ':
            self.display_menu(self.email_client.current_choices)
    
    def handle_right_arrow(self):
        if self.email_menu.view_name != 'MENU':
            return
        next_page = self.email_client.get_next_page_of_emails()
        if next_page is None:
            return
        self.display_menu(next_page)
    
    def handle_left_arrow(self):
        if self.email_menu.view_name != 'MENU':
            return
        prev_page = self.email_client.get_prev_page_of_emails()
        if prev_page is None:
            return
        self.display_menu(prev_page)
    
    def handle_ctrl_r(self):
        temp = self.get_temp_file()
        if self.email_menu.view_name == 'READ':
            self.add_reply_addr_to_temp(temp)
        subprocess.call(['nano', temp])
        email_contents = self.get_email_contents(temp)
        if len(email_contents) != 3:
            return
        self.prepare_and_send_email(email_contents)
        self.display_menu(self.email_client.current_choices)

    def get_temp_file(self):
        temp = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        temp.close()
        return temp.name

    def get_email_contents(self, temp_file_name: str) -> list[str]:
        with open(temp_file_name) as file:
            email_contents = file.read()
        return email_contents.split('\n\n')
    
    def prepare_and_send_email(self, email_contents: list[str]):
        to_addrs = email_contents[0]
        subject = email_contents[1]
        message = email_contents[2]
        email_formatted_as_string = self.format_email_as_string(to_addrs, subject, message)
        self.email_client.send_email(to_addrs, email_formatted_as_string)

    def format_email_as_string(self, to_addrs: str, subject: str, message: str):
        return (
            f'From: {self.email}\r\n'
            f'To: {to_addrs}\r\n'
            f'Subject: {subject}\r\n\r\n'
            f'{message}'
        )
    
    def add_reply_addr_to_temp(self, temp_file_name: str):
        with open(temp_file_name, 'w') as file:
            file.write(self.email_menu.current_reply_addr + '\n\n')
