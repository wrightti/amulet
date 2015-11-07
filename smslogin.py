from flask import Flask
from flask import render_template, redirect, url_for, session
from flask.ext.session import Session

# login modul
from login import *

# init app
app = Flask(__name__)

# set views
@app.route('/')
@app.route('/login', methods=['GET','POST'], strict_slashes=False)
def login():

    # debug
    # force check user logged in
    if 'user' in session:
        return redirect(url_for('logged_in'))

    return login_form()


@app.route('/verify_code', methods=['POST'], strict_slashes=False)
@app.route('/verify_code/<path:email>', methods=['GET','POST'], strict_slashes=False)
def verify_code(email=''):
    return verify_code_form(email)


@app.route('/logged_in', methods=['GET'], strict_slashes=False)
def logged_in():
    return render_template('logged_in.html')


@app.route('/logout', methods=['GET'], strict_slashes=False)
def logout():
    session.clear()
    return redirect(url_for('login'))

# run app
if __name__ == '__main__':

    # app conf
    app.secret_key = 'c%&w8f&j_#8g4)u(ttj9v)n0t@5rgt%2^z#km4f1c9nmvnk=*y'
    app.config["CACHE_TYPE"] = "null"
    app.config['SESSION_TYPE'] = 'filesystem'

    # inti session
    # http://pythonhosted.org/Flask-Session/
    sess = Session()
    sess.init_app(app)

    app.run()
