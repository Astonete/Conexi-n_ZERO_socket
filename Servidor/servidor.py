import socket
# por que el server no tiene usa o no tiene Delay?
from configuracion_conexion_servidor import HOST,PORT
from gestor_clientes import aceptar_clientes
from datetime import datetime

def hora_actual():
    return datetime.now().strftime("fecha %d/%m/%Y hr %H:%M:%S")

def iniciar_servidor():
    # Crea un socket TCP/IP, lo vincula a una dirección y puerto, y escucha conexiones entrantes.
    try:
        # 1. crea un socket usando IPv4 y TCP
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 2. Permite reutilizar la dirección del socket al reiniciar el servidor.
        #    Evita el error "Address already in use"
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 3. Vincula el socket a la IP y puerto concretos para que el servidor pueda escuchar ahí las conexiones que lleguen
        servidor_socket.bind((HOST, PORT))

        # 4. Activa la escucha de conexiones; 5 es el máximo de conexiones en espera.
        servidor_socket.listen()

        # 5. Si no hay nada, no bloquea
        servidor_socket.setblocking(False)

        print(
            f"---Servidor Escuchando (soy todo oídos 👂)---\n"
            f" En IP: {HOST}\n"
            f" Puerto: {PORT}\n"
            f"{hora_actual()}hrs."
        )

        aceptar_clientes(servidor_socket)  # inicia el bucle principal del servidor para aceptar y manejar clientes
    except OSError as e:
        print(f"Error al configurar el servidor: {e} {hora_actual()}hrs.")
        exit(1)  # el servidor no pudo iniciar por un error de sistema, como puerto ocupado o falta de permisos