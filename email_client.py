import imaplib
import email
import webbrowser
import os

class EmailClient:
    def __init__(self, email: str):
        self.email = email
        self.imap_server = None
    
    def connect_to_email(self, access_token: str):
        auth_string = (
            "user=" + self.email + "\x01auth=Bearer " + access_token + "\x01\x01"
        )
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap_server.authenticate(mechanism="XOAUTH2", authobject=lambda x: auth_string)

    def disconnect_from_email(self):
        self.imap_server.close()
        self.imap_server.logout()

    def select_mailbox(self, mailbox: str):
        status, data = self.imap_server.select(mailbox)
        if status != 'OK':
            # TODO: curses method to print error to window
            return
        return status, data[0].decode()
    
    def fetch_email(self, email_number: int) -> tuple:
        status, data = self.imap_server.fetch(str(email_number), "(RFC822)")
        if status != 'OK':
            # TODO: curses method to print error to window
            return
        raw_email = data[0][1]
        message = email.message_from_bytes(raw_email)
        subject = email.header.decode_header(message["Subject"])[0][0]
        sender = email.utils.parseaddr(message["From"])[1]
        content = self.get_content(message)
        return (subject, sender, content)
        
    def get_content(self, message) -> str:
        if not message.is_multipart():
            content = message.get_payload(decode=True).decode(message.get_content_charset())
            return content
        for part in message.walk():
            content_type = part.get_content_type()
            if "text/plain" == content_type:
                content = part.get_payload(decode=True).decode(part.get_content_charset())
                return content
    
    def print_email(self, email: tuple):
        if email[0]:
            print(f"Subject: {email[0]}")
        if email[1]:
            print(f"Sender: {email[1]}")
        if email[2][0]:
            print(f"Content: {email[2]}")
    