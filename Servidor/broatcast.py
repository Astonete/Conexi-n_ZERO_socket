def broatcast(mensaje, socket_emisor, socket_servidor, sockets):
    # reenvia el mensaje a todos los clientes excepto al emisor y al servidor
    for decir in sockets:
        if decir != socket_emisor and decir != socket_servidor:
            try:
                decir.sendall(mensaje)
            except Exception as e:
                print(f"Error al enviar mensaje a {decir.getpeername()}: {e}")
                pass
# diferencia entre continue y pass?