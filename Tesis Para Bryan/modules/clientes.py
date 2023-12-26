class Clientes:
    def __init__(self, cedula, nombre,codigo,direccion):
        self.cedula = cedula
        self.codigo = codigo
        self.direccion = direccion
        self.nombre = nombre

    def ClientDBCollection(self):
        return{
            'codigo': self.codigo,
            'nombre': self.nombre,
            'direccion':self.direccion,
            'cedula':self.cedula
            
        }