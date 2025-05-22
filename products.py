from flask import Blueprint, render_template, request, redirect, url_for, session, current_app
from models import db, Product
from werkzeug.utils import secure_filename
import os

products_bp = Blueprint('products', __name__)

@products_bp.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image = request.files['image']
        filename = secure_filename(image.filename)  # type: ignore
        image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

        product = Product(name=name, description=description, price=price, image=filename)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('products.product_list'))
    return render_template('add_product.html')


@products_bp.route('/edit-product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])

        if 'image' in request.files and request.files['image'].filename != '':
            image = request.files['image']
            filename = secure_filename(image.filename)  # type: ignore
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            product.image = filename

        db.session.commit()
        return redirect(url_for('products.product_list'))

    return render_template('edit_product.html', product=product)


@products_bp.route('/delete-product/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('products.product_list'))


@products_bp.route('/products')
def product_list():
    products = Product.query.all()
    return render_template('dashboard.html', products=products)
