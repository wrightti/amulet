from flask import request, render_template, \
    redirect, url_for, session
from forms import LoginForm, VerifyForm
from controller import *


def login_form():

    try:

        form = LoginForm(request.form, csrf_enabled=False)

        if request.method == 'POST' and form.validate():

            pin_code = generate_random_code()
            phone_number = save_user_with_code(email=request.form.get('email'),
                                               code=pin_code)

            print("User phone: %s" % phone_number)

            try:
                # send pin code via SMS
                send_sinch_sms(phone_number, pin_code)

            except Exception as e:
                #todo: error handling
                print(e)
                pass

            return redirect(url_for('verify_code', email=request.form.get('email')))

        return render_template('login.html', form=form)

    except Exception as e:
        #todo: error handling
        print(e)


def verify_code_form(email=''):

    try:

        form = VerifyForm(request.form, csrf_enabled=False)

        if request.method == 'GET':
            form.email.data = email

        if request.method == 'POST' and form.validate():

            # set session
            session['user'] = request.form.get('email')

            # delete user from temporary
            delete_user_from_data(request.form.get('email'))

            # redirect
            return redirect(url_for('logged_in'))


        return render_template('verify.html', form=form)

    except Exception as e:
        #todo: error handling
        print(e)