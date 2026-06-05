import socket
# por que el server no tiene usa o no tiene Delay?
from configuracion_conexion_servidor import HOST,PORT
from gestor_clientes import aceptar_clientes

def iniciar_servidor():
    # crea un socket TCP/IP y lo enlaza a la direccion y puerto especifico y luego empieza a escuchar las conexiones entrantes
    try:
        servidor_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # crea un socket usuando ip4 y tcp
        servidor_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)# permite reutilizar la direccion del socket para evitar el error "Address already in use" al reiniciar el servidor
        servidor_socket.bind((HOST,PORT))# enlaza el socket a la direccion y puerto especifico para que el servidor pueda escuchar las conexiones entrantes en esa direccion y puerto
        servidor_socket.listen()# pone el socket en modo de escucha para aceptar conexiones entrantes, el numero 5 es el tamaño maximo de la cola de conexiones pendientes
        servidor_socket.setblocking(False)# si no hay nada lanza expecion(no bloqueo)
        print(f"---Servidor Escuchando (soy todo oidos 👂)---\n En IP: {HOST}\n Puerto: {PORT}")
        aceptar_clientes(servidor_socket)# inicia el bucle principal del servidor para aceptar y manejar clientes
    except OSError as e:
        print(f"Error al Configurar el servidor: {e}")
        exit(1)# el servidor no pudo iniciar por un error de sistema, como puerto ocupado o falta de permisos