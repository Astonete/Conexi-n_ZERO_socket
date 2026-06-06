import select

from broatcast import broatcast
from configuracion_conexion_servidor import BUFFER, HOST, PORT

def nombre_socket(socket_cliente):
    try:
        ip, puerto=socket_cliente.getpeername()
        return f"{ip}:{puerto}"
    except OSError:
        return "-> Cliente Desconectado hasta la Proxima"

def desenchufar_cliente(socket_cliente, sockets):
    # Elimina al cliente de la lista y cierra su socket.
    if socket_cliente in sockets:
        sockets.remove(socket_cliente)

    try:
        socket_cliente.close()
    except OSError as error:
        print(f"Error al cerrar el socket del cliente: {error}")


def aceptar_nuevo_cliente(servidor_socket, sockets):
    # Acepta una nueva conexion entrante y la agrega a la lista de sockets.
    try:
        socket_cliente, direccion_cliente = servidor_socket.accept()
        socket_cliente.setblocking(False)
        sockets.append(socket_cliente)
        print(
            f"Nuevo cliente conectado desde {direccion_cliente}\n"
            f"nueva conexion: {direccion_cliente[0]}:{direccion_cliente[1]}"
        )
    except OSError as error:
        print(f"Error al aceptar conexion: {error}")


def manejar_cliente(socket_cliente, socket_servidor, sockets):
    # Maneja el mensaje del cliente, lo reenvia a otros y desconecta si no hay mensaje.
    nombre_cliente=nombre_socket(socket_cliente)
    try:
        mensaje = socket_cliente.recv(BUFFER)
        if not mensaje:
            print(f"Cliente {nombre_cliente} se ha desconectado.")
            desenchufar_cliente(socket_cliente, sockets)
            return

        try:
            print(f"Dice: {mensaje.decode('utf-8').strip()}")
        except UnicodeDecodeError:
            print(f"{nombre_cliente} no se pudo decodificar el mensaje.")

        broatcast(mensaje, socket_cliente, socket_servidor, sockets)
    except OSError as error:
        print(f"Error al manejar cliente {nombre_cliente}: {error}")
        desenchufar_cliente(socket_cliente, sockets)


def aceptar_clientes(socket_servidor):
    # Bucle principal del servidor usando select para manejar multiples clientes.
    sockets = [socket_servidor]
    print(f"Servidor listo en IP= {HOST} \n Puerto numero= {PORT}")

    try:
        while True:
            socket_listo, _, _ = select.select(sockets, [], [])
            for socket_actual in socket_listo:
                if socket_actual == socket_servidor:
                    aceptar_nuevo_cliente(socket_servidor, sockets)
                    print(f"conectados: {len(sockets) - 1}")
                else:
                    manejar_cliente(socket_actual, socket_servidor, sockets)
                    print(f"conectados: {len(sockets) - 1}")

    except KeyboardInterrupt:
        print("\nServidor cerrado de forma manual.")

    except OSError as error:
        print(f"Error en el bucle principal del servidor: {error}")

    finally:
        for sock in sockets[:]:
            try:
                sock.close()
            except OSError:
                pass
        sockets.clear()