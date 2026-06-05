# cliente.py
# orquesta el inicio del Cliente: Hilo receptor + bucle emisor

import threading
from enchufar_desenchufar import cliente_conectado
from recibir import recibir_mensaje
from enviar import enviar_mensaje

def iniciar_cliente():
    nombre=input("¿Como Te Llamas?: ")

    # Estado compartido entre hilos(evita variables globales)
    estado={
        "socket": None,
        "desenchufado": False,
    }

    # conexion inicial
    if not cliente_conectado(estado):
        print("Cliente finalizado: no se pudo conectar al servidor.")
        return
    
    # Hilo receptor(daemon para que se cierre el hilo principal termina)
    hilo_receptor=threading.Thread(target=recibir_mensaje, args=(estado,), daemon=True)#"Recibir mensajes en un hilo separado para no bloquear el hilo principal."
    hilo_receptor.start()

    # Bucle emisor en el hilo principal (para que el usuario pueda escribir mensajes)
    enviar_mensaje(estado,nombre)

    #espera a que el hilo receptor termine limpiamente antes de salir del programa
    hilo_receptor.join(timeout=3)
