import email
from imaplib import IMAP4_SSL


class EmailPage:
    def __init__(self, imap_server: IMAP4_SSL, size: int, total_emails: int):
        self.imap_server = imap_server
        self.size = size
        self.total_emails = total_emails
        self.items = []

    def set_page(self, page_number: int) -> list:
        self.items = []
        start = self.total_emails - ((page_number - 1) * self.size)
        end = self.total_emails - (page_number * self.size)
        try:
            for i in range(start, end, -1):
                email = self.fetch_email(i)
                self.items.append(email)
        except IndexError:
            pass
    
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