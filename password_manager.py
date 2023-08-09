import os
import pickle
import hashlib
import base64
from getpass import getpass

class PasswordManager:
    def __init__(self):
        self.code_dir = os.path.dirname(os.path.abspath(__file__))
        self.password_path = os.path.join(
            self.code_dir, "config", f"password.bin"
        )
    
    def generate_salt(self, len: int=16) -> bytes:
        return os.urandom(len)

    def add_salt(self, password: str, salt: bytes) -> str:
        salt_as_str = base64.b64encode(salt).decode()
        return password + salt_as_str

    def hash_password(self, salted_password: str) -> bytes:
        encoded_password = salted_password.encode()
        hashed_password = hashlib.sha3_256(encoded_password).digest()
        return hashed_password
    
    def verify_config_dir(self):
        config_dir = os.path.join(self.code_dir, "config")
        if not os.path.exists(config_dir):
            os.mkdir(config_dir)
    
    def load_config(self) -> dict:
        self.verify_config_dir()
        if not os.path.exists(self.password_path):
            data = {}
            return data
        with open(self.password_path, "rb") as file:
            data = pickle.load(file)
        return data
    
    def save_config(self, data: dict):
        self.verify_config_dir()
        with open(self.password_path, "wb") as file:
            pickle.dump(data, file)
    
    def save_salt(self, salt: bytes):
        config = self.load_config()
        config["salt"] = salt
        self.save_config(config)
    
    def load_salt(self) -> bytes:
        config = self.load_config()
        if "salt" in config:
            return config["salt"]

    def save_password(self, password: str):
        config = self.load_config()
        salt = self.load_salt()
        if not salt:
            print("Could not find salt.")
            return
        salted_password = self.add_salt(password, salt)
        hashed_password = self.hash_password(salted_password)
        config["password"] = hashed_password
        self.save_config(config)
    
    def load_password(self) -> str:
        config = self.load_config()
        if "password" in config:
            return config["password"]
    
    def verify_password(self, password: str) -> bool:
        salt = self.load_salt()
        salted_password = self.add_salt(password, salt)
        hashed_password = self.hash_password(salted_password)
        saved_password = self.load_password()
        return hashed_password == saved_password
    
    def verify_setup(self):
        salt = self.load_salt()
        password = self.load_password()
        return salt is not None or password is not None

    def setup(self):
        if not self.verify_setup():
            salt = self.generate_salt()
            self.save_salt(salt)
            password = getpass("Enter a password: ")
            self.save_password(password)
    
    def get_derived_key(self, password: str) -> bytes:
        salt = self.load_salt()
        key = hashlib.pbkdf2_hmac(
            hash_name="sha256",
            password=password.encode(),
            salt=salt,
            iterations=100000,
            dklen=32,
        )
        return base64.urlsafe_b64encode(key)
