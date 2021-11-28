from flask import Blueprint, request, redirect, render_template, session

from launch import sql_provider, DB_CONFIG
from db_access.db_access import querying_data, inserting_data
from auth.access import group_permission

inspection = Blueprint('inspection', __name__, template_folder='templates')


@inspection.route('/', methods=['GET', 'POST'])
@group_permission
def inspect_patient():
    if request.method == 'GET':
        doctor = querying_data(
            sql_provider.get_request('inspection_get_doctor_id.sql', account=session['user_id']),
            DB_CONFIG
        )[0][0]
        self_patients = querying_data(
            sql_provider.get_request('inspection_self_patients.sql', doctor=doctor),
            DB_CONFIG
        )
        other_patients = querying_data(
            sql_provider.get_request('inspection_other_patients.sql', doctor=doctor),
            DB_CONFIG
        )
        return render_template(
            'inspection.html',
            self_patients=self_patients,
            other_patients=other_patients,
            doctor=doctor
        )
    else:
        doctor = request.form.get('doctor')
        patient = request.form.get('patient')
        history = querying_data(
            sql_provider.get_request('inspection_get_history_id.sql', patient=patient),
            DB_CONFIG
        )[0][0]
        inserting_data(
            sql_provider.get_request('inspection_create_note.sql', doctor=doctor, history=history),
            DB_CONFIG
        )
        return redirect('/inspection')
