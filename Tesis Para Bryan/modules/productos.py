class Productos:
    def __init__(self, marca, nombre,categoria,cantidad,precio):
        self.marca=marca
        self.categoria=categoria
        self.cantidad=cantidad
        self.precio=precio
        self.nombre = nombre

    def ProduDBCollection(self):
        return{
            'marca':self.marca,
            'categoria':self.categoria,
            'cantidad':self.cantidad,
            'nombre':self.nombre,
            'precio':self.precio

        }