# Recibe mensajes entrantes del servidor y los muestra con reconexion automatica.

import time

from configuracion_conexion import BUFFER, DELAY
from enchufar_desenchufar import cliente_conectado


def cerrar_socket_actual(estado):
    if estado["socket"]:
        try:
            estado["socket"].close()
        except OSError:
            pass
        finally:
            estado["socket"] = None


def recibir_mensaje(estado):
    # Escucha mensajes del servidor en bucle.
    while not estado["desenchufado"]:
        if estado["socket"] is None:
            print(f"Sin conexion activa. Intentando reconectar en {DELAY} segundos...")
            time.sleep(DELAY)
            cliente_conectado(estado)
            continue

        try:
            mensaje = estado["socket"].recv(BUFFER)
            if not mensaje:
                raise ConnectionError("El servidor cerro la conexion")

            usuario_decir = mensaje.decode("utf-8")
            print(f"\nNuevo mensaje: {usuario_decir}\n")
        except ConnectionError as error:
            print(f"{error}. Intentando reconectar en {DELAY} segundos...")
            cerrar_socket_actual(estado)
            time.sleep(DELAY)
        except OSError as error:
            print(f"Error del sistema al recibir el mensaje: {error}")
            cerrar_socket_actual(estado)
            time.sleep(DELAY)
        except Exception as error:
            print(f"Error al recibir el mensaje: {error}")
            cerrar_socket_actual(estado)
            time.sleep(DELAY)

    print("Hilo de recepcion finalizado.")
