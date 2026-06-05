import select

from broatcast import broatcast
from configuracion_conexion_servidor import BUFFER, HOST, PORT


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
    try:
        mensaje = socket_cliente.recv(BUFFER)
        if not mensaje:
            print(f"Cliente {socket_cliente.getpeername()} se ha desconectado.")
            desenchufar_cliente(socket_cliente, sockets)
            return

        try:
            print(f"Mensaje: {mensaje.decode('utf-8').strip()}")
        except UnicodeDecodeError:
            print(f"{socket_cliente.getpeername()} no se pudo decodificar el mensaje.")

        broatcast(mensaje, socket_cliente, socket_servidor, sockets)
    except OSError as error:
        print(f"Error al manejar cliente {socket_cliente.getpeername()}: {error}")
        desenchufar_cliente(socket_cliente, sockets)


def aceptar_clientes(socket_servidor):
    # Bucle principal del servidor usando select para manejar multiples clientes.
    sockets = [socket_servidor]
    print(f"Servidor listo en IP {HOST} : puerto {PORT}")

    try:
        while True:
            socket_listo, _, _ = select.select(sockets, [], [])
            for socket_actual in socket_listo:
                if socket_actual == socket_servidor:
                    aceptar_nuevo_cliente(socket_servidor, sockets)
                else:
                    manejar_cliente(socket_actual, socket_servidor, sockets)
    except KeyboardInterrupt:
        print("\nServidor cerrado de forma manual.")
    except OSError as error:
        print(f"Error en el bucle principal del servidor: {error}")
