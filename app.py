from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)  # app instance
app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applicants_data.db'

db = SQLAlchemy(app)  # db instance


class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(20))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        start_date = request.form['start_date']
        occupation = request.form['occupation']

    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
