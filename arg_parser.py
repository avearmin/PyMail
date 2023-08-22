from argparse import ArgumentParser
from email_service import EmailService
from email_list_manager import EmailListManager

class ArgParser:
    def __init__(self):
        self.email_list_manager = EmailListManager()
        self.parser = ArgumentParser()
        self.subparsers = self.parser.add_subparsers(title='command', dest='command')

        self.handle_login_cmd()
        self.handle_add_cmd()
        self.handle_del_cmd()
    
    def create_email_service_obj_and_login(self, email):
        email_list = self.email_list_manager.load_email_list()
        if email not in email_list:
            print(f'{email} not found. Use add command to add it.')
            return
        self.service = EmailService(email)
        self.service.start()

    def handle_login_cmd(self):
        self.parser_login_cmd = self.subparsers.add_parser('login')
        self.parser_login_cmd.add_argument(
            'email', type=str, help='an email you want to login to'
        )
        self.parser_login_cmd.set_defaults(func=self.create_email_service_obj_and_login)

    def handle_add_cmd(self):
        self.parser_login_cmd = self.subparsers.add_parser('add')
        self.parser_login_cmd.add_argument(
            'email', type=str, help='an email you want to add'
        )
        self.parser_login_cmd.set_defaults(func=self.email_list_manager.write_email_to_list)
    
    def handle_del_cmd(self):
        self.parser_login_cmd = self.subparsers.add_parser('del')
        self.parser_login_cmd.add_argument(
            'email', type=str, help='an email you want to delete'
        )
        self.parser_login_cmd.set_defaults(func=self.email_list_manager.delete_email_from_list)
    
    def parse_arguments(self):
        args = self.parser.parse_args()
        if hasattr(args, 'func'):
            if args.func == self.create_email_service_obj_and_login:
                email = args.email
                args.func(email)
            elif args.func == self.email_list_manager.write_email_to_list:
                email = args.email
                args.func(email)
            elif args.func == self.email_list_manager.delete_email_from_list:
                email = args.email
                args.func(email)
            