from argparse import ArgumentParser
from email_service import EmailService

class ArgParser:
    def __init__(self):
        self.parser = ArgumentParser()
        self.subparsers = self.parser.add_subparsers(title='command', dest='command')

        self.handle_login_cmd()
    
    def create_email_service_obj_and_login(self, email):
        self.service = EmailService(email)
        self.service.start()

    def handle_login_cmd(self):
        self.parser_login_cmd = self.subparsers.add_parser('login')
        self.parser_login_cmd.add_argument(
            'email', type=str, help='an email you want to login to'
        )
        self.parser_login_cmd.set_defaults(func=self.create_email_service_obj_and_login)
    
    def parse_arguments(self):
        args = self.parser.parse_args()
        if hasattr(args, 'func'):
            if args.func == self.create_email_service_obj_and_login:
                email = args.email
                args.func(email)