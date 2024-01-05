class Productos:
    def __init__(self, codigo,marca,categoria,cantidad,precio):
        self.codigo=codigo
        self.marca=marca
        self.categoria=categoria
        self.cantidad=cantidad
        self.precio=precio

    def ProduDBCollection(self):
        return{
            "codigo":self.codigo,
            'marca':self.marca,
            'categoria':self.categoria,
            'cantidad':self.cantidad,
            'precio':self.precio

        }