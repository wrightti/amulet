__author__ = 'xstead-master'

from flask_wtf import Form
from wtforms import StringField, HiddenField, validators
from wtforms.validators import ValidationError

# custom validators
from users import get_user_by_email
from controller import check_user_with_code


class LoginForm(Form):
    email = StringField('email', [validators.Length(min=6, max=128),
                                  validators.email()])

    def validate_email(form, field):
        if not get_user_by_email(field.data):
            raise ValidationError('Email address doesn\'t exists.')


class VerifyForm(Form):
    email = HiddenField('email')
    code = StringField('code', [validators.Length(min=4)])

    def validate_code(form, field):
        if not check_user_with_code(form.email.data, field.data):
            raise ValidationError('Entered verification code is not valid.')
