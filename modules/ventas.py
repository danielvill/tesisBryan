class Ventas:
    def __init__(self, usuario,cliente,marca,categoria,precio,cambio):
        self.usuario=usuario
        self.cliente=cliente
        self.marca=marca
        self.categoria=categoria
        self.precio = precio
        self.cambio =cambio

    def VentaDBCollection(self):
        return{
            'usuario':self.usuario,
            'cliente':self.cliente,
            'marca':self.marca,
            'categoria':self.categoria,
            'precio':self.precio,
            'cambio':self.cambio

        }