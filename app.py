from flask import flash, Flask, render_template, request,Response ,jsonify, redirect, url_for
from controllers.bdatos import Conexion as dbase
from modules.clientes import Clientes
from modules.admin import Admin
from modules.productos import Productos
from modules.usuarios import Usuario
from modules.ventas import Ventas
from datetime import datetime
from collections import defaultdict

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
            return redirect(url_for("client"))
    else:
        return render_template("admin/clientes.html")
        

#Ingresado de Productos
@app.route('/admin/producto',methods=['GET','POST'])
def producto():
    if request.method == 'POST':      
        producto =db['productos']
        codigo=request.form["codigo"]
        marca=request.form["marca"]
        categoria=request.form["categoria"]
        cantidad=request.form["cantidad"]
        precio=request.form["precio"]
    
        if codigo and marca and categoria and cantidad and precio:
            regpro= Productos(codigo,marca,categoria,cantidad,precio)
            producto.insert_one(regpro.ProduDBCollection())
            return redirect(url_for('producto'))
    else:
        return render_template("admin/producto.html")

# Ingresado de Ventas
@app.route('/admin/ventas',methods=['GET','POST'])
def ventas():
    if request.method == 'POST':
            venta =db['ventas']
            usuario=request.form["usuario"]
            cliente=request.form["cliente"]
            marca=request.form["marca"]
            categoria=request.form["categoria"]
            precio=request.form["precio"]
            cambio=request.form["cambio"]
            fecha=request.form["fecha"]
        
            if usuario and cliente and marca and categoria and precio and cambio and fecha:
                regvent = Ventas(usuario ,cliente,marca,categoria, precio,cambio,fecha)
                venta.insert_one(regvent.VentaDBCollection())
                return redirect(url_for('ventas'))
    else:
        return render_template("admin/ventas.html", usuarios=adsu(), clientes=adcli(), productos=adma(),categorias=adcat())

#Vista de clientes
@app.route('/admin/e_client')
def editarcliente():
    cliente = db['clientes'].find()
    return render_template('admin/e_client.html', clientes=cliente)    


#Eliminar cliente de clientes
@app.route('/delete_cli/<string:client_name>')
def elitcl(client_name):
    clientes = db['clientes']
    clientes.delete_one({'nombre':client_name})
    return redirect(url_for('editarcliente'))

#Editar los clientes
@app.route('/edit_cli/<string:client_name>', methods=['GET', 'POST'])
def editcl(client_name):
    clientes = db['clientes']
    nombre= request.form["nombre"]
    cedula= request.form["cedula"]
    direccion=request.form["direccion"]

    if nombre and cedula and direccion:
        clientes.update_one({'nombre':client_name},{'$set':{'nombre':nombre,'cedula':cedula,'direccion':direccion}})
        return redirect(url_for('editarcliente'))
    else:
        return render_template("admin/e_client.html")

# Vista de Productos
@app.route('/admin/e_produc')
def editarproducto():
    producto = db['productos'].find()
    return render_template('admin/e_produc.html', productos=producto)

# Elimnado de Productos
@app.route('/delete_prod/<string:prod_codigo>')
def eliproduc(prod_codigo):
    producto =db['productos']
    producto.delete_one({'codigo':prod_codigo})
    return redirect(url_for('editarproducto'))        

# Editado de Productos
@app.route('/edit_prod/<string:prod_codigo>', methods=['GET', 'POST'] )
def edproduc(prod_codigo):
    producto =db['productos']
    codigo= request.form["codigo"]
    marca=request.form["marca"]
    categoria=request.form["categoria"]
    cantidad=request.form["cantidad"]
    precio=request.form["precio"]
    
    if codigo and marca and categoria and cantidad and precio:
        producto.update_one({'codigo':prod_codigo},{'$set':{'codigo':codigo,'marca':marca,'categoria':categoria,'cantidad':cantidad,'precio':precio}})
        return redirect(url_for('editarproducto'))
        
# Select Para las ventas agregar en el html
def adsu():
    usuarios = db.usuarios.find({}, {"usuario": 1})
    return [usuario['usuario'] for usuario in usuarios]

def adcli():
    clientes = db.clientes.find({}, {"nombre": 1})
    return [cliente['nombre'] for cliente in clientes]

def adma():
    productos = db.productos.find({}, {"marca": 1})
    return [producto['marca'] for producto in productos]

def adcat():
    productos = db.productos.find({}, {"categoria": 1})
    return [producto['categoria'] for producto in productos]


#Fecha para mostrar en reportes
def formatear_fecha(reportes):
    # Almacena los meses y años que ya has procesado
    meses_procesados = set()
    fechas_formateadas = []
    sumas = {}

    # Diccionario para mapear los nombres de los meses en inglés a español
    meses_en_español = {
        "January": "Enero", "February": "Febrero", "March": "Marzo", "April": "Abril",
        "May": "Mayo", "June": "Junio", "July": "Julio", "August": "Agosto",
        "September": "Septiembre", "October": "Octubre", "November": "Noviembre", "December": "Diciembre"
    }

    for reporte in reportes:
        try:
            # Intenta obtener la fecha del reporte
            fecha = reporte['fecha']
        except KeyError:
            # Si no hay un campo 'fecha', continuar con el siguiente reporte
            continue

        # Convertir la fecha a un objeto datetime
        fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")

        # Formatear la fecha al formato deseado (en inglés)
        fecha_formateada = fecha_dt.strftime("%B %Y")  # Esto dará "December 2023"

        # Traducir el nombre del mes al español
        mes, año = fecha_formateada.split()
        fecha_formateada = meses_en_español[mes] + " " + año  # Esto dará "Diciembre 2023"

        # Si el mes y año ya han sido procesados, sumar el valor de 'cambio' al total para este mes y año
        if fecha_formateada in meses_procesados:
            sumas[fecha_formateada] += float(reporte['cambio'])
        else:
            # Si el mes y año no han sido procesados, inicializar la suma de 'cambio' para este mes y año
            sumas[fecha_formateada] = float(reporte['cambio'])
            # Agregar el mes y año a los meses procesados
            meses_procesados.add(fecha_formateada)
            # Agregar la fecha formateada a la lista de fechas formateadas
            fechas_formateadas.append(fecha_formateada)

    return fechas_formateadas, sumas

#Vista de Reportes de todas las ventas que se hace por completo
@app.route('/admin/reportes')
def reporte():
    reportes = db.ventas.find()
    fechas_formateadas, sumas_como_cadenas = formatear_fecha(reportes)
    return render_template('admin/reportes.html', ventas=reportes, fechas=fechas_formateadas, sumas=sumas_como_cadenas)
#Vista Usuarios de todos los usuarios para Poder editarlos
@app.route('/admin/v_user')
def visuser():
    usuarios =db.usuarios.find()
    return render_template('admin/v_user.html', usuarios=usuarios)

#Vista de Ventas por Mecanico para visualizarlo
@app.route('/admin/v_ventas')
def v_ventas():
    # Obtener todas las ventas de la colección 'ventas'
    ventas = db.ventas.find()

    # Crear un diccionario para almacenar las ventas por usuario
    ventas_por_usuario = {}

    # Iterar sobre las ventas y sumar las cantidades por usuario
    for venta in ventas:
        usuario = venta['usuario']
        cantidad = float(venta['cambio'])  # Convertir el valor de 'cambio' a float

        # Verificar si el usuario ya está en el diccionario
        if usuario in ventas_por_usuario:
            ventas_por_usuario[usuario] += cantidad
        else:
            ventas_por_usuario[usuario] = cantidad

    # Ordenar los usuarios por la cantidad de ventas en orden descendente
    usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: x[1], reverse=True)

    # Renderizar la plantilla 'admin/v_ventas.html' con los datos necesarios
    return render_template('admin/v_ventas.html', usuarios_ordenados=usuarios_ordenados)




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
        return redirect(url_for('usuarios/e_client.html'))    


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
