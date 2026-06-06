import socket
import time

from configuracion_conexion import DELAY, HOST, PORT

MAX_REINTENTOS = 3

def cliente_conectado(estado):
    # Intenta conectarse con el servidor y vuelve a intentar si algo falla.
    reintentos = 0

    while (
        estado["socket"] is None
        and not estado["desenchufado"]
        and reintentos < MAX_REINTENTOS
    ):
        cliente_socket = None
        try:
            print("Uniendo al servidor...")
            cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente_socket.connect((HOST, PORT))
            estado["socket"] = cliente_socket
            print(f"Bienvenido al Servidor\n -> IP: {HOST}\n -> PUERTO: {PORT}")
            return True
        except ConnectionError as error:
            if cliente_socket:
                cliente_socket.close()

            reintentos += 1
            print(
                f"ConnectionError (comprueba la conexion/red)\n"
                f"Detalle: {error}\n"
                f"Este es el intento numero: {reintentos} para unirte\n"
                f"Espera {DELAY} segundos para volver a conectar"
            )
            print("Si el problema persiste consulte a soporte tecnico")
            time.sleep(DELAY)
        except OSError:
            if cliente_socket:
                cliente_socket.close()

            if not estado["desenchufado"]:
                reintentos += 1
                print(
                    f"OSError (Error de sistema).\n"
                    f"Este es el intento numero: {reintentos}\n"
                    f"Reconectando en {DELAY} segundos..."
                )
                print("Si el problema persiste consulte a soporte tecnico")
                time.sleep(DELAY)
        except Exception as error:
            if cliente_socket:
                cliente_socket.close()

            print("Exception Consulte a soporte tecnico")
            raise SystemExit("No se pudo conectar al servidor.") from error

    if estado["socket"] is None and not estado["desenchufado"]:
        print("No se pudo conectar al servidor. Reintentos agotados.")
        return False

    return estado["socket"] is not None


def cliente_desconectado(estado):
    # Cierra el socket y marca el cliente como desconectado.
    estado["desenchufado"] = True

    if estado["socket"]:
        try:
            print("Desconectando del servidor...")
            estado["socket"].close()
        except OSError:
            print("Error al cerrar el socket. Puede que ya este cerrado.")
        finally:
            estado["socket"] = None
