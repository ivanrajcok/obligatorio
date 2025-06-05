
from entities.cliente import Cliente
class Cliente_particular(Cliente):
    def __init__(self, id, telefono, correo_electronico,cedula,nombre_completo):
        self.cedula=cedula
        self.nombre_completo=nombre_completo
        super().__init__(id, telefono, correo_electronico)

   