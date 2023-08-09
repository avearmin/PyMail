import imaplib


class EmailClient:
    def __init__(self, email):
        self.email = email
        self.imap_server = None
    
    def connect_to_email(self, access_token):
        auth_string = (
            "user=" + self.email + "\x01auth=Bearer " + access_token + "\x01\x01"
        )
        self.imap_server = imaplib.IMAP4_SSL("imap.gmail.com")
        self.imap_server.authenticate(mechanism="XOAUTH2", authobject=lambda x: auth_string)

    def disconnect_from_email(self):
        self.imap_server.close()
        self.imap_server.logout()

    def get_mailbox(self):
        status, data = self.imap_server.select(mailbox="INBOX")
        return status, data[0].decode()