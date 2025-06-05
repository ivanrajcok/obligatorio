from entities.sistema import Sistema
from exceptions.datos_invalidos import DatosInvalidos
from exceptions.pieza_ya_existe import PiezaYaExiste
from exceptions.cliente_ya_existe import ClienteYaExiste
from exceptions.maquina_ya_existe import MaquinaYaExiste


def pedir_numero(mensaje, tipo=int):
    while True:
        try:
            return tipo(input(mensaje))
        except ValueError:
            print("Dato inválido. Intente nuevamente.")

def menu_principal():
    sistema = Sistema()
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrar")
        print("2. Listar")
        print("3. Salir")
        op = input("Seleccione opción: ")

        if op == "1":
            menu_registrar(sistema)
        elif op == "2":
            menu_listar(sistema)
        elif op == "3":
            break
        else:
            print("Opción inválida.")

def menu_registrar(sistema):
    while True:
        print("\n--- REGISTRAR ---")
        print("1. Pieza")
        print("2. Máquina")
        print("3. Cliente")
        print("4. Pedido")
        print("5. Reposición")
        print("6. Volver")
        op = input("Opción: ")

        try:
            if op == "1":
                descripcion = input("Descripción: ")
                costo = pedir_numero("Costo unitario: ", float)
                lote = pedir_numero("Tamaño del lote: ")
                cantidad = pedir_numero("Cantidad disponible (0 por defecto): ")
                pieza = sistema.registrar_pieza(descripcion, costo, lote, cantidad)
                print("Pieza registrada:", pieza.descripcion)

            elif op == "2":
                descripcion = input("Descripción de la máquina: ")
                requerimientos = []
                ya_usadas = set()
                while True:
                    continuar = input("¿Agregar requerimiento? (s/n): ").lower()
                    if continuar != 's': break

                    for p in sistema.piezas:
                        if p.codigo not in ya_usadas:
                            print(f"{p.codigo} - {p.descripcion}")
                    cod = pedir_numero("Código de la pieza: ")
                    cantidad = pedir_numero("Cantidad necesaria: ")
                    pieza = next(p for p in sistema.piezas if p.codigo == cod)
                    ya_usadas.add(cod)
                    requerimientos.append((pieza, cantidad))
                maquina = sistema.registrar_maquina(descripcion, requerimientos)
                print(f"Máquina registrada: {maquina.descripcion}, Costo: ${maquina.costo_produccion}")

            elif op == "3":
                tipo = input("Tipo (1 = Particular, 2 = Empresa): ")
                datos = {}
                if tipo == "1":
                    datos["cedula"] = input("Cédula: ")
                    datos["nombre_completo"] = input("Nombre completo: ")
                elif tipo == "2":
                    datos["rut"] = input("RUT: ")
                    datos["nombre"] = input("Nombre: ")
                    datos["pagina_web"] = input("Página web: ")
                else:
                    print("Tipo inválido.")
                    continue
                datos["telefono"] = input("Teléfono: ")
                datos["correo"] = input("Correo electrónico: ")
                cliente = sistema.registrar_cliente("particular" if tipo == "1" else "empresa", datos)
                print("Cliente registrado con ID:", cliente.id)

            elif op == "4":
                print("Clientes disponibles:")
                for i, c in enumerate(sistema.clientes):
                    tipo = "Empresa" if hasattr(c, "rut") else "Particular"
                    print(f"{i}. {tipo} - ID: {c.id}")
                idx = pedir_numero("Seleccione cliente: ")
                cliente = sistema.clientes[idx]

                print("Máquinas disponibles:")
                for i, m in enumerate(sistema.maquinas):
                    print(f"{i}. {m.descripcion}")
                idx2 = pedir_numero("Seleccione máquina: ")
                maquina = sistema.maquinas[idx2]

                pedido = sistema.registrar_pedido(cliente, maquina)
                print("Pedido registrado. Estado:", pedido.estado)

            elif op == "5":
                for p in sistema.piezas:
                    print(f"{p.codigo} - {p.descripcion} (lote: {p.lote})")
                cod = pedir_numero("Código de la pieza: ")
                pieza = next(p for p in sistema.piezas if p.codigo == cod)
                lotes = pedir_numero("Cantidad de lotes: ")
                reposicion = sistema.registrar_reposicion(pieza, lotes)
                print("Reposición registrada. Stock actualizado:", pieza.cantidad)

            elif op == "6":
                break
            else:
                print("Opción inválida.")

        except DatosInvalidos as e:
            print("Datos inválidos:", e)
        except PiezaYaExiste as e:
            print("Error: Pieza ya existente:", e)
        except ClienteYaExiste as e:
            print("Error: Cliente ya existente:", e)
        except MaquinaYaExiste as e:
            print("Error: Máquina ya existente:", e)
        except Exception as e:
            print("Error inesperado:", e)

def menu_listar(sistema):
    while True:
        print("\n--- LISTAR ---")
        print("1. Clientes")
        print("2. Pedidos")
        print("3. Máquinas")
        print("4. Piezas")
        print("5. Contabilidad")
        print("6. Volver")
        op = input("Opción: ")

        if op == "1":
            for c in sistema.listar_clientes():
                print(c)
        elif op == "2":
            filtro = input("¿Filtrar por estado? (s/n): ").lower()
            estado = None
            if filtro == "s":
                est = input("1 = Pendientes, 2 = Entregados: ")
                estado = "pendiente" if est == "1" else "entregado"
            for p in sistema.listar_pedidos(estado):
                print(p)
        elif op == "3":
            for m in sistema.listar_maquinas():
                print(m)
        elif op == "4":
            for p in sistema.listar_piezas():
                print(p)
        elif op == "5":
            cont = sistema.listar_contabilidad()
            for k, v in cont.items():
                print(f"{k}: {v}")
        elif op == "6":
            break
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu_principal()
