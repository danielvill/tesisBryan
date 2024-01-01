class Admin:
    def __init__(self, correo, usuario,rol,contraseña):
        self.correo = correo
        self.usuario = usuario
        self.rol = rol
        self.contraseña = contraseña

    def AdminDBCollection(self):
        return{
            'correo': self.correo,
            'usuario': self.usuario,
            'rol':self.rol,
            'contraseña':self.contraseña
            
        }