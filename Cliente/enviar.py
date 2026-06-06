# Se encarga de enviar mensajes al servidor.

from enchufar_desenchufar import cliente_conectado, cliente_desconectado
from recibir import cerrar_socket_actual


def enviar_mensaje(estado, nombre):
    # Lee los mensajes del usuario y los envia al servidor.
    while not estado["desenchufado"]:
        try:
            mensaje = input("Escribe tu mensaje (qq para desconectar): ")

            if mensaje.lower() == "qq":
                print("Desconectando...")
                cliente_desconectado(estado)
                break

            if estado["socket"] is None:
                print("Sin conexion activa. Intentando reconectar...")
                cliente_conectado(estado)

            if estado["socket"] is None:
                print("No se pudo enviar porque no hay conexion activa.")
                continue

            usuario_decir = f"☺ {nombre} -> dice: {mensaje}".encode("utf-8")
            estado["socket"].sendall(usuario_decir)
        except OSError as error:
            if not estado["desenchufado"]:
                print(f"Error del sistema al enviar el mensaje: {error}")
            cerrar_socket_actual(estado)
        except KeyboardInterrupt:
            print(f"{nombre} desconecto manualmente.")
            cliente_desconectado(estado)
            break
        except Exception as error:
            print(f"Error al enviar el mensaje: {error}")
            cerrar_socket_actual(estado)
