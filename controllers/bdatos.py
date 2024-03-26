from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27017'

def Conexion():
    try:
        client = MongoClient(MONGO_URI)
        db = client["mecanica"]
        # Verifica si el contador para producto_id ya existe
        if db['codigo_counter'].find_one({'_id': 'producto_id'}) is None:
            # Si no existe, inicializa el contador
            db['codigo_counter'].insert_one({'_id': 'producto_id', 'value': 0})
        # Verifica si el contador para id_venta ya existe
        if db['codigo_counter'].find_one({'_id': 'ventaID'}) is None:
            # Si no existe, inicializa el contador
            db['codigo_counter'].insert_one({'_id': 'ventaID', 'value': 0})
            
        print("Conexión a MongoDB exitosa.")
    except ConnectionError:
        print('Error de conexión con la bdd')
    return db