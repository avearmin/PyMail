import os
import pickle
import json
from cryptography.fernet import Fernet


class CredentialsManager:
    def __init__(self, domain: str):
        self.code_dir = os.path.dirname(os.path.abspath(__file__))
        self.credentials_path = os.path.join(
            self.code_dir, "credentials", f"{domain}_credentials.bin"
        )

    def encrypt(self, key: bytes, credential: str) -> bytes:
        f = Fernet(key)
        return f.encrypt(credential.encode())

    def decrypt(self, key: bytes, credential: bytes) -> str:
        f = Fernet(key)
        return f.decrypt(credential).decode()

    def verify_credentials_dir(self):
        cred_dir = os.path.join(self.code_dir, "credentials")
        if not os.path.exists(cred_dir):
            os.mkdir(cred_dir)

    def import_credentials(self, key: bytes, path: str):
        if not os.path.exists(path):
            print("Credentials not found.")
            return
        credentials = self.load_credentials()
        with open(path, "r") as json_file:
            json_data = json.load(json_file)
        credentials["client_id"] = self.encrypt(
            key, json_data["installed"]["client_id"]
        )
        credentials["client_secret"] = self.encrypt(
            key, json_data["installed"]["client_secret"]
        )
        self.save_credentials(credentials)

    def load_credentials(self) -> dict:
        self.verify_credentials_dir()
        if not os.path.exists(self.credentials_path):
            credentials = {}
            return credentials
        with open(self.credentials_path, "rb") as file:
            credentials = pickle.load(file)
        return credentials

    def save_credentials(self, credentials: str):
        self.verify_credentials_dir()
        with open(self.credentials_path, "wb") as file:
            pickle.dump(credentials, file)

    def save_refresh_token(self, key: bytes, refresh_token: str):
        credentials = self.load_credentials()
        credentials["refresh_token"] = self.encrypt(key, refresh_token)
        self.save_credentials(credentials)

    def save_client_id(self, key: bytes, client_id: str):
        credentials = self.load_credentials()
        credentials["client_id"] = self.encrypt(key, client_id)
        self.save_credentials(credentials)

    def save_client_secret(self, key: bytes, client_secret: str):
        credentials = self.load_credentials()
        credentials["client_secret"] = self.encrypt(key, client_secret)
        self.save_credentials(credentials)

    def load_refresh_token(self, key: bytes) -> str:
        credentials = self.load_credentials()
        if "refresh_token" in credentials:
            return self.decrypt(key, credentials["refresh_token"])

    def load_client_id(self, key: bytes) -> str:
        credentials = self.load_credentials()
        if "client_id" in credentials:
            return self.decrypt(key, credentials["client_id"])

    def load_client_secret(self, key: bytes) -> str:
        credentials = self.load_credentials()
        if "client_secret" in credentials:
            return self.decrypt(key, credentials["client_secret"])


class GoogleCredentialsManager(CredentialsManager):
    def __init__(self):
        super().__init__("google")