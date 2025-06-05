
from entities.cliente import Cliente
class Empresa(Cliente):
    
    def __init__(self, id, telefono, correo_electronico,rut,nombre,pagina_web):
        self.rut = rut
        self.nombre = nombre
        self.pagina_web = pagina_web
        super().__init__(id, telefono, correo_electronico)

    