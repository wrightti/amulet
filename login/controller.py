__author__ = 'xstead-master'
import random, string, os
import config, datetime, fileinput
from users import get_user_by_email

import time
from sinchsms import SinchSMS

#
# generate random pin code
# xxxx digit
#
def generate_random_code():
    return ''.join(random.choice(string.digits) for _ in range(4))


#
# check user login data
# check email == USEREMAIL,
#       phone == USERPHONE,
#       code == VALID
#
def check_user_with_code(email='', code=''):
    try:
        data = read_data_from_file()

        if data:

            match = [j for i, j in data if i == email]

            #todo: check phone valid!
            if match:
                return (match[0].get('code') == code)
            else:
                return False
        else:
            return False

    except Exception as e:
        print(e)


#
# save user login data
#
#   email;phone;generated pin;datetime
#   email;phone;generated pin;datetime
#   ...
#   ...
#
def save_user_with_code(email='', code=''):
    try:

        make_dir(config.data_dir)

        user_data = get_user_by_email(email)

        if user_data:
            save_data_into_file(
                ';'.join(
                    [email.encode('utf-8'),
                     user_data.get('phone').encode('utf-8'),
                     code.encode('utf-8'),
                     datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
                )
            )

        return user_data.get('phone') if user_data else None


    except Exception as e:
        print(e)

#
# write login data into file
# data file set in config.py
#
def save_data_into_file(r):
    try:

        data_file = os.path.join(config.data_dir, config.data_file)
        f = open(data_file,'a+')
        f.write(r+"\n")
        f.close()

    except Exception, e:
        raise e

#
# read login data from file
# data file set in config.py
# security time check
# pin code valid until "config.code_valid_in_minutes" minutes only
#
# return dict, {email,phone,code,timestamp}
#
def read_data_from_file():

    result = {}

    try:

        security_date = datetime.datetime.now()-datetime.timedelta(minutes=config.code_valid_in_minutes)

        data_file = os.path.join(config.data_dir, config.data_file)
        with open(data_file) as f:
            content = f.readlines()

        for user in content:
            email = user.rstrip('\n').split(';')[0]
            phone = user.rstrip('\n').split(';')[1]
            code = user.rstrip('\n').split(';')[2]
            time_ = user.rstrip('\n').split(';')[3]
            date_object = datetime.datetime.strptime(time_, '%Y-%m-%d %H:%M:%S')

            if date_object > security_date:
                 result[email] = {'email': email, 'phone': phone, 'code': code, 'time': date_object}

        return sorted(result.iteritems())

    except Exception, e:
        raise e


#
# remove user from login file
# when successfully logged in
#
def delete_user_from_data(email=''):

    data_file = os.path.join(config.data_dir, config.data_file)
    for line in fileinput.input(data_file, inplace=True):
        if email in line:
            continue
        print(line.rstrip('\n'))

#
# make directory if doesnt exists
#
def make_dir(dir_path):
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    except Exception, e:
        raise e

#
# send pin code sms
#
def send_sinch_sms(number='', code=''):

    message = ('Your verification code is: %s' % code)

    client = SinchSMS(config.sinch_sms_app_key,
                      config.sinch_sms_secret)

    print("Sending '%s' to %s" % (message, number))

    #
    #todo: handle repsonse
    # not important to check
    # more security when you save the message id too!
    #

    sms_sent_response = client.send_message(number, message)

    """
    message_id = sms_sent_response['messageId']
    sms_status_response = client.check_status(message_id)

    while sms_status_response['status'] != 'Successful':
        print(sms_status_response['status'])
        time.sleep(4)
        sms_status_response = client.check_status(message_id)
        print(sms_status_response['status'])
    """
