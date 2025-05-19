from flask import Flask, redirect, url_for, session, render_template
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_SECRET_KEY
from auth import auth_bp
from models import db
from flask_jwt_extended import JWTManager  # type: ignore

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    """ Redirect to login if not logged in """
    if 'access_token' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    """ Render Dashboard page """
    if 'access_token' in session:
        return render_template('dashboard.html')
    return redirect(url_for('auth.login'))

@app.route('/logout', methods=['POST'])
def logout():
    """ Logout and redirect to login """
    session.pop('access_token', None)
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=True)
