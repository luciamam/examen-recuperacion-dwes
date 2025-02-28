from flask import Flask,render_template, redirect, request,url_for,flash
from flask_bootstrap import Bootstrap4 
from dotenv import load_dotenv
from formularios.forms import RegisterUser,LoginUser
from pymongo import MongoClient
import os
load_dotenv



#AQUI ES DONDE REALIZAMOS LA CONEXION A MONGODB 
client = MongoClient("localhost", 27017)
#accedemos a  la base de datos ,aunque si en mogo no se encuentra la crea 
db = client['MibasedeDatosUsuarios']
#creamos la collecction 
users_collection=db['usuarios']





app=Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
Bootstrap4(app)



@app.route('/')
def home():
    return render_template('Home.html')


@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterUser()
    datos=request.form

    if request.method=='POST':
        #vamos a segurarnos que el formualrio este validaddo , en caso contrario que no se puede enviar estos datos 
        if not form.validate_on_submit():
            return redirect(url_for('register'))
        else:
            #guardamos los datos de nuestro usuario a la base de datos 
            usuario={
                'username':datos['username'],
                'password':datos['password'],
                'fullname':datos['fullname']
            }
            users_collection.insert_one(usuario)
            return redirect(url_for('perfil'))
            

    return render_template('RegistrarUsuario.html',form=form)


@app.route('/login')
def login():
    form=LoginUser()
    return render_template('LoginUsuario.html',form=form)


#es siempre bueno manejar  el 404 de forma personilaza 
@app.errorhandler(404)
def pagina_404(error):
    return "<h1> Este recurso no se encuentra 😎</h1>"


#la ruta perfil tiene que esta protegida en esste caso lo vamos a proteger con el token jwt 
@app.route('/perfil')
def perfil():
    return "bienvenido usuario "




if __name__=='__main__':
    app.run(debug=True)