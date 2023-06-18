from flask import Flask, render_template, request

app = Flask(__name__)  # app instance


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email = request.form['email']
        start_date = request.form['start_date']
        occupation = request.form['occupation']

    return render_template('index.html')


app.run(debug=True, port=5001)
