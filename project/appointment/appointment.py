from flask import Blueprint, request, redirect, render_template

from launch import sql_provider, DB_CONFIG, ROOMS_AMOUNT, MAX_PATIENTS_IN_ROOM
from db_access.db_access import querying_data, inserting_data
from auth.access import group_permission

appointment = Blueprint('appointment', __name__, template_folder='templates')


@appointment.route('/new_patient', methods=['GET', 'POST'])
@group_permission
def appointment_new_patient():
    if request.method == 'GET':
        doctors = querying_data(sql_provider.get_request('appointment_get_doctors.sql'), DB_CONFIG)
        patients = querying_data(sql_provider.get_request('appointment_get_referrals.sql'), DB_CONFIG)
        rooms = querying_data(
            sql_provider.get_request(
                'appointment_get_rooms.sql',
                max_patient_amount=MAX_PATIENTS_IN_ROOM
            ),
            DB_CONFIG
        )
        print(rooms)
        return render_template(
            'appointment_new_patient.html',
            patients=patients,
            doctors=doctors,
            rooms=rooms
        )
    else:
        patient_referral_id = request.form.get('patient')
        doctor_id = request.form.get('doctor')
        room_id = request.form.get('room')

        patient = querying_data(
            sql_provider.get_request(
                'appointment_get_patient_data.sql',
                referral_id=patient_referral_id
            ),
            DB_CONFIG
        )[0]

        print(patient)

        inserting_data(
            sql_provider.get_request(
                'appointment_new_patient.sql',
                first_name=patient[1],
                second_name=patient[2],
                surname=patient[3],
                birthday=patient[4],
                address=patient[5],
                passport=patient[6],
                doctor=doctor_id,
                room=room_id
            ),
            DB_CONFIG
        )

        inserting_data(
            sql_provider.get_request(
                'appointment_increase_roommates.sql',
                room_id=room_id
            ),
            DB_CONFIG
        )
        patient_id = querying_data(sql_provider.get_request('appointment_get_patient_id.sql'), DB_CONFIG)[0][0]
        inserting_data(
            sql_provider.get_request(
                'appointment_create_history.sql',
                diagnose=patient[7],
                patient=patient_id
            ),
            DB_CONFIG
        )

        inserting_data(sql_provider.get_request('appointment_delete_referral.sql', referral_id=patient_referral_id), DB_CONFIG)

        return redirect('/appointment/new_patient')
