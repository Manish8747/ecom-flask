import os
from flask import Flask, redirect, request, send_from_directory, url_for, session, render_template
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_SECRET_KEY
from auth import auth_bp
from models import db, Product
from flask_jwt_extended import JWTManager  # type: ignore
from werkzeug.utils import secure_filename
from products import products_bp


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp)


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
    if 'access_token' not in session:
        return redirect(url_for('auth.login'))
    products = Product.query.all()
    return render_template('dashboard.html', products=products)




@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)




@app.route('/logout', methods=['POST'])
def logout():
    """ Logout and redirect to login """
    session.pop('access_token', None)
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True)
