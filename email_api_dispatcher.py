from email_api.gmail_api import GmailAPI

class EmailAPIDispatcher:
    """Connects email accounts to appropriate APIs."""

    def __init__(self, email_domain: str):
        """Initialize the EmailAPIDispatcher with the appropriate email service provider API."""
        self.email_api = self.connect_to_email_api(email_domain)
    
    def connect_to_email_api(email_domain: str) -> [GmailAPI]:
        if email_domain == 'gmail.com':
            return GmailAPI()

