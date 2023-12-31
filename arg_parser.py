from argparse import ArgumentParser
from email_service import EmailService
from email_manager import EmailManager

class ArgParser:
    def __init__(self):
        self.email_manager = EmailManager()
        self.parser = ArgumentParser()
        self.subparsers = self.parser.add_subparsers(title='command', dest='command')

        self.handle_login_cmd()
        self.handle_add_cmd()
    
    def create_email_service_obj_and_login(self):
        email = self.email_manager.load_email()
        if email is None:
            print('Use the add command to add an email.')
            return
        self.service = EmailService(email)
        self.service.start()

    def handle_login_cmd(self):
        self.parser_login_cmd = self.subparsers.add_parser('login')
        self.parser_login_cmd.set_defaults(func=self.create_email_service_obj_and_login)

    def handle_add_cmd(self):
        self.parser_login_cmd = self.subparsers.add_parser('add')
        self.parser_login_cmd.add_argument(
            'email', type=str, help='an email you want to add'
        )
        self.parser_login_cmd.set_defaults(func=self.email_manager.save_email)
    
    def parse_arguments(self):
        args = self.parser.parse_args()
        if hasattr(args, 'func'):
            if args.func == self.create_email_service_obj_and_login:
                args.func()
            elif args.func == self.email_manager.save_email:
                email = args.email
                args.func(email)
            