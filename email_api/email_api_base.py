class EmailAPIBase:
    """Base class for email service provider APIs."""
    
    def fetch_inbox(self):
        pass

    def read_email(self):
        pass

    def write_email(self):
        pass