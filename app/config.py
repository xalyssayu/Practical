import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OWASP C7 Level 1 Password Requirements
    MIN_PASSWORD_LENGTH = 12
    MAX_PASSWORD_LENGTH = 128
    
    # Path to common passwords file
    COMMON_PASSWORDS_FILE = '/app/data/common_passwords.txt'