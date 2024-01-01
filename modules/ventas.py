class Ventas:
    def __init__(self, usuario,cliente,marca,categoria,precio,cambio):
        self.cliente=cliente
        self.usuario=usuario
        self.marca=marca
        self.categoria=categoria
        self.precio = precio
        self.cambio =cambio

    def VentaDBCollection(self):
        return{
            'marca':self.marca,
            'categoria':self.categoria,
            'usuario':self.usuario,
            'cambio':self.cambio,
            'cliente':self.cliente,
            'precio':self.precio

        }