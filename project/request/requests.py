from flask import Blueprint, render_template, request

from launch import DB_CONFIG, sql_provider
from db_access.db_access import querying_data
from auth.access import group_permission

requests = Blueprint('request', __name__, template_folder='templates')


@requests.route('/')
def requests_page():
    return render_template('requests_main.html')


@requests.route('/request1', methods=['POST', 'GET'])
@group_permission
def requests_request1():
    doctors = querying_data(sql_provider.get_request('request1_doctors.sql'), DB_CONFIG)
    if request.method == 'GET':
        return render_template("request1.html", patients=None, doctors=doctors)
    else:
        doctor = request.form.get('doctor')
        patients = querying_data(sql_provider.get_request('request1.sql', doctor=doctor), DB_CONFIG)
        return render_template("request1.html", patients=patients, doctors=doctors)


@requests.route('/request2', methods=['GET', 'POST'])
@group_permission
def requests_request2():
    # we can reuse sql request from 'request 1', because this function follow same filters
    doctors = querying_data(sql_provider.get_request('request1_doctors.sql'), DB_CONFIG)
    if request.method == 'GET':
        return render_template("request2.html", histories=None, doctors=doctors)
    else:
        doctor = request.form.get('doctor')
        histories = querying_data(sql_provider.get_request('request2.sql', doctor=doctor), DB_CONFIG)
        return render_template("request2.html", histories=histories, doctors=doctors)


@requests.route('/request3', methods=['POST', 'GET'])
@group_permission
def requests_request3():
    if request.method == 'GET':
        patients = querying_data(sql_provider.get_request('request3_all_patients.sql'), DB_CONFIG)
        return render_template("request3.html", patients=patients)
    else:
        date = request.form.get('date')
        patients = querying_data(sql_provider.get_request('request3.sql', birthday=date), DB_CONFIG)
        return render_template("request3.html", patients=patients)


@requests.route('/request4', methods=['POST', 'GET'])
@group_permission
def requests_request4():
    if request.method == 'GET':
        doctors = querying_data(sql_provider.get_request('request4_all_doctors.sql'), DB_CONFIG)
        return render_template("request4.html", doctors=doctors)
    else:
        employment_date = request.form.get('date')
        doctors = querying_data(sql_provider.get_request('request4.sql', employment_date=employment_date), DB_CONFIG)
        return render_template("request4.html", doctors=doctors)
