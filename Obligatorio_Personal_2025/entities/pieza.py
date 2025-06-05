
class Pieza:
    def __init__(self,codigo,descripcion,costo,lote,cantidad):
        self.codigo = codigo
        self.descripcion = descripcion
        self.costo = costo
        self.lote = lote
        self.cantidad = cantidad
        self.reposiciones = []