from flask import Flask, render_template

from request.requests import requests
from auth.auth import auth
from appointment.appointment import appointment
from inspection.inspection import inspection

app = Flask(__name__)
app.register_blueprint(requests, url_prefix='/requests')
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(appointment, url_prefix='/appointment')
app.register_blueprint(inspection, url_prefix='/inspection')

app.secret_key = "MY SUPER SECRET KEY"


@app.route("/")
def app_start_page():
    return render_template('main.html')


@app.route("/exit")
def app_end_of_work():
    return render_template('exit.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
