# Amulet
2-Step Authentication Using Email &amp; SMS Code



Mac OS X
==========================================

    1. INSTALL PYTHON
    ==========================================

        Method "A":
        ==========================================

            1.1 INSTALL BREW
            ------------------------------------------
                http://brew.sh/

            1.2 INSTALL PYTHON
            ------------------------------------------
                brew install python
                after successfully finished: (brew link python)

        Method "B":
        ==========================================

            Install PyCharm IDE (https://www.jetbrains.com/pycharm/)


    2. INSTALL VIRTUALENV
    ------------------------------------------
        sudo pip install virtualenv


    3. SETUP VENV FOR PROJECT
    ------------------------------------------
        cd project directory and run:
        virtualenv  -p python2.7 venv


    4. INSTALL REQUIREMENTS FOR PROJECT
    ------------------------------------------

        4.1 INSTALL PACKAGES
        ------------------------------------------
        venv/bin/pip install -r requirements.txt

        4.2 SETUP SINCH SMS API
        ------------------------------------------
            - create developer acc,
            - create app,
            - get your app && secret key
            - https://www.sinch.com/dashboard/#/signup

        /smslogin/login/config.py --> (last 2 lines)
            sinch_sms_app_key = ''
            sinch_sms_secret  = ''


        4.3 CREATE FAKE USERS
        ------------------------------------------
        /smslogin/users/users.dat

            - 1 user / 1 line
            - first field: email, second field: phone number
            - e.g.:
                bob@example.com;+18001234567
                ...
                etc...


    5. RUN
    ------------------------------------------
    venv/bin/python smslogin.py
