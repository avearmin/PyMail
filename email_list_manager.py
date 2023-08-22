import os


class EmailListManager:
    def __init__(self):
        self.code_dir = os.path.dirname(os.path.abspath(__file__))
        self.email_list_path = os.path.join(
            self.code_dir, 'config', f'email-list.txt'
        )
    
    def verify_config_dir(self):
        config_dir = os.path.join(self.code_dir, 'config')
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)

    def load_email_list(self) -> list[str]:
        self.verify_config_dir()
        if not os.path.exists(self.email_list_path):
            email_list = []
            return email_list
        with open(self.email_list_path, 'r') as file:
            email_list = file.read().split('\n')
        return email_list
    
    def save_email_list(self, email_list: list[str]):
        with open(self.email_list_path, 'w') as file:
            for email in email_list:
                file.write(email + '\n')
    
    def write_email_to_list(self, email: str):
        email_list = self.load_email_list()
        email_list.append(email)
        self.save_email_list(email_list)
        print(f'{email} saved!')

    def delete_email_from_list(self, email: str):
        email_list = self.load_email_list()
        email_list.remove(email)
        self.save_email_list(email_list)
        print(f'{email} deleted!')
        