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
        usuario_found2= db.usuarios.find_one({'usuario':usuario,'contraseña':contra})#Este modulo es para el usuario para ingresar a la otra pagina 
        if usuario_found:
            return redirect(url_for('client'))
        elif usuario_found2:
            return redirect(url_for('useclient'))
        else:
            flash('Usuario o contraseña incorrectas')
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


#Login registro de usuarios

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method =='POST': 
        registrar =db["usuarios"]
        cedula=request.form["cedula"]
        usuari=request.form["usuario"]
        roles=request.form["rol"]
        email=request.form["correo"]
        contra=request.form["contraseña"]

        if cedula and usuari and roles and email and contra:
            registr= Usuario(cedula,usuari,roles,email,contra)
            registrar.insert_one(registr.UserDBCollection())
            return redirect(url_for ('index'))
        else:
            return "No se encontro la pagina"
    else:
        return render_template('login.html')

#Administrador modulo de ingresado de clientes
@app.route('/admin/clientes',methods=['GET','POST'])
def client():
    if request.method == 'POST':
        clientes = db['clientes']
        nombre= request.form["nombre"]
        cedula= request.form["cedula"]
        direccion=request.form["direccion"]
        if nombre and cedula and direccion:
            regcli= Clientes(nombre,cedula,direccion)
            clientes.insert_one(regcli.ClientDBCollection())
            return redirect(url_for("admin/clientes.html"))
    else:
        return render_template("admin/clientes.html")
        

#Ingresado de Productos
@app.route('/admin/producto',methods=['GET','POST'])
def producto():
    producto =db['productos']
    codigo=request.form["codigo"]
    marca=request.form["marca"]
    categoria=request.form["categoria"]
    cantidad=request.form["cantidad"]
    precio=request.form["precio"]

    if codigo and marca and categoria and cantidad and precio:
        regpro= Productos(codigo,marca,categoria,cantidad,precio)
        producto.insert_one(regpro.ProduDBCollection())
        return redirect(url_for('admin/producto.html'))
    else:
        return print("No se mando nada a la base de datos")

# Ingresado de Ventas
@app.route('/admin/ventas',methods=['GET','POST'])
def ventas():
    venta =db['ventas']
    usuario=request.form["usuario"]
    cliente=request.form["cliente"]
    marca=request.form["marca"]
    categoria=request.form["categoria"]
    precio=request.form["precio"]
    cambio=request.form["cambio"]

    if usuario and cliente and marca and categoria and precio and cambio:
        regvent = Ventas(usuario ,cliente,marca,categoria, precio,cambio)
        venta.insert_one(regvent.VentDBCollection())
        return redirect(url_for('admin/ventas.html'))
    else:
        return print("No se mando nada a la base de datos")
    

#Eliminar cliente de clientes
@app.route('/delete_cli/<string:client_name>')
def elitcl(client_name):
    clientes = db['clientes']
    clientes.delete_one({'nombre':client_name})
    return redirect(url_for('admin/clientes.html'))

#Editar los clientes
@app.route('/edit_cli/<string:client_name>', methods=['GET', 'POST'])
def editcl(client_name):
    clientes = db['clientes']
    if request.method == 'POST':
        nombre= request.form["nombre"]
        cedula= request.form["cedula"]
        direccion=request.form["direccion"]

        if nombre and cedula and direccion:
            clientes.update_one({'nombre':client_name},{'$set':{'nombre':nombre,'cedula':cedula,'direccion':direccion}})
            return redirect(url_for('admin/clientes.html'))
        else:
            return print("No se mando nada a la base de datos")
    
# Elimnado de Productos
@app.route('/delete_prod/<string:prod_codigo>')
def eliproduc(prod_codigo):
    producto =db['productos']
    producto.delete_one({'codigo':prod_codigo})
    return render_template('admin/e_produc.html')        
 
#Editado de Productos
@app.route('/edit_prod/<string:prod_codigo>')
def edproduc(prod_codigo):
    producto =db['productos']
    if request.method == 'POST':
        codigo= request.form["codigo"]
        marca=request.form["marca"]
        categoria=request.form["categoria"]
        cantidad=request.form["cantidad"]
        precio=request.form["precio"]
        
        if codigo and marca and categoria and cantidad and precio:
            producto.update_one({'codigo':prod_codigo},{'$set':{'codigo':codigo,'marca':marca,'categoria':categoria,'cantidad':cantidad,'precio':precio}})
            return redirect(url_for('admin/e_producto.html'))
        
    return render_template('admin/e_produc.html')

#Vista de Reportes de todas las ventas que se hace por completo
@app.route('/admin/reportes')
def reporte():
    reportes =db.ventas.find()
    return render_template('admin/reportes.html',ventas=reportes)

#Vista Usuarios de todos los usuarios para Poder editarlos
@app.route('/admin/v_user')
def visuser():
    usuarios =db.usuarios.find()
    return render_template('admin/v_user.html', usuarios=usuarios)

#Vista de Ventas por Mecanico para visualizarlo
@app.route('/admin/v_ventas')
def v_ventas():
    ventas =db.ventas.find()
    return render_template('admin/v_ventas.html',ventas=ventas)


# ---------Carpeta Usuarios------------------------------


#Carpetas Usuarios

#Ingresado de Clientes los mecanicos
@app.route('/usuarios/clientes')
def useclient():
    clientes= db['clientes']
    nombre= request.form["nombre"]
    cedula= request.form["cedula"]
    direccion=request.form["direccion"]

    if nombre and cedula and direccion:
        regcli= Clientes(nombre,cedula,direccion)
        clientes.insert_one(regcli.ClientDBCollection())
        return redirect(url_for("usuarios/clientes.html"))
    return render_template('usuarios/clientes.html')

#Editado de Clientes de los mecanicos

@app.route('/edit_cliusu/<string:client_name>', methods=['GET', 'POST'])
def editcluse(client_name):
    clientes = db['clientes']
    if request.method == 'POST':
        nombre= request.form["nombre"]
        cedula= request.form["cedula"]
        direccion=request.form["direccion"]
        
        if nombre and cedula and direccion:
            clientes.update_one({'nombre':client_name},{'$set':{'nombre':nombre,'cedula':cedula,'direccion':direccion}})
            return redirect(url_for('usuarios/e_client.html'))
    else:
        return print("No se mando nada a la base de datos")    


#Carpetas Usuarios para mostrar los clientes 
@app.route('/usuarios/e_client')
def vuse_cliente():
    cliente = db.cliente.find()
    return render_template('usuarios/e_client.html', cliente=cliente)



#Carpetas Usuarios Ingresado de Productos 

@app.route('/usuarios/producto')
def usedproduc():
    producto= db.product["productos"]
    codigo=request.form["codigo"]
    marca=request.form["marca"]
    categoria=request.form["categoria"]
    cantidad=request.form["cantidad"]
    precio=request.form["precio"]
    
    if codigo and marca and categoria and cantidad and precio:
        regpro= Productos(codigo,marca,categoria,cantidad,precio)
        producto.insert_one(regpro.ProduDBCollection())
        return redirect(url_for('usuarios/producto.html'))                        
    else:
        return print("No se mando nada a la base de datos")

# Carpeta de vistado de productos 
@app.route('/useedit_prod/<string:prod_codigo>')
def useediproduc(prod_codigo):
    producto =db['productos']
    if request.method == 'POST':
        codigo= request.form["codigo"]
        marca=request.form["marca"]
        categoria=request.form["categoria"]
        cantidad=request.form["cantidad"]
        precio=request.form["precio"]
        
        if codigo and marca and categoria and cantidad and precio:
            producto.update_one({'codigo':prod_codigo},{'$set':{'codigo':codigo,'marca':marca,'categoria':categoria,'cantidad':cantidad,'precio':precio}})
            return redirect(url_for('usuarios/e_product.html'))
        
    else:
        return print("No se mando nada a la base de datos")

    
#Carpeta vista de productos
@app.route('/usuarios/e_product')
def vuse_producto():
    producto = db.productos.find()
    return render_template('usuarios/e_product.html', producto=producto)    


if __name__ == '__main__':
    app.run(debug=True, port=3000)
