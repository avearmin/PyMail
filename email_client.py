import imaplib


class EmailClient:
    def __init__(self, email):
        self.email = email
    
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