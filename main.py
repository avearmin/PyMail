from email_service import EmailService

email = input('Enter a google email: ')
e = EmailService(email)
e.start()