import os, pickle
from cryptography.fernet import Fernet


class CredentialsManager:
    
    def __init__(self, domain: str):
         self.code_dir = os.path.dirname(os.path.abspath(__file__))
         self.credentials_path =  os.path.join(self.code_dir, "credentials", f"{domain}_credentials.bin")
    
    def encrypt(self, key: bytes, credentials: str) -> bytes:
        f = Fernet(key)
        return f.encrypt(credentials.encode())
    
    def decrypt(self, key: bytes, credentials: bytes) -> str:
        f = Fernet(key)
        return f.decrypt(credentials).decode()
    
    def verify_credentials_dir(self):
        cred_dir = os.path.join(self.code_dir, "credentials")
        if not os.path.exists(cred_dir):
            os.mkdir(cred_dir)

    def load_credentials(self, key: bytes) -> dict:
        self.verify_credentials_dir()
        if not os.path.exists(self.credentials_path):
            credentials = {}
            return credentials
        with open(self.credentials_path, "rb") as file:
            credentials = pickle.load(file)
        return self.decrypt(key, credentials)
        
    def save_credentials(self, key: bytes, credentials: str):
        self.verify_credentials_dir()
        encrypted_credentials = self.encrypt(key, credentials)
        with open(self.credentials_path, "wb") as file:
            pickle.dump(encrypted_credentials, file)
        
    def save_refresh_token(self, key: bytes, refresh_token: str):
        credentials = self.load_credentials(key)
        credentials["refresh_token"] = refresh_token
        self.save_credentials(key, credentials)
        
    def save_client_id(self, key: bytes, client_id: str):
        credentials = self.load_credentials(key)
        credentials["client_id"] = client_id
        self.save_credentials(key, credentials)
    
    def save_client_secret(self, key: bytes, client_secret: str):
        credentials = self.load_credentials(key)
        credentials["client_secret"] = client_secret
        self.save_credentials(key, credentials)
    
    def load_refresh_token(self, key: bytes) -> str:
        credentials = self.load_credentials(self, key)
        if "refresh_token" in credentials:
            return credentials["refresh_token"]
            
    def load_client_id(self, key: bytes) -> str:
        credentials = self.load_credentials(self, key)
        if "client_id" in credentials:
            return credentials["client_id"]
    
    def load_client_secret(self, key: bytes) -> str:
        credentials = self.load_credentials(self, key)
        if "client_secret" in credentials:
            return credentials["client_secret"]

class GoogleCredentialsManager(CredentialsManager):
    
    def __init__(self):
        super().__init__("google")