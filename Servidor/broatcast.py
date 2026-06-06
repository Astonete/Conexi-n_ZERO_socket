def broatcast(mensaje, socket_emisor, socket_servidor, sockets):
    # reenvia el mensaje a todos los clientes excepto al emisor y al servidor
    sockets_muertos=[]
    
    for decir in sockets[:]:#que hace esta lista de [:]
        if decir != socket_emisor and decir != socket_servidor:
            try:
                decir.sendall(mensaje)
            except Exception as e:
                print(f"Error al enviar mensaje: {e}")
                sockets_muertos.append(decir)

    for muerto in sockets_muertos:
        if muerto in sockets:
            sockets.remove(muerto)
        try:
            muerto.close()
        except OSError:
            pass
# diferencia entre continue y pass?