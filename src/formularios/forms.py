from flask_wtf import FlaskForm
from wtforms import StringField, EmailField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,Email,EqualTo

class RegisterUser(FlaskForm):
    username=StringField("username",validators=[DataRequired(),Length(min=6,max=12)])
    fullname=StringField("fullname",validators=[DataRequired(),Length(min=6,max=20)])
    password=StringField("password",validators=[DataRequired(),Length(min=6,max=20)])
    submit=SubmitField("Registrarse")
    
class LoginUser(FlaskForm):
     username=StringField("username",validators=[DataRequired(),Length(min=6,max=12)])
     password=StringField("password",validators=[DataRequired(),Length(min=6,max=20)])
     Submit=SubmitField('Inciar Sesion')



    