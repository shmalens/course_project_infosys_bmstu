from flask import Blueprint, session, render_template, redirect, request

from db_access.db_access import querying_data
from launch import sql_provider, DB_CONFIG

auth = Blueprint('auth', __name__, template_folder='templates')


@auth.route('/', methods=['GET', 'POST'])
def auth_login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login')
        password = request.form.get('password')
        auth_data = querying_data(sql_provider.get_request('auth.sql', login=login), DB_CONFIG)
        if auth_data:
            if auth_data[0][0] == password:
                session['group'] = auth_data[0][1]
                session['user_id'] = auth_data[0][2]
        return redirect('/')


@auth.route('/exit')
def auth_exit():
    if 'group' in session:
        session.pop('group')
    if 'user_id' in session:
        session.pop('user_id')
    return redirect('/')
