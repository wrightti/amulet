
# users stored in file:
#
#   user@email.com;phone_number
#   user@email.com;phone_number
#   user@email.com;phone_number
#   ...
#   ...
import os
data_file = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'users.dat')

#
# read users
def get_users():

    result = {}

    try:

        with open(data_file) as f:
            content = f.readlines()

        for user in content:
            email = user.rstrip('\n').split(';')[0]
            phone  = user.rstrip('\n').split(';')[1]

            result[email] = {'email': email, 'phone': phone}

        return sorted(result.iteritems())

    except Exception, e:
        raise e

#
# get user by email
def get_user_by_email(email=''):
    if not email:
        return None

    match = [j for i, j in get_users() if i == email]
    return match[0] if match else None