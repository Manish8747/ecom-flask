from flask_mail import Mail, Message  # type: ignore
from flask import current_app

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_order_email(recipient, order_details):
    # Compose HTML email content
    html_body = f"""
    <html>
    <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color:#f9f9f9; padding:20px;">
      <div style="max-width:600px; margin:auto; background:#fff; border-radius:12px; padding:20px; box-shadow:0 0 10px rgba(0,0,0,0.1);">
        <h2 style="color:#6e3cbc;">Thank you for your order!</h2>
        <p>We have received your order and it is being processed.</p>
        <h3 style="color:#48b1f5;">Order Details:</h3>
        <pre style="background:#eee; padding:15px; border-radius:8px; font-size:14px; white-space: pre-wrap;">{order_details}</pre>
        <p style="margin-top: 30px; font-size: 14px; color: #555;">
          If you have any questions, feel free to reply to this email.
        </p>
        <p style="font-weight:600; color:#6e3cbc;">Happy Shopping! 🛒</p>
      </div>
    </body>
    </html>
    """

    msg = Message(
        subject="Your Order Confirmation - Thank You!",
        sender=current_app.config['MAIL_USERNAME'],
        recipients=[recipient],
        html=html_body
    )
    mail.send(msg)
