from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, IntegerField, ValidationError
from wtforms.validators import DataRequired, EqualTo

from expenses_app import db
from expenses_app.models import User, Group


class RegistrationForm(FlaskForm):
    name = StringField('Vardas', [DataRequired()])
    email = StringField('El. paštas', [DataRequired()])
    password = PasswordField('Slaptažodis', [DataRequired()])
    password_repeat = PasswordField("Pakartokite slaptažodį", [EqualTo('password', "Slaptažodžiai turi sutapti.")])
    submit = SubmitField('Registruotis')

    def validate_email(self, field):
        email = field.data
        if User.query.filter_by(email=email).count() > 0:
            raise ValidationError('Vartotojas su tokiu el. pašto adresu jau egzistuoja')


class LoginForm(FlaskForm):
    email = StringField('El. paštas', [DataRequired()])
    password = PasswordField('Slaptažodis', [DataRequired()])
    submit = SubmitField('Prisijungti')



class JoinGroupForm(FlaskForm):
    group_id = IntegerField('Grupės ID', [DataRequired()])
    submit = SubmitField('Prisijungti')

    def validate_group_id(self, field):
        group = Group.query.get(field.data)
        if group is None:
            raise ValidationError('Grupė nerasta')
        else:
            if group in current_user.groups:
                raise ValidationError('Prie šios grupės jau prisijungta')

    
class ExpenseForm(FlaskForm):
    amount = IntegerField('Suma', [DataRequired()])
    description = StringField('Aprašymas', [DataRequired()])
    submit = SubmitField('Pridėti', [DataRequired()])
