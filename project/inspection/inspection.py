from flask import Blueprint, request, redirect, render_template, session, url_for

from launch import sql_provider, DB_CONFIG
from db_access.db_access import querying_data, inserting_data
from auth.access import group_permission

inspection = Blueprint('inspection', __name__, template_folder='templates')


@inspection.route('/', methods=['GET'])
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
        return redirect('/inspection/spec_patient')


@inspection.route('/spec_patient', methods=['GET', 'POST'])
@group_permission
def inspect_spec_patient():
    if request.method == 'GET':
        patient = request.args.get('patient')
        doctor = request.args.get('doctor')

        patient_data = querying_data(
            sql_provider.get_request('inspection_get_patient.sql', patient=patient),
            DB_CONFIG
        )[0]

        doctor_data = querying_data(
            sql_provider.get_request('inspection_get_doctor.sql', doctor=patient_data[-1]),
            DB_CONFIG
        )[0]

        history = querying_data(
            sql_provider.get_request('inspection_get_history.sql', patient=patient),
            DB_CONFIG
        )[0]

        notes = querying_data(
            sql_provider.get_request('inspection_get_notes.sql', history=history[0]),
            DB_CONFIG
        )

        room = querying_data(
            sql_provider.get_request('inspection_get_room.sql', room_id=patient_data[8]),
            DB_CONFIG
        )[0]

        return render_template("inspect_spec_patient.html",
                               patient_data=patient_data,
                               doctor_data=doctor_data,
                               history=history,
                               notes=notes,
                               doctor=doctor,
                               room=room)
    else:
        request_type = request.form.get('request_type')
        patient = request.form.get('patient')
        doctor = request.form.get('doctor')
        history = request.form.get('history')

        if request_type == 'new_note':
            note = request.form.get('note')
            inserting_data(sql_provider.get_request('inspection_create_note.sql',
                                                    note=note,
                                                    doctor=doctor,
                                                    history=history),
                           DB_CONFIG)
            return redirect(url_for('inspection.inspect_spec_patient', patient=patient, doctor=doctor))

        if request_type == 'discharge':
            diagnose = request.form.get('diagnose')
            room_id = request.form.get('room_id')
            inserting_data(sql_provider.get_request('inspection_discharge_patient.sql',
                                                    diagnose=diagnose,
                                                    history=history),
                           DB_CONFIG)
            inserting_data(sql_provider.get_request('inspection_decrease_roommates.sql', room_id=room_id), DB_CONFIG)

            return redirect(url_for('inspection.inspect_patient'))


