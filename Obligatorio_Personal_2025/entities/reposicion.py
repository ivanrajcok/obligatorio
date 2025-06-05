
class Reposicion:
    def __init__(self,pieza,cantidad_lotes,fecha,costo):
        self.pieza = pieza
        self.cantidad_lotes = cantidad_lotes
        self.fecha = fecha
        self.__costo = costo

    @property
    def costo(self):
        return self.__costo
    
    @costo.setter
    def costo(self, costo_nuevo):
        self.__costo=costo_nuevo
        