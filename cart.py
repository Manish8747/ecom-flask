from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from models import Product  # Assuming you already have a Product model
from mail_config import send_order_email

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/')
def view_cart():
    cart = session.get('cart', {})
    items = []
    total = 0

    for product_id, quantity in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            subtotal = product.price * quantity
            items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
            total += subtotal

    return render_template('cart.html', items=items, total=total)

@cart_bp.route('/add/<int:product_id>')
def add_to_cart(product_id):
    cart = session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session['cart'] = cart
    flash('Product added to cart!', 'success')
    return redirect(url_for('products.product_list'))

@cart_bp.route('/remove/<int:product_id>')
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    cart.pop(str(product_id), None)
    session['cart'] = cart
    flash('Product removed from cart.', 'info')
    return redirect(url_for('cart.view_cart'))


@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart = session.get('cart', {})
    products = Product.query.filter(Product.id.in_(cart.keys())).all() if cart else []

    if request.method == 'POST':
        user_email = request.form.get('email')
        if not user_email:
            flash('Please enter your email address.')
            return redirect(url_for('cart.checkout'))

        order_details = ""
        total = 0
        for product in products:
            quantity = cart.get(str(product.id), 0)
            line_total = product.price * quantity
            total += line_total
            order_details += f"{product.name} - Qty: {quantity} - Price: ₹{line_total}\n"

        order_details += f"\nTotal Amount: ₹{total}"

        try:
            send_order_email(user_email, order_details)
            flash('Order placed successfully! Confirmation email sent.')
            session.pop('cart', None)  # clear cart
            return redirect(url_for('cart.checkout'))
        except Exception as e:
            flash(f"Failed to send email: {str(e)}")
            return redirect(url_for('cart.checkout'))

    return render_template('checkout.html', products=products)
