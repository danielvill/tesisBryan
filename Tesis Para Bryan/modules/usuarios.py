class Usuario:
    def __init__(self, cedula, nombre,rol,correo,contraseña):
        self.correo = correo
        self.cedula = cedula
        self.rol = rol
        self.contraseña = contraseña
        self.nombre = nombre

    def UserDBCollection(self):
        return{
            'correo': self.correo,
            'nombre': self.nombre,
            'rol':self.rol,
            'contraseña':self.contraseña,
            'cedula':self.cedula
            
        }