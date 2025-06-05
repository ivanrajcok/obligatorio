from exceptions.datos_invalidos import DatosInvalidos
from exceptions.pieza_ya_existe import PiezaYaExiste
from entities.pieza import Pieza

from entities.maquina import Maquina
from entities.requerimiento import Requerimiento
from exceptions.maquina_ya_existe import MaquinaYaExiste

from entities.cliente_particular import Cliente_particular
from entities.empresa import Empresa
from exceptions.cliente_ya_existe import ClienteYaExiste

from entities.pedido import Pedido
from datetime import datetime
from exceptions.stock_insuficiente import StockInsuficiente

from entities.reposicion import Reposicion

import math




class Sistema:
    def __init__(self):
        self.maquinas = []
        self.clientes = []
        self.pedidos = []
        self.piezas = []

        self.contador_codigo_pieza= 1
        self.contador_codigo_maquina = 1
        self.contador_id_cliente= 1
        self.contador_pedidos= 1

    


    def registrar_pieza(self, descripcion, costo_unitario, lote_reposicion, cantidad_disponible=0):
        
        if not descripcion or costo_unitario < 0 or lote_reposicion <= 0 or cantidad_disponible< 0:
            raise DatosInvalidos("Los datos ingresados son inválidos.")

        
        for pieza in self.piezas:
            if pieza.descripcion == descripcion:
                raise PiezaYaExiste("Ya existe una pieza con esa descripción.")

        
        nueva_pieza = Pieza(
            codigo = self.contador_codigo_pieza,
            descripcion = descripcion,
            costo = costo_unitario,
            lote = lote_reposicion,
            cantidad = cantidad_disponible,
            reposiciones = []
        )
        self.piezas.append(nueva_pieza)
        self.contador_codigo_pieza += 1
        return nueva_pieza
    


   

    def registrar_maquina(self, descripcion, requerimientos_data):
        if not descripcion:
            raise DatosInvalidos("La descripción no puede estar vacía.")

        for maquina in self.maquinas:
            if maquina.descripcion == descripcion:
                raise MaquinaYaExiste("Ya existe una máquina con esa descripción.")

        nueva_maquina = Maquina(
            codigo = self.contador_codigo_maquina,
            descripcion = descripcion
        )

        costo_total = 0
        piezas_agregadas = set()

        for pieza, cantidad in requerimientos_data:
            if pieza in piezas_agregadas:
                raise DatosInvalidos(f"La pieza {pieza.descripcion} ya fue agregada.")
            piezas_agregadas.add(pieza)

            if cantidad <= 0:
                raise DatosInvalidos("La cantidad debe ser mayor a cero.")

            nuevo_requerimiento = Requerimiento(nueva_maquina, pieza, cantidad)
            nueva_maquina.requerimientos.append(nuevo_requerimiento)

            costo_total += pieza.costo * cantidad

        nueva_maquina.costo_produccion = costo_total
        self.maquinas.append(nueva_maquina)
        self.contador_codigo_maquina += 1
        return nueva_maquina





    def registrar_cliente(self, tipo, datos):
        
        
        
        if tipo not in ['particular', 'empresa']:
            raise DatosInvalidos("Tipo de cliente inválido.")

        if tipo == 'particular':
            cedula = datos.get("cedula")
            nombre_completo = datos.get("nombre_completo")
            telefono = datos.get("telefono")
            correo = datos.get("correo")

            if not (cedula and nombre_completo and telefono and correo):
                raise DatosInvalidos("Faltan datos del cliente particular.")

            for cliente in self.clientes:
                if isinstance(cliente, Cliente_particular) and cliente.cedula == cedula:
                    raise ClienteYaExiste("Ya existe un cliente con esa cédula.")

            nuevo_cliente = Cliente_particular(
                id = self.contador_id_cliente,
                telefono = telefono,
                correo_electronico = correo,
                cedula = cedula,
                nombre_completo = nombre_completo
            )

        else:  
            rut = datos.get("rut")
            nombre = datos.get("nombre")
            pagina_web = datos.get("pagina_web")
            telefono = datos.get("telefono")
            correo = datos.get("correo")

            if not (rut and nombre and pagina_web and telefono and correo):
                raise DatosInvalidos("Faltan datos de la empresa.")

            for cliente in self.clientes:
                if isinstance(cliente, Empresa) and cliente.rut == rut:
                    raise ClienteYaExiste("Ya existe una empresa con ese RUT.")

            nuevo_cliente = Empresa(
                id = self.contador_id_cliente,
                telefono = telefono,
                correo_electronico = correo,
                rut = rut,
                nombre = nombre,
                pagina_web = pagina_web
            )

        self.clientes.append(nuevo_cliente)
        self.contador_id_cliente += 1
        return nuevo_cliente





    def registrar_pedido(self, cliente, maquina):
        if not cliente or not maquina:
            raise DatosInvalidos("Cliente o máquina no válidos.")

        fecha_actual = datetime.now()

        
        puede_entregar = True
        for req in maquina.requerimientos:
            if req.pieza.cantidad < req.cantidad:
                puede_entregar = False
                break

        if puede_entregar:
            
            for req in maquina.requerimientos:
                req.pieza.cantidad -= req.cantidad
            estado = "entregado"
            fecha_entrega = fecha_actual
        else:
            estado = "pendiente"
            fecha_entrega = None 

        
        precio_base = maquina.costo_produccion * 1.5
        if hasattr(cliente, 'rut'):  
            precio_base *= 0.8  

        nuevo_pedido = Pedido(
            cliente = cliente,
            maquina = maquina,
            fecha_recibido = fecha_actual,
            fecha_entregado = fecha_entrega,
            estado = estado,
            precio = precio_base
        )

        self.pedidos.append(nuevo_pedido)
        return nuevo_pedido
    


    def completar_pedidos_pendientes(self):
            from datetime import datetime
            for pedido in self.pedidos:
                if pedido.estado == "pendiente":
                    maquina = pedido.maquina
                    puede_entregar = True

                    for req in maquina.requerimientos:
                        if req.pieza.cantidad < req.cantidad:
                            puede_entregar = False
                            break

                    if puede_entregar:
                        for req in maquina.requerimientos:
                            req.pieza.cantidad -= req.cantidad

                        pedido.estado = "entregado"
                        pedido.fecha_entregado = datetime.now()





    def registrar_reposicion(self, pieza, cantidad_lotes):
        if not pieza or cantidad_lotes <= 0:
            raise DatosInvalidos("Datos inválidos para la reposición.")

        fecha_actual = datetime.now()
        unidades_agregadas = cantidad_lotes * pieza.lote
        pieza.cantidad += unidades_agregadas

        costo_total = cantidad_lotes * pieza.costo
        nueva_reposicion = Reposicion(
            pieza = pieza,
            cantidad_lotes = cantidad_lotes,
            fecha = fecha_actual,
            costo = costo_total
        )

        pieza.reposiciones.append(nueva_reposicion)

        
        self.completar_pedidos_pendientes()

        return nueva_reposicion






    def listar_clientes(self):
        clientes_info = []

        for cliente in self.clientes:
            if hasattr(cliente, 'cedula'):  
                info = {
                    "id": cliente.id,
                    "tipo": "Particular",
                    "cedula": cliente.cedula,
                    "nombre_completo": cliente.nombre_completo,
                    "telefono": cliente.telefono,
                    "correo": cliente.correo_electronico
                }
            elif hasattr(cliente, 'rut'):  
                info = {
                    "id": cliente.id,
                    "tipo": "Empresa",
                    "rut": cliente.rut,
                    "nombre": cliente.nombre,
                    "pagina_web": cliente.pagina_web,
                    "telefono": cliente.telefono,
                    "correo": cliente.correo_electronico
                }
            clientes_info.append(info)

        return clientes_info







    def listar_pedidos(self, estado=None):
      
        pedidos_info = []

        for pedido in self.pedidos:
            if estado and pedido.estado != estado:
                continue

            info = {
                "cliente_id": pedido.cliente.id,
                "cliente_tipo": "Empresa" if hasattr(pedido.cliente, "rut") else "Particular",
                "maquina_codigo": pedido.maquina.codigo,
                "fecha_recibido": pedido.fecha_recibido.strftime("%Y-%m-%d %H:%M"),
                "fecha_entregado": pedido.fecha_entregado.strftime("%Y-%m-%d %H:%M") if pedido.fecha_entregado else "Pendiente",
                "estado": pedido.estado,
                "precio": round(pedido.precio, 2)
            }
            pedidos_info.append(info)

        return pedidos_info
    


    


    def listar_piezas(self):
        piezas_info = []

        
        demanda = {}  

        for pedido in self.pedidos:
            if pedido.estado == "pendiente":
                for req in pedido.maquina.requerimientos:
                    cantidad_faltante = max(0, req.cantidad - req.pieza.cantidad)
                    if cantidad_faltante > 0:
                        if req.pieza not in demanda:
                            demanda[req.pieza] = 0
                        demanda[req.pieza] += cantidad_faltante

        for pieza in self.piezas:
            faltante = demanda.get(pieza, 0)
            sugerencia_lotes = math.ceil(faltante / pieza.lote) if faltante > 0 else 0

            info = {
                "codigo": pieza.codigo,
                "descripcion": pieza.descripcion,
                "cantidad_disponible": pieza.cantidad,
                "lote": pieza.lote,
                "faltante": faltante,
                "lotes_sugeridos": sugerencia_lotes
            }
            piezas_info.append(info)

        return piezas_info







    def listar_maquinas(self):
        maquinas_info = []

        for maquina in self.maquinas:
            disponible = True
            for req in maquina.requerimientos:
                if req.pieza.cantidad < req.cantidad:
                    disponible = False
                    break

            precio_venta = round(maquina.costo_produccion * 1.5, 2)

            info = {
                "codigo": maquina.codigo,
                "descripcion": maquina.descripcion,
                "costo_produccion": round(maquina.costo_produccion, 2),
                "precio_venta": precio_venta,
                "disponible": "Sí" if disponible else "No"
            }
            maquinas_info.append(info)

        return maquinas_info







    def listar_contabilidad(self):
        costo_total = 0
        ingreso_total = 0

        for pedido in self.pedidos:
            if pedido.estado == "entregado":
                costo_total += pedido.maquina.costo_produccion
                ingreso_total += pedido.precio

        ganancia_bruta = ingreso_total - costo_total
        impuesto = ganancia_bruta * 0.25
        ganancia_neta = ganancia_bruta - impuesto

        return {
            "costo_total": round(costo_total, 2),
            "ingreso_total": round(ingreso_total, 2),
            "ganancia_bruta": round(ganancia_bruta, 2),
            "impuesto": round(impuesto, 2),
            "ganancia_neta": round(ganancia_neta, 2)
        }

