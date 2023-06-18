from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from datetime import datetime

app = Flask(__name__)  # app instance

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applicants_data.db'

# mail configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'my.projects.with.python@gmail.com'
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASSWORD')

db = SQLAlchemy(app)  # db instance

mail = Mail(app)  # mail instance


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    start_date = db.Column(db.Date)
    occupation = db.Column(db.String(20))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        start_date = request.form['start_date']
        date_object = datetime.strptime(start_date, '%Y-%m-%d')
        occupation = request.form['occupation']

        form = FormData(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        start_date=date_object,
                        occupation=occupation)
        db.session.add(form)
        db.session.commit()
        message_body = f"Hi, You have received a new application.\n\nHere are the details:\n" \
                       f"Full name : {first_name} {last_name}\n" \
                       f"Email : {email}\n" \
                       f"Ready to join from : {start_date}\n" \
                       f"Current employment status : {occupation}\n\n" \
                       f"Regards."
        message = Message(subject='New Application Received',
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']],
                          body=message_body
                          )
        mail.send(message)

        flash(f"Hi {first_name}, Your data is submitted successfully.", 'success')
        db.session.close()
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
