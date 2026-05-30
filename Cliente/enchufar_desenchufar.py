import socket, time
from configuracion_conexion import HOST,PORT,DELAY

def cliente_conectado(estado):
    # intenta conectarse con el servidor vuelve a intentar si algo falla
    reintentos =0
    while estado["socket"] is None and not estado["desenchufado"] and reintentos < 3:
        try:
            print("📡 Uniéndo al servidor...")
            cliente_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)#“Crea un socket usando IPv4 y comunicación TCP”.
            cliente_socket.connect((HOST,PORT))
            print(f"Bienvenido al Servidor \n ->🟢 IP: {HOST} \n ->🟢 PUERTO: {PORT}")
        except ConnectionError:
            reintentos += 1
            print(f"🚩 (comprueba la conexión/red)\n Este es el intento numero: {reintentos} para unirte\n 🕖 Espera {DELAY} segundos para volver a conectar")
            print(f"🧑‍💻 Si el Problema Persiste consulte a Soporte Tecnico")
            
            time.sleep(DELAY)
        except OSError:
            if not estado["desenchufado"]:
                reintentos += 1
                print(f"🚩 (Error de sistema).\n Este es el intento numero: {reintentos}\n Reconectando en 🕖 {DELAY} segundos...")
                print(f"🧑‍💻 Si el Problema Persiste consulte a Soporte Tecnico")
                time.sleep(DELAY)
        except:
            print(f"🧑‍💻 Consulte a Soporte Tecnico")
            raise SystemExit("❌ No se pudo conectar al servidor.")

def cliente_desconectado(estado):
# cierra el socket y cambia su estado en None
    if estado["socket"]:
        try:
            print("🔌 Desconectando del servidor...")
            estado["socket"].close()
        except:
            print("⚠️ Error al cerrar el socket. Puede que ya esté cerrado.")
            pass
            estado["socket"]=None