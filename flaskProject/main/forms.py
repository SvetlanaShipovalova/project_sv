from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email

class SimpleForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
   # email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
   # confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
   # gender = SelectField('Пол', choices=[('Мужской', 'Мужской'), ('Женский', 'Женский')])
    submit = SubmitField('Авторизоваться')