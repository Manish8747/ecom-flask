```markdown
# 🛒 Flask E-Commerce Learning Project

This is a simplified **e-commerce-style web application** built using **Flask and Python**. It is designed for educational purposes to teach students the fundamentals of web development including:

- Routing
- Blueprints
- Templates
- User authentication (Register/Login)
- Environment variables
- Flash messages
- Modular structure

> ⚙️ This project is built using **only Flask and Python**, making it perfect for beginners.

---

## 📁 Project Structure
```

e_commerce/
├── app.py # Main application entry point
├── config.py # Environment variable loader
├── .env # Secret keys and environment configs
├── .gitignore # Ignore unnecessary files like virtual env, .env, etc.
├── requirements.txt # Python dependencies
├── auth.py # Auth routes (register/login)
├── products.py # Placeholder for product logic
├── cart.py # Placeholder for cart logic
├── orders.py # Placeholder for orders logic
├── models.py # In-memory user data
├── utils.py # Placeholder for helper functions
├── static/ # CSS or JS assets
│ └── css/
│ └── styles.css
└── templates/ # HTML templates
├── base.html
└── auth/
├── register.html
└── login.html

````

---

## 🚀 Features

- 🧱 Modular structure using Flask Blueprints
- 🔐 User registration and login using Flask forms
- 🔒 Password validation (plain text for learning)
- 📦 Flash messaging for user feedback
- 📁 Organized templates and static assets
- 📌 `.env` file for managing secrets
- 📚 Teachable structure – everything explained for students

---

## ✅ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/e_commerce.git
cd e_commerce
````

### 2. Create Virtual Environment and Activate

```bash
python -m venv env
# Windows
env\Scripts\activate
# Mac/Linux
source env/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Add `.env` File

Create a `.env` file in the root:

```
SECRET_KEY=supersecretkey
```

### 5. Run the App

```bash
python app.py
```

Then go to: [http://127.0.0.1:5000/auth/register](http://127.0.0.1:5000/auth/register)

---

## 🧠 Learning Goals

- Understand request/response cycle in Flask
- Learn the use of Blueprints for modular code
- Use HTML templates with Jinja2
- Manage state using sessions and cookies (in later stages)
- Apply secure coding with secrets stored in `.env`
- Build a scalable structure for future additions

---

## 🔮 Future Additions (Covered in Later Days)

- JWT Authentication
- Product listing & cart functionality
- Order management
- Role-based access
- Persistent database integration

---

## 📌 License

This project is for educational purposes only. Use it freely in your classrooms or workshops.

---

## 🙋‍♂️ Author

**Instructor:** \[Amogh Pathak]
**LinkedIn:** [linkedin.com/in/yourname](https://linkedin.com/in/yourname)

```

```
