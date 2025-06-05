
from abc import ABC, abstractmethod

class Cliente(ABC):
    def __init__(self,id,telefono,correo_electronico):
        self.id = id
        self.telefono = telefono
        self.correo_electronico = correo_electronico

    