import os
from flask import Flask, redirect, request, send_from_directory, url_for, session, render_template, flash
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, JWT_SECRET_KEY
from auth import auth_bp
from models import db, Product
from flask_jwt_extended import JWTManager  # type: ignore
from werkzeug.utils import secure_filename
from products import products_bp
from cart import cart_bp
from dotenv import load_dotenv

# Mail imports
from mail_config import mail, init_mail, send_order_email

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY

# Email service variables loaded from .env
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# Initialize Flask-Mail
init_mail(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # create folder if it doesn't exist
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)

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
    
    # Get cart from session and count total quantity
    cart = session.get('cart', {})
    cart_count = sum(cart.values())  # total number of items in the cart

    return render_template('dashboard.html', products=products, cart_count=cart_count)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/logout', methods=['POST'])
def logout():
    """ Logout and redirect to login """
    session.pop('access_token', None)
    return redirect(url_for('auth.login'))

# New Checkout route
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        email = request.form.get('email')
        cart = session.get('cart', {})
        if not email:
            flash("Please enter your email to place the order.", "warning")
            return redirect(url_for('checkout'))

        if not cart:
            flash("Your cart is empty.", "warning")
            return redirect(url_for('dashboard'))

        # Build order details string
        products = Product.query.filter(Product.id.in_(cart.keys())).all()
        order_details = ""
        for product in products:
            quantity = cart.get(str(product.id), 0)
            order_details += f"{product.name} - Quantity: {quantity}\n"

        try:
            send_order_email(email, order_details)
            flash("Order placed successfully! Confirmation email sent.", "success")
            session.pop('cart', None)  # clear cart after order
        except Exception as e:
            flash(f"Failed to send email: {str(e)}", "danger")

        return redirect(url_for('dashboard'))

    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)
