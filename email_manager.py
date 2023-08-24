import os


class EmailManager:
    def __init__(self):
        self.code_dir = os.path.dirname(os.path.abspath(__file__))
        self.email_path = os.path.join(
            self.code_dir, 'config', 'email.txt'
        )
    
    def verify_config_dir(self):
        config_dir = os.path.join(self.code_dir, 'config')
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

    def load_email(self) -> str:
        self.verify_config_dir()
        if not os.path.exists(self.email_path):
            return
        with open(self.email_path, 'r') as file:
            email = file.read()
        return email
    
    def save_email(self, email: str):
        self.verify_config_dir()
        with open(self.email_path, 'w') as file:
            file.write(email)

        