from flask import flash, Flask,session, render_template, request,Response ,jsonify, redirect, url_for
from pymongo import ReturnDocument
from controllers.bdatos import Conexion as dbase
from modules.clientes import Clientes
from modules.admin import Admin
from modules.productos import Productos
from modules.usuarios import Usuario
from modules.ventas import Ventas
from datetime import datetime,timedelta
from collections import defaultdict
from babel.dates import format_date 
from bson import json_util
import json

db = dbase()

app = Flask(__name__)
app.secret_key = 'mecanicajulio'

@app.route('/logout')
def logout():
    # Elimina el usuario de la sesión si está presente
    session.pop('username', None)
    return redirect(url_for('index'))


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
        usuario_found2= db.usuarios.find_one({'usuario':usuario,'contraseña':contra})#Este modulo es para el usuario  
        if usuario_found:
            session['usuario'] = usuario
            session["username"]= usuario_found["usuario"]
            return redirect(url_for('client'))
        elif usuario_found2:
            session["username"]= usuario_found2["usuario"]
            session['usuario'] = usuario
            return redirect(url_for('useclient'))
        else:
            flash('Usuario o contraseña incorrectas')
            return redirect(url_for('index'))
    else:
        return render_template('index.html')


#Login registro de usuarios

@app.route('/admin/in_mecanicos',methods=['GET','POST'])
def login():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method =='POST': 
        registrar =db["usuarios"]
        cedula=request.form["cedula"]
        usuari=request.form["usuario"]
        roles=request.form["rol"]
        email=request.form["correo"]
        contra=request.form["contraseña"]

        existing_cedula = registrar.find_one({'cedula':cedula})
        existing_usuari = registrar.find_one({'usuario':usuari})

        if existing_cedula :
            flash("Ya existe un usuario con esa cedula")
            return redirect(url_for('login'))
        elif existing_usuari:
            flash("Ya existe ese nombre de usuario ")
            return redirect(url_for('login'))
        else:
            registr= Usuario(cedula,usuari,roles,email,contra)
            registrar.insert_one(registr.UserDBCollection())
            flash("Guardado a la base de datos ")
            return redirect(url_for ('login'))
    else:
        return render_template('admin/in_mecanicos.html')

# *Administrador modulo de ingresado de clientes
@app.route('/admin/clientes',methods=['GET','POST'])
def client():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method == 'POST':
        clientes = db['clientes']
        nombre= request.form["nombre"]
        cedula= request.form["cedula"]
        direccion=request.form["direccion"]
        
        existing_nombre = clientes.find_one({'nombre':nombre})
        existing_cedula = clientes.find_one({'cedula':cedula})

        if existing_nombre:
            flash("Ya existe un cliente con esa cedula")
            return redirect(url_for('client'))
        elif existing_cedula:
            flash("Ya existe un cliente con esa cedula")
            return redirect(url_for('client'))
        else:
            regcli= Clientes(nombre,cedula,direccion)
            clientes.insert_one(regcli.ClientDBCollection())
            flash("Guardado a la base datos")
            return redirect(url_for("client"))
    else:
        return render_template("admin/clientes.html")
        

# * Ingresado de Productos
@app.route('/admin/producto',methods=['GET','POST'])
def producto():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    # Define codigo fuera del bloque if/else
    codigo = None

    if request.method == 'POST':      
        producto =db['productos']
        codigo_counter = db['codigo_counter']
        
        # Obtén el último valor del contador y actualízalo
        counter = codigo_counter.find_one_and_update(
            {'_id': 'producto_id'},
            {'$inc': {'value': 1}},
            return_document=ReturnDocument.AFTER
        )
        codigo = counter['value']
        
        categoria=request.form["categoria"]
        precio=request.form["precio"]
        
        # Validacion si existe esa categoria
        existing_categoria = producto.find_one({"categoria": categoria}) 
        
        if existing_categoria:
            flash("Ya existe esa categoria")
            return redirect(url_for('producto'))

        if categoria  and precio:
            regpro= Productos(codigo,categoria,precio)
            producto.insert_one(regpro.ProduDBCollection())
            flash("Guardado en la base de datos")
            return redirect(url_for('producto'))
    else:
        # Pasa el código a la plantilla
        return render_template("admin/producto.html")

# Ingresado de Ventas
@app.route('/admin/ventas',methods=['GET','POST'])
def ventas():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method == 'POST':
        venta = db['ventas']
        codigo_counter = db['codigo_counter']
        # Obtén el último valor del contador y actualízalo
        counter = codigo_counter.find_one_and_update(
            {'_id': 'ventaID'},
            {'$inc': {'value': 1}},
            return_document=ReturnDocument.AFTER
        )
        id_venta = counter['value']
        usuario = request.form["usuario"]
        cliente = request.form["cliente"]
        cedula = request.form["cedula"]
        categorias = request.form["categoria"]
        precios = request.form["precio"]
        cantidades = request.form["cantidad"]
        cambio = request.form["cambio"]
        fecha = request.form["fecha"]
    
        if id_venta and usuario and cliente and cedula and categorias and precios and cantidades and cambio and fecha:
            regvent = Ventas(id_venta,usuario ,cliente,cedula,categorias, precios,cantidades,cambio,fecha)
            venta.insert_one(regvent.VentaDBCollection())
            flash("Guardado en la base de datos")
            return redirect(url_for('ventas'))
    else:   
        return render_template("admin/ventas.html", usuarios=adsu(), clientes=adcli(),categorias=adcat())

#Para obtener un Id en ventas 
def get_next_sequence_value(sequence_name):
    document = db['counters'].find_one_and_update(
        {'_id': sequence_name }, 
        {'$inc': {'sequence_value': 1}},
        return_document=ReturnDocument.AFTER
    )
    return document['sequence_value']

# Para buscar al cliente con la cedula 
@app.route('/get_cliente_nombre', methods=['GET'])
def get_cliente_nombre():
    cedula = request.args.get('cedula')
    cliente = db.clientes.find_one({"cedula": cedula}, {"nombre": 1})
    if cliente:
        return cliente['nombre']
    else:
        return ""
    
@app.route('/get_producto_precio', methods=['GET'])
def get_producto_precio():
    categoria = request.args.get('categoria')
    producto = db.productos.find_one({"categoria": categoria}, {"precio": 1})
    if producto:
        return str(producto['precio'])
    else:
        return ""


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
@app.route('/delete_prod/<int:prod_codigo>')
def eliproduc(prod_codigo):
    producto =db['productos']
    producto.delete_one({'codigo':prod_codigo})
    return redirect(url_for('editarproducto'))        

# Editado de Productos
@app.route('/edit_prod/<int:prod_codigo>', methods=['GET', 'POST'] )
def edproduc(prod_codigo):
    producto =db['productos']
    codigo= request.form["codigo"]
    categoria=request.form["categoria"]
    precio=request.form["precio"]
    
    if codigo  and categoria  and precio:
        producto.update_one({'codigo':prod_codigo},{'$set':{'codigo':codigo,'categoria':categoria,'precio':precio}})
        return redirect(url_for('editarproducto'))

#* Reporte de Productos 

@app.route('/admin/r_productos')
def r_productos():
    # Obtener todas las ventas de la colección 'ventas'
    ventas = db.ventas.find()

    # Crear un diccionario para almacenar las ventas por usuario
    ventas_por_usuario = {}

    # Iterar sobre las ventas y sumar las cantidades por usuario
    for venta in ventas:
        usuario = venta['categoria']
        cantidad = int(venta['cantidad'])
        fecha = venta ["fecha"]  

        # Convertir la fecha a formato español
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_es = format_date(fecha, 'MMMM yyyy', locale='es_ES')

        # Verificar si el usuario ya está en el diccionario
        if usuario in ventas_por_usuario:
            ventas_por_usuario[usuario]['ventas'] += cantidad
            ventas_por_usuario[usuario]['fecha'] = fecha_es
        else:
            ventas_por_usuario[usuario] = {'ventas': cantidad, 'fecha': fecha_es}

    # Ordenar los usuarios por la cantidad de ventas en orden descendente
    usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: x[1]['ventas'], reverse=True)

    
    return render_template('admin/r_productos.html', usuarios_ordenados=usuarios_ordenados)
        


# Select Para las ventas agregar en el html
def adsu():
    usuarios = db.usuarios.find({}, {"usuario": 1})
    return [usuario['usuario'] for usuario in usuarios]

def adcli():
    clientes = db.clientes.find({}, {"nombre": 1, "cedula": 1})
    return [(cliente['cedula'], cliente['nombre']) for cliente in clientes]


def adcat():
    productos = db.productos.find({}, {"categoria": 1,"precio":1})
    return [(producto['categoria'], producto['precio']) for producto in productos]


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
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    reportes = db.ventas.find()
    fechas_formateadas, sumas_como_cadenas = formatear_fecha(reportes)
    return render_template('admin/reportes.html', ventas=reportes, fechas=fechas_formateadas, sumas=sumas_como_cadenas)

# * Vista Usuarios de todos los usuarios para Poder editarlos
@app.route('/admin/v_user')
def visuser():
    usuarios =db.usuarios.find()
    return render_template('admin/v_user.html', usuarios=usuarios)

# * Eliminar los v_user
@app.route('/delete_user/<string:user_name>')
def eliuser(user_name):
    user =db['usuarios']
    user.delete_one({'usuario':user_name})
    return redirect(url_for('visuser'))

#* Editar los v_user
@app.route('/edit_use/<string:user_name>', methods=['GET', 'POST'])
def editus(user_name):
    user = db['usuarios']
    cedula = request.form['cedula']
    usuario = request.form['usuario']
    rol = request.form['rol']
    email = request.form['correo']
    contraseña = request.form['contraseña']
    
    if cedula and usuario and rol and email and contraseña:
        user.update_one({'cedula':user_name},{'$set':{'cedula':cedula,'usuario':usuario,'rol':rol,'correo':email,'contraseña':contraseña}})
        return redirect(url_for('visuser'))
    else:
        return render_template("admin/v_user.html")


# * Vista de Ventas por Mecanico para visualizarlo
@app.route('/admin/v_ventas')
def v_ventas():
    # Obtener todas las ventas de la colección 'ventas'
    ventas = db.ventas.find()

    # Crear un diccionario para almacenar las ventas por usuario
    ventas_por_usuario = {}

    # Iterar sobre las ventas y sumar las cantidades por usuario
    for venta in ventas:
        usuario = venta['usuario']
        cantidad = float(venta['cambio'])
        fecha = venta ["fecha"]  

        # Convertir la fecha a formato español
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        fecha_es = format_date(fecha, 'MMMM yyyy', locale='es_ES')

        # Verificar si el usuario ya está en el diccionario
        if usuario in ventas_por_usuario:
            ventas_por_usuario[usuario]['ventas'] += cantidad
            ventas_por_usuario[usuario]['fecha'] = fecha_es
        else:
            ventas_por_usuario[usuario] = {'ventas': cantidad, 'fecha': fecha_es}

    # Ordenar los usuarios por la cantidad de ventas en orden descendente
    usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: x[1]['ventas'], reverse=True)

    # Renderizar la plantilla 'admin/v_ventas.html' con los datos necesarios
    return render_template('admin/v_ventas.html', usuarios_ordenados=usuarios_ordenados)

@app.route('/admin/comprobante', methods=['GET'])
def comprobante():
    id_venta = request.args.get('id_venta')
    venta = None

    if id_venta:
        id_venta = int(id_venta)  # Convierte id_venta a un número
        venta = db.ventas.find_one({'id_venta': id_venta})

    return render_template('admin/comprobante.html', venta=venta)



@app.route('/get_venta_info')
def get_venta_info():
    id_venta = request.args.get('id', type=int)
    venta = db.ventas.find_one({'id_venta': id_venta})
    if venta:
        return json.dumps(venta, default=json_util.default)
    else:
        return jsonify({'error': 'No se encontró la venta'})

# * Editar ventas de mecanicos 

# * Vista ventas de todos los usuarios para Poder editarlos
@app.route('/admin/e_venta')
def e_venta():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    venta =db.ventas.find()
    return render_template('admin/e_venta.html',ventas=venta )

# * Eliminar ventas
@app.route('/delete_venta/<string:venta_name>')
def elive(venta_name):
    venta =db['ventas']
    venta.delete_one({'usuario':venta_name})
    return redirect(url_for('e_venta'))

#* Editar los v_user
@app.route('/edit_venta/<string:venta_name>', methods=['GET', 'POST'])
def editve(venta_name):
    venta = db['ventas']
    id_venta =request.form['id_venta']
    usuario = request.form['usuario']
    cliente = request.form['cliente']
    cedula = request.form['cedula']
    categoria = request.form['categoria']
    precio = request.form['precio']
    cantidad = request.form['cantidad']
    cambio = request.form['cambio']
    fecha = request.form['fecha']
    
    if id_venta and usuario and cliente and cedula and categoria and precio and cantidad and cambio and fecha:
        venta.update_one({'id_venta':venta_name},{'$set':{'id_venta':id_venta ,'usuario':usuario,'cliente':cliente, 'cedula':cedula, 'categoria':categoria,'precio':precio, 'cantidad':cantidad, 'cambio':cambio,'fecha':fecha}})
        return redirect(url_for('e_venta'))
    else:
        return render_template("admin/e_venta.html")

# Vista de reportes diarios de todos lo mecanicos
@app.route('/admin/rep_diario')
def repodia(): 
        # Verifica si el usuario está en la sesión
        if 'username' not in session:
            flash("Inicia sesion con tu usuario y contraseña")
            return redirect(url_for('index'))
        # Obtener todas las ventas de la colección 'ventas'
        ventas = db.ventas.find()
        
        # Crear un diccionario para almacenar las ventas por usuario
        ventas_por_usuario = {}
        
        # Iterar sobre las ventas y sumar las cantidades por usuario
        for venta in ventas:
            usuario = venta['usuario']
            cantidad = float(venta['cambio'])
            fecha = venta ["fecha"]  
        
            # Convertir la fecha a formato español
            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_es = format_date(fecha, 'EEEE d MMMM yyyy', locale='es_ES')
        
            # Verificar si el usuario ya está en el diccionario
            if usuario in ventas_por_usuario:
                # Verificar si la fecha ya está en el diccionario del usuario
                if fecha_es in ventas_por_usuario[usuario]:
                    ventas_por_usuario[usuario][fecha_es] += cantidad
                else:
                    ventas_por_usuario[usuario][fecha_es] = cantidad
            else:
                ventas_por_usuario[usuario] = {fecha_es: cantidad}
        
        # Ordenar los usuarios por la cantidad de ventas en orden descendente
        usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: sum(x[1].values()), reverse=True)

        # Renderizar la plantilla 'admin/v_ventas.html' con los datos necesarios
        return render_template('admin/rep_diario.html', usuarios_ordenados=usuarios_ordenados)


#Admin Vista de Reportes semanales
@app.route('/admin/rep_semanal')
def reposemana(): 
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    # Obtener todas las ventas de la colección 'ventas'
    ventas = db.ventas.find()
    
    # Crear un diccionario para almacenar las ventas por usuario
    ventas_por_usuario = {}
    
    # Iterar sobre las ventas y sumar las cantidades por usuario
    for venta in ventas:
        usuario = venta['usuario']
        cantidad = float(venta['cambio'])
        fecha = venta["fecha"]  
        
        # Convertir la fecha a formato español
        fecha = datetime.strptime(fecha, "%Y-%m-%d")
        
        # Calcular el inicio de la semana para la fecha
        inicio_semana = fecha - timedelta(days=fecha.weekday())
        inicio_semana_es = format_date(inicio_semana, 'EEEE d MMMM yyyy', locale='es_ES')
        
        # Verificar si el usuario ya está en el diccionario
        if usuario in ventas_por_usuario:
            # Verificar si la semana ya está en el diccionario del usuario
            if inicio_semana_es in ventas_por_usuario[usuario]:
                ventas_por_usuario[usuario][inicio_semana_es] += cantidad
            else:
                ventas_por_usuario[usuario][inicio_semana_es] = cantidad
        else:
            ventas_por_usuario[usuario] = {inicio_semana_es: cantidad}
    
    # Ordenar los usuarios por la cantidad de ventas en orden descendente
    usuarios_ordenados = sorted(ventas_por_usuario.items(), key=lambda x: sum(x[1].values()), reverse=True)

    # Renderizar la plantilla 'admin/r_semanal.html' con los datos necesarios
    return render_template('admin/rep_semanal.html', usuarios_ordenados=usuarios_ordenados)






#*---------------------- Carpetas Usuarios ----------------------------------

#Ingresado de Clientes los mecanicos
@app.route('/usuarios/clientes' ,methods=['GET','POST'])
def useclient():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method == 'POST':
        clientes= db['clientes']
        nombre= request.form["nombre"]
        cedula= request.form["cedula"]
        direccion=request.form["direccion"]
    
        existing_nombre = clientes.find_one({'nombre':nombre})
        existing_cedula = clientes.find_one({'cedula':cedula})

        if existing_nombre:
            flash("Ya existe un cliente con ese nombre")
            return redirect(url_for('useclient'))
        elif existing_cedula:
            flash("Ya existe un cliente con esa cedula")
            return redirect(url_for('useclient'))
        else:
            regcli= Clientes(nombre,cedula,direccion)
            clientes.insert_one(regcli.ClientDBCollection())
            flash("Guardado a la base datos")
            return redirect(url_for("useclient"))
    else:
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
            return redirect(url_for('vuse_cliente'))
    else:
        return redirect(url_for('usuarios/e_client.html'))    


#Carpetas Usuarios para mostrar los clientes 
@app.route('/usuarios/e_client')
def vuse_cliente():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    cliente = db.clientes.find()
    return render_template('usuarios/e_client.html', clientes=cliente)


# * Ingreso de Usuarios ventas
@app.route('/usuarios/ventas', methods=['GET', 'POST'])
def useventa():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    if request.method == 'POST':
        venta = db['ventas']
        codigo_counter = db['codigo_counter']
        # Obtén el último valor del contador y actualízalo
        counter = codigo_counter.find_one_and_update(
            {'_id': 'ventaID'},
            {'$inc': {'value': 1}},
            return_document=ReturnDocument.AFTER
        )
        id_venta = counter['value']
        usuario = request.form["usuario"]
        cliente = request.form["cliente"]
        cedula = request.form["cedula"]
        categorias = request.form["categoria"]
        precios = request.form["precio"]
        cantidades = request.form["cantidad"]
        cambio = request.form["cambio"]
        fecha = request.form["fecha"]
    
        if id_venta and usuario and cliente and cedula and categorias and precios and cantidades and cambio and fecha:
            regvent = Ventas(id_venta,usuario ,cliente,cedula,categorias, precios,cantidades,cambio,fecha)
            venta.insert_one(regvent.VentaDBCollection())
            flash("Guardado en la base de datos")
            return redirect(url_for('useventa'))
            
    else:
        return render_template('usuarios/ventas.html', usuarios=adsu(), clientes=adcli(),categorias=adcat() , usuario=session['usuario'])   
    

@app.route('/usuarios/v_venta')
def usuv_venta():
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    
    venta =db.ventas.find()
    return render_template('/usuarios/v_venta.html',ventas=venta)


@app.route('/usuarios/comprobante', methods=['GET'])
def usucomprobante():
    id_venta = request.args.get('id_venta')
    venta = None

    if id_venta:
        id_venta = int(id_venta)  # Convierte id_venta a un número
        venta = db.ventas.find_one({'id_venta': id_venta})

    return render_template('usuarios/comprobante.html', venta=venta)

#Carpeta vista de productos
@app.route('/usuarios/e_produc')
def vuse_producto():
    # Verifica si el usuario está en la sesión
    if 'username' not in session:
        flash("Inicia sesion con tu usuario y contraseña")
        return redirect(url_for('index'))
    producto = db.productos.find()
    return render_template('usuarios/e_produc.html', productos=producto)    


if __name__ == '__main__':
    app.run(debug=True, port=4000)
