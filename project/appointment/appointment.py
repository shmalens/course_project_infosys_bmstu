from flask import Blueprint, request, redirect, render_template

from launch import sql_provider, DB_CONFIG
from db_access.db_access import querying_data, inserting_data
from auth.access import group_permission

appointment = Blueprint('appointment', __name__, template_folder='templates')


@appointment.route('/new_patient', methods=['GET', 'POST'])
@group_permission
def appointment_new_patient():
    if request.method == 'GET':
        doctors = querying_data(sql_provider.get_request('request1_doctors.sql'), DB_CONFIG)
        return render_template('appointment_new_patient.html', doctors=doctors)
    else:
        first_name = request.form.get('first_name')
        second_name = request.form.get('second_name')
        surname = request.form.get('surname')
        birthday = request.form.get('birthday')
        address = request.form.get('address')
        passport = request.form.get('passport')
        diagnose = request.form.get('diagnose')
        doctor = request.form.get('doctor')

        inserting_data(
            sql_provider.get_request('appointment_new_patient.sql', first_name=first_name, second_name=second_name,
                                     surname=surname, birthday=birthday, address=address, passport=passport,
                                     doctor=doctor), DB_CONFIG)
        patient_id = querying_data(sql_provider.get_request('appointment_new_patient_id.sql'), DB_CONFIG)
        inserting_data(
            sql_provider.get_request('appointment_new_history.sql', diagnose=diagnose, patient=patient_id[0][0]),
            DB_CONFIG)
        return redirect('/')


@appointment.route('/rewrite', methods=['GET', 'POST'])
@group_permission
def appointment_rewrite_patient():
    if request.method == 'GET':
        patients = querying_data(sql_provider.get_request('appointment_rewrite_patients.sql'), DB_CONFIG)
        return render_template('appointment_rewrite.html', patients=patients)
    else:
        patient = request.form.get('patient')
        diagnose = request.form.get('diagnose')
        inserting_data(
            sql_provider.get_request('appointment_new_history.sql', diagnose=diagnose, patient=patient),
            DB_CONFIG)
        return redirect('/')
