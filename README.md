# PyMail
A CLI email client built with Python.

## Setting Up The Email Client
This section will guide you through the setup process, including cloning the repository, setting up a permanent alias for convenient access, and getting credentials from the google dev console for API access.

### Dependencies

- cryptography
- requests
- urwid

You can install these dependencies using pip:
```bash
pip install cryptography
pip install requests
pip install urwid
```

### Creating a Permanent Alias
For convenience, you can create a permanent alias that allows you to access the mail client from any directory in your terminal.

Open your terminal and navigate to your home directory:
```bash
cd ~
```
Edit your shell profile file. Depending on the shell you're using (bash, zsh, etc.), the file could be one of the following:

- For bash, use ~/.bashrc or ~/.bash_profile
- For zsh, use ~/.zshrc

For example, if you're using bash:
```bash
nano ~/.bashrc
```

Add the following line at the end of the file to create an alias:
```bash
alias pymail="python /path/to/PyMail/main.py"
```
Replace /path/to/PyMail with the actual path to the directory where you cloned the repository.
1. Save and close the file (for nano, press Ctrl + X, then Y, and finally Enter).
2. To apply the changes, either restart your terminal or run the following command:
```bash
source ~/.bashrc
```

### Troubleshooting: Permission Denied Error

If you encounter a "permission denied" error when trying to run the mail client, it might be due to the lack of execution permissions on the `main.py` file. To resolve this issue, follow these steps:

Open your terminal or command prompt. Navigate to the directory where the `main.py` file is located using the `cd` command:
```bash
cd/path/to/PyMail
   ```
Check the current permissions on the `main.py` file using the `ls -l` command:
```bash
ls -l main.py
```
Ensure that the file has the necessary execution permissions. If it doesn't, you can add them using the chmod command:
```bash
chmod +x main.py
```

### Setting Up Credentials for Google API Access
To interact with Gmail services through the CLI email client, you'll need to provide your own credentials obtained from the Google Developer Console. Here's how you can do it:

1. Access the Google Developer Console: Navigate to the Google Developer Console.


2. Create a New Project (if needed): If you don't already have a suitable project, create a new one by clicking "Select a project" at the top left corner and then selecting "New Project".


3. Configure OAuth2 Consent Screen:
    - After setting up the project, click on "OAuth consent screen" from the left-hand menu.
    - Choose either "External" (for personal use) or "Internal" (for organization-wide use) and fill in the necessary information.


4. Generate OAuth2 Credentials:
    - Proceed to the "Credentials" tab in the left-hand menu.
    - Click "Create Credentials" and select "OAuth client ID".
    - Choose "Desktop App" as the application type.


5. Specify Redirect URIs:
    - Under the "Authorized redirect URIs" section, add "urn:ietf:wg:oauth:2.0:oob". This URI is crucial for out-of-band (OOB) authorization.


6. Choose Scopes:
    - Scopes define the access levels your app requests from the user. For the CLI email client, ensure you select at least the "https://mail.google.com/" scope to access Gmail.


7. Download Credentials:
    - Upon creating the OAuth client ID, you'll be able to download a JSON file containing your credentials. Save this file securely.


8. Integrate Credentials into the App:
    - Run the app and follow the prompts to paste the path to the downloaded JSON credentials file.
    - These credentials will enable the CLI email client to authenticate with Gmail services. Keep your credentials confidential and never share them publicly. Note that the app doesn't include the actual credentials, requiring you to provide them locally.

## Logging In

To login first add your email using the `add` command then use the `login` command:
```bash
pymail add some@email.com
pymail login
```

If its your first time using the client, you will be prompted to create a password, give access, and import credentials. You only have to do this once.


## Current Features
The email client currently supports the following features:
1. Storage with Fernet Encryption
    - Your email client settings and data are securely stored locally using the Fernet encryption scheme. This encryption ensures that your sensitive information remains confidential and protected even if unauthorized access occurs.

2. Gmail Authentication Flow
    - Easily authenticate with your Gmail account using the built-in authentication flow. Your credentials are handled securely, allowing you to access your Gmail inbox seamlessly.

3. IMAP Connection
    - Establish a secure IMAP connection to your Gmail account, enabling real-time access to your email messages. The IMAP protocol ensures efficient and synchronized communication between the client and your Gmail inbox.

4. Inbox Display and Email Selection
    - View your inbox directly within the email client's interface. Browse through your emails with ease and select the ones you want to interact with.

5. Email Content Display in Plaintext
    - When selecting an email, its contents are displayed in plaintext format, making it convenient to read and understand the message's content.

