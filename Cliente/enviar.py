# se va a encargar de enviar mensajes
# lee los inputs del usuario "mensajes" y va pal servidor
from enchufar_desenchufar import cliente_conectado, cliente_desconectado

def enviar_mensaje(estado,nombre):
    #Lee los mensajes del usuario y los envia al servidor
    #maneja KeyboardInterruptor para desconectar de forma limpia y segura
    while True:
        try:
            mensaje=input("Escribe tu Mensaje (qqq para desconectar)")
            if mensaje.lower()=="qqq":
                print("🔌 Desconectando...")
                cliente_desconectado(estado)
                break
            if estado ["socket"] is None:
                print ("Sin Conexión Activa")
                continue
            if estado["socket"]:
                usuario_decir=f"-> {nombre}: {mensaje}".encode("utf-8")
                estado ["socket"].senall(usuario_decir)
            else:
                print("No Estás conectado al servidor. verifique la conexion Intenta reconectar...")
                cliente_conectado(estado)
        except OSError:
            if not estado["desenchufado"]:
                print("Error del sistema al enviar el Mensaje")
            cliente_desconectado(estado)
        except KeyboardInterrupt:
            print(f"{nombre} Desconecta manualmente (interrupcíon del teclado)...")
            estado["desenchufado"]=True
            cliente_desconectado(estado)
            break
        except Exception as e:
            print(f"Error al enviar el Mensaje: {e}")
            cliente_desconectado(estado)
            break