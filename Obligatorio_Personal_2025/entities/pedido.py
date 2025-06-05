

class Pedido:
    def __init__(self,cliente,maquina,fecha_recibido,fecha_entregado,estado,precio):
        self.cliente = cliente
        self.maquina = maquina
        self.fecha_recibido = fecha_recibido
        self.fecha_entregado = fecha_entregado
        self.estado = estado
        self.__precio = precio

        

    
    @property
    def precio(self):
        return self.__precio
    
    @precio.setter
    def precio(self,nuevo_precio):
        self.__precio=nuevo_precio