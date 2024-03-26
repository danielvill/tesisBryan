class Productos:
    def __init__(self, codigo,categoria,precio):
        self.codigo=codigo
        self.categoria=categoria
        self.precio=precio

    def ProduDBCollection(self):
        return{
            "codigo":self.codigo,
            'categoria':self.categoria,
            'precio':self.precio
        }