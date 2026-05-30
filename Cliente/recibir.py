# recibe mensajes entrantes del servidor y lo muestra  con reconexion automatica

import time

from configuracion_conexion import DELAY,BUFFER
from enchufar_desenchufar import cliente_conectado, cliente_desconectado

def recibir_mensaje(estado):
    # escucha mensajes del servidor en bucle
    # 'estado' es un diccionario pompartido con las claves: #
    # "socket" activo o None
    # #"desenchufado" True cuando el usuario decide salir
    while estado["desenchufado"]:
        #si no hay socket activo, intenta reconectar
        if estado["socket"] is None:
            print(f"🔌 Sin conexión activa.\n 🕖 Intentando reconectar en {DELAY} segundos...")
            cliente_conectado(estado)
            time.sleep(DELAY)
            continue

        try:
            # recv() devuelve bytes.
            mensaje=estado["socket"].recv(BUFFER)
            # Si recv() devuelve '' significa
            # que el servidor cerró la conexión.
            if not mensaje:
                print("⚠️ EL SERVIDOR HA CERRADO LA CONEXION🔌")
                raise ConnectionError("SERVIDOR CERRO LA CONEXION")
            usuario_decir=mensaje.decode('utf-8')
            print(f"\n📩 Nuevo Mensaje{usuario_decir}\n")
            #NOTA PERSONAL Connection Error debe ir antes de OS error
            # porque ConnectionError hereda de OsError
        except ConnectionError as e:
            print(f"🚩 {e}\n El Servidor ha cerrado la conexión. Intentando reconectar en {DELAY} segundos...")
            time.sleep(DELAY)

        except OSError as e:
            print(f"💥 Error del sistema al recibir el mensaje {e}\n contacte a soporte Tecnico.")     
            cliente_desconectado(estado)
            time.sleep(DELAY)
                
        except Exception as e:
            print(f"Error al recibir el mensaje: {e}")
            cliente_desconectado(estado)
            time.sleep(DELAY)
    print("🛑 Hilo de recepción finalizado.")
    