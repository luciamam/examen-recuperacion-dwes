from flask import Flask,render_template, redirect, request,url_for,make_response
from flask_bootstrap import Bootstrap4 
from dotenv import load_dotenv
from formularios.forms import RegisterUser,LoginUser
from pymongo import MongoClient
#para proteger la ruta vamos a usar el jwt y vamos a guardar el token en la cookie
from flask_jwt_extended import JWTManager ,jwt_required, create_access_token, get_jwt_identity
import os
load_dotenv
import json




#AQUI ES DONDE REALIZAMOS LA CONEXION A MONGODB 
client = MongoClient("localhost", 27017)
#accedemos a  la base de datos ,aunque si en mogo no se encuentra la crea 
db = client['MibasedeDatosUsuarios']
#creamos la collecction 
users_collection=db['usuarios']

app=Flask(__name__)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')
jwt=JWTManager(app)
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

            #como voy a guardar el token en la cookie necesito el make-reponse para cambios en la respuesta(response) de mi servidor 
            response=make_response(redirect(url_for('perfil')))

            create_token=create_access_token(identity=str({'fullname':datos['fullname']}))
            response.set_cookie('access_token_cookie',create_token)
            users_collection.insert_one(usuario)
            return response
            

    return render_template('RegistrarUsuario.html',form=form)


@app.route('/login')
def login():
    form=LoginUser()
    return render_template('LoginUsuario.html',form=form)


#es siempre bueno manejar  el 404 de forma personilaza 
@app.errorhandler(404)
def pagina_404(error):
    return "<h1> Este recurso no se encuentra 😎</h1>"



#manejo de error del 401 , le redirecciono al usario al login  para que no  le salga  la respuesta por defecto 
@jwt.unauthorized_loader
def manejar_error_401(mensaje):
    return redirect(url_for('login'))


#la ruta perfil tiene que esta protegida en esste caso lo vamos a proteger con el token jwt 
@app.route('/perfil')
@jwt_required(locations=['cookies'])
def perfil():
    current_user=get_jwt_identity()
    current_user=current_user.replace("'",'"')
    current_user=json.loads(current_user)
    fullname=current_user['fullname']
    return "bienvenido {}".format(fullname)




if __name__=='__main__':
    app.run(debug=True)