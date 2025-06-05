
class Maquina:
    def __init__(self, codigo, descripcion):
        self.codigo = codigo
        self.descripcion = descripcion
        self.requerimientos = []  
        self.__costo_produccion = 0
        self.__disponibilidad = True

    @property
    def costo_produccion(self):
        return self.__costo_produccion

    @costo_produccion.setter
    def costo_produccion(self, nuevo_costo_produccion):
        self.__costo_produccion = nuevo_costo_produccion

    @property
    def disponibilidad(self):
        return self.__disponibilidad

    @disponibilidad.setter
    def disponibilidad(self, nueva_disponibilidad):
        self.__disponibilidad = nueva_disponibilidad


   
    
    

        