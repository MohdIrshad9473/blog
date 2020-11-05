from flask_mail import Mail, Message
from View import app
mail = Mail(app)


class utility:
    def send_mail(subject, recipients, mailbody):  # common for sending email
        msg = Message(subject=subject,  recipients=recipients)
        msg.html = mailbody
        mail.send(msg)




