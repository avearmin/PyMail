import imaplib
from email_page import EmailPage
from email_menu import EmailMenu


class EmailClient:
    def __init__(self, email: str):
        self.email = email
        self.imap_server = None
        self.page = None
        self.email_menu = EmailMenu()
        
    
    def connect_to_email(self, access_token: str):
        auth_string = (
            "user=" + self.email + "\x01auth=Bearer " + access_token + "\x01\x01"
        )
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap_server.authenticate(mechanism="XOAUTH2", authobject=lambda x: auth_string)

    def get_inbox(self):
        page_size = 10
        status, total_emails = self.select_mailbox("INBOX")
        self.page = EmailPage(self.imap_server, page_size, total_emails)
        self.page.set_page(1)
        self.email_menu.display_menu(self.page.items)


    def disconnect_from_email(self):
        self.imap_server.close()
        self.imap_server.logout()

    def select_mailbox(self, mailbox: str):
        status, data = self.imap_server.select(mailbox)
        if status != 'OK':
            # TODO: curses method to print error to window
            return
        return status, int(data[0])
            
    