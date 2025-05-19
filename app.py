from flask import Flask, jsonify
from config import SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the E-commerce App!"})

if __name__ == '__main__':
    app.run(debug=True)
