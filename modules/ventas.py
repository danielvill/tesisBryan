class Ventas:
    def __init__(self, usuario,cliente,marca,categoria,precio,cambio,fecha):
        self.usuario=usuario
        self.cliente=cliente
        self.marca=marca
        self.categoria=categoria
        self.precio = precio
        self.cambio =cambio
        self.fecha=fecha

    def VentaDBCollection(self):
        return{
            'usuario':self.usuario,
            'cliente':self.cliente,
            'marca':self.marca,
            'categoria':self.categoria,
            'precio':self.precio,
            'cambio':self.cambio,
            'fecha':self.fecha

        }