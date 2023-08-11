# PyMail
A CLI email client built with Python.

## Setting Up Credentials for Google API Access
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

## Future Updates
1. **Secure Info Storage:** Implement encryption/decryption to securely store users' email credentials and master password for access.

2. **User-API-Middleman:** Create a middleman that connects to the correct API based on the email domain to interact with different email service providers.

3. **Email Fetching:** Fetch emails from the connected email accounts using the respective APIs.

4. **Email Parsing:** Parse email content, including headers, body, attachments (if applicable), and other metadata.

5. **Email Sending:** Enable users to send emails through the CLI, supporting attachments and multiple recipients.

6. **CLI Interface:** Design and implement a user-friendly command-line interface that allows users to manage multiple email accounts, view email statistics, read emails, send emails, and perform other relevant actions efficiently.
