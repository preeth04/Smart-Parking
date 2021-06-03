from flask.helpers import url_for
from werkzeug.utils import redirect


from functools import wraps
from flask import session,redirect,url_for
def driver_login_required(test):
    @wraps(test)
    def driver_decorator(*args,**kwargs):
        if not session["driver_login"]:
            return redirect(url_for('Userdetails'))
        return test(*args,**kwargs)
    return driver_decorator


def driver_vehicle_login_required(test):
    @wraps(test)
    def driver_vehicle_decorator(*args,**kwargs):
        if not session['vehicle_login']:
            return redirect(url_for('Vehicledetails'))
        return test(*args,**kwargs)
    return driver_vehicle_decorator

def admin_login_required(test):
    @wraps(test)
    def admin_decorator(*args,**kwargs):
        if not session["admin_login"]:
            return redirect(url_for('login'))
        return test(*args,**kwargs)
    return admin_decorator
