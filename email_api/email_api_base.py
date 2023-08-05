class EmailAPIBase:
    """Base class for email service provider APIs."""

    def __init__(self, email, client_id, client_secret, token_endpoint):
        self.email = email
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint