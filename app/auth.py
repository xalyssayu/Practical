import re
from .db import User, db

class PasswordValidator:
    @staticmethod
    def validate(password, common_check_func):
        errors = []
        if len(password) < 12:
            errors.append("Password must be at least 12 characters long")
        if len(password) > 128:
            errors.append("Password must not exceed 128 characters")
        if common_check_func and common_check_func(password):
            errors.append("Password is too common")
        return {'valid': len(errors) == 0, 'errors': errors}

    @staticmethod
    def get_strength(password):
        score = 0
        if len(password) >= 12: score += 25
        if len(password) >= 16: score += 15
        if len(password) >= 20: score += 10
        if re.search(r'[a-z]', password): score += 10
        if re.search(r'[A-Z]', password): score += 10
        if re.search(r'\d', password): score += 10
        if re.search(r'[^a-zA-Z0-9\s]', password): score += 10
        return min(score, 100)

class AuthManager:
    @staticmethod
    def register_user(username, email, password, common_check_func):
        validation = PasswordValidator.validate(password, common_check_func)
        if not validation['valid']:
            return {'success': False, 'errors': validation['errors']}
        
        if User.query.filter_by(username=username).first():
            return {'success': False, 'errors': ['Username already exists']}
        
        if User.query.filter_by(email=email).first():
            return {'success': False, 'errors': ['Email already registered']}
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {'success': True, 'user': user}
    
    @staticmethod
    def login_user(username, password):
        user = User.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {'success': False, 'error': 'Invalid username or password'}
        return {'success': True, 'user': user}