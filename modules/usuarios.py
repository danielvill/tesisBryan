class Usuario:
    def __init__(self, cedula, usuario,rol,correo,contraseña):
        self.cedula = cedula
        self.usuario = usuario
        self.rol = rol
        self.correo = correo        
        self.contraseña = contraseña

    def UserDBCollection(self):
        return{
            'cedula':self.cedula,
            'usuario': self.usuario,
            'rol':self.rol,
            'correo': self.correo,
            'contraseña':self.contraseña,    
        }