from functools import wraps

from flask import session, request, redirect

from launch import ACCESS_CONFIG


def group_permission_validation():
    group_name = session.get('group', 'unauthorized')
    target_app = "" if len(request.endpoint.split('.')) == 1 else request.endpoint.split('.')[1]

    if (group_name in ACCESS_CONFIG) and (target_app in ACCESS_CONFIG[group_name]):
        return True
    return False


def group_permission(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if group_permission_validation():
            return func(*args, **kwargs)
        return redirect('/')

    return wrapper
