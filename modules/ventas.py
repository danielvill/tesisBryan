class Ventas:
    def __init__(self, id_venta,usuario,cliente,cedula,categoria,precio,cantidad ,cambio,fecha):
        self.id_venta=id_venta
        self.usuario=usuario
        self.cliente=cliente
        self.cedula=cedula
        self.categoria=categoria
        self.precio = precio
        self.cantidad=cantidad
        self.cambio =cambio
        self.fecha=fecha

    def VentaDBCollection(self):
        return{
            'id_venta':self.id_venta,
            'usuario':self.usuario,
            'cliente':self.cliente,
            'cedula':self.cedula,
            'categoria':self.categoria,
            'precio':self.precio,
            'cantidad':self.cantidad,
            'cambio':self.cambio,
            'fecha':self.fecha

        }