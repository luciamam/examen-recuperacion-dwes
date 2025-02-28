from flask import Flask,render_template, redirect, request
from flask_bootstrap import Bootstrap4 
from dotenv import load_dotenv
from formularios.forms import RegisterUser,LoginUser
import os
load_dotenv





app=Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
Bootstrap4(app)



@app.route('/')
def home():
    return "home"


@app.route('/register')
def register():
    form=RegisterUser()
    return render_template('RegistrarUsuario.html',form=form)


@app.route('/login')
def login():
    form=LoginUser()
    return render_template('LoginUsuario.html',form=form)


#es siempre bueno manejar  el 404 de forma personilaza 
@app.errorhandler(404)
def pagina_404(error):
    return "<h1> Este recurso no se encuentra 😎</h1>"




if __name__=='__main__':
    app.run(debug=True)