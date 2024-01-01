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

# Esta me direcciona al index.html
@app.route('/',methods=['GET','POST'])
def principal():
    
    return render_template('index.html')
#Index 
@app.route('/index',methods=['GET','POST'])
def index():
    if request.method =='POST':
        usuario = request.form['usuario']
        contra = request.form['contraseña']
        usuario_found = db.admin.find_one({'usuario':usuario,'contraseña':contra})
        if usuario_found:
            return redirect(url_for('client'))
        else:
            flash('Usuario o contraseña incorrectas')
            return redirect(url_for('index'))

#Login registro de usuarios

@app.route('/login')
def login():
    return render_template('login.html')

#Administrador
@app.route('/admin/clientes')
def client():
    return render_template('admin/clientes.html')

#Ingresado de Productos
@app.route('/admin/producto')
def producto():
    return render_template('admin/producto.html')

#Editado de clientes
@app.route('/admin/e_client')
def editcl():
    return render_template('admin/e_client.html')

#Editado de Productos
@app.route('/admin/e_product')
def eproduc():
    return render_template('admin/e_produc.html')

#Vista de Reportes 
@app.route('/admin/reportes')
def reporte():
    return render_template('admin/reportes.html')

#Vista Usuarios
@app.route('/admin/v_user')
def visuser():
    return render_template('admin/v_user.html')

#Vista de Ventas
@app.route('/admin/ventas')
def ventas():
    return render_template('admin/ventas.html')


# ---------Carpeta Usuarios


#Carpetas Usuarios
@app.route('/usuarios/clientes')
def useclient():
    return render_template('usuarios/clientes.html')

#Carpetas Usuarios productos
@app.route('/usuarios/e_client')
def useproduc():
    return render_template('usuarios/e_client.html')
#Carpetas Usuarios Editar Productos

@app.route('/usuarios/e_product')
def usedproduc():
    return render_template('usuarios/e_product.html')


if __name__ == '__main__':
    app.run(debug=True, port=3000)
