from flask import flash, Flask, render_template, request,Response ,jsonify, redirect, url_for
from controllers.bdatos import Conexion as dbase
from modules.clientes import Clientes
from modules.admin import Admin
from modules.productos import Productos
from modules.usuarios import Usuario
from modules.ventas import Ventas

db = dbase()

app = Flask(__name__)
app.secret_key = 'mecanicajulio'

#Index 
@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')

#Login registro de usuarios

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

#Administrador
@app.route('/admin/clientes',methods=['GET','POST'])
def client():
    return render_template('admin/clientes.html')

#Ingresado de Productos
@app.route('/admin/producto',methods=['GET','POST'])
def producto():
    return render_template('admin/producto.html')

#Editado de clientes
@app.route('/admin/e_client',methods=['GET','POST'])
def editcl():
    return render_template('admin/e_client.html')

#Editado de Productos
@app.route('/admin/e_product',methods=['GET','POST'])
def eproduc():
    return render_template('admin/e_produc.html')

#Vista de Reportes 
@app.route('/admin/reportes',methods=['GET','POST'])
def reporte():
    return render_template('admin/reportes.html')

#Vista Usuarios
@app.route('/admin/v_user',methods=['GET','POST'])
def visuser():
    return render_template('admin/v_user.html')

#Vista de Ventas
@app.route('/admin/ventas',methods=['GET','POST'])
def ventas():
    return render_template('admin/ventas.html')


# ---------Carpeta Usuarios


#Carpetas Usuarios
@app.route('/usuarios/clientes',methods=['GET','POST'])
def useclient():
    return render_template('usuarios/clientes.html')

#Carpetas Usuarios productos
@app.route('/usuarios/e_client',methods=['GET','POST'])
def useproduc():
    return render_template('usuarios/e_client.html')
#Carpetas Usuarios Editar Productos

@app.route('/usuarios/e_product',methods=['GET','POST'])
def useproduc():
    return render_template('usuarios/e_product.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
