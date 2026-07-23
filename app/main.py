from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify

# Create Flask app FIRST
app = Flask(__name__)

# Import after creating app to avoid circular imports
from .config import Config
from .db import db, User, CommonPassword
from .auth import PasswordValidator, AuthManager

# Configure app
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

def is_common_password(password):
    return CommonPassword.is_common(password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = AuthManager.login_user(
            request.form.get('username'),
            request.form.get('password')
        )
        if result['success']:
            session['user_id'] = result['user'].id
            session['username'] = result['user'].username
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash(result.get('error', 'Invalid login'), 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm = request.form.get('confirm_password')
        
        if password != confirm:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        
        result = AuthManager.register_user(username, email, password, is_common_password)
        if result['success']:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        else:
            for error in result.get('errors', []):
                flash(error, 'danger')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out', 'info')
    return redirect(url_for('index'))

@app.route('/password-strength', methods=['POST'])
def password_strength():
    password = request.json.get('password', '')
    strength = PasswordValidator.get_strength(password)
    is_common = is_common_password(password)
    validation = PasswordValidator.validate(password, is_common_password)
    return jsonify({
        'strength': strength,
        'is_common': is_common,
        'valid': validation['valid'],
        'errors': validation['errors']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)