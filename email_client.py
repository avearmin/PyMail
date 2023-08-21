import imaplib
import smtplib
import email
from math import ceil
import base64


class EmailClient:
    def __init__(self, email: str):
        self.email = email
        self.imap_server = None
        self.smtp_server = None
        self.total_emails = None
        self.page_size = 20
        self.current_page_num = 1
        self.current_choices = None
        
    
    def connect_to_email(self, access_token: str):
        auth_string = (
            'user=' + self.email + '\x01auth=Bearer ' + access_token + '\x01\x01'
        )
        base64_auth_string = base64.b64encode(auth_string.encode()).decode()
        self.imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
        self.imap_server.authenticate(mechanism='XOAUTH2', authobject=lambda x: auth_string)
        self.smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.smtp_server.ehlo_or_helo_if_needed()
        self.smtp_server.auth('XOAUTH2', lambda: auth_string)

    def disconnect_from_email(self):
        self.imap_server.close()
        self.imap_server.logout()
        self.smtp_server.quit()

    def select_mailbox(self, mailbox: str):
        status, data = self.imap_server.select(mailbox)
        if status != 'OK':
            # TODO: curses method to print error to window
            return
        self.total_emails = int(data[0])
    
    def get_page_of_emails(self) -> list:
        items = []
        start = self.total_emails - ((self.current_page_num - 1) * self.page_size)
        end = self.total_emails - (self.current_page_num * self.page_size)
        try:
            for i in range(start, end, -1):
                email = self.fetch_email(i)
                items.append(email)
            self.current_choices = items
            return items
        except IndexError:
            pass
    
    def get_next_page_of_emails(self) -> list:
        if self.current_page_num == self.get_total_num_pages():
            return
        self.current_page_num += 1
        return self.get_page_of_emails()

    def get_prev_page_of_emails(self) -> list:
        if self.current_page_num == 1:
            return
        self.current_page_num -= 1
        return self.get_page_of_emails()
    
    def get_total_num_pages(self):
        return ceil(self.total_emails / self.page_size)
    
    def fetch_email(self, email_number: int) -> tuple:
        status, data = self.imap_server.fetch(str(email_number), "(RFC822)")
        if status != 'OK':
            # TODO: curses method to print error to window
            return
        raw_email = data[0][1]
        message = email.message_from_bytes(raw_email)
        subject = email.header.decode_header(message['Subject'])[0][0]
        sender = email.utils.parseaddr(message['From'])[1]
        content = self.get_content(message)
        return (subject, sender, content)
        
    def get_content(self, message) -> str:
        if not message.is_multipart():
            if isinstance(message, str):
                content = message.get_payload(decode=True).decode(message.get_content_charset())
            else:
                content = message.get_payload(decode=False)
            return content
        for part in message.walk():
            content_type = part.get_content_type()
            if 'text/plain' == content_type:
                content = part.get_payload(decode=True).decode(part.get_content_charset())
                return content
            
    def send_email(self, to_addrs: list, msg: str):
        self.smtp_server.sendmail(self.email, to_addrs, msg)