class Clientes:
    def __init__(self,nombre,cedula,direccion):
        self.nombre = nombre
        self.cedula = cedula
        self.direccion = direccion
        

    def ClientDBCollection(self):
        return{
            'nombre': self.nombre,
            'cedula':self.cedula,
            'direccion':self.direccion,
            
            
        }