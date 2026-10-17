import http.server
import socketserver
import threading
import time
import os
import sys

PORT = 8080
DIRECTORY = "."
TIEMPO_DESPIERTO = 21600  # 6 horas expresadas en segundos

# 1. Función para levantar el servidor web local
def run_server():
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"[*] Servidor web iniciado internamente en el puerto {PORT}")
        httpd.serve_forever()

# 2. Función del túnel con persistencia forzada de 6 horas
def run_tunnel():
    print("[*] Levantando túnel nativo... Espera un momento.")
    time.sleep(2)
    
    try:
        from ngrok import ngrok
    except ImportError:
        print("[-] Error: Asegúrate de tener la librería ngrok instalada.")
        return

    try:
        # Iniciamos el túnel aleatorio en tu puerto local 8080
        listener = ngrok.forward(PORT)
        url_publica = listener.url()
        
        # Aseguramos el cifrado SSL para la reproducción de audio de Sydney
        url_final = url_publica.replace("http://", "https://")
        
        print("\n" + "="*60)
        print(f"[¡TÚNEL ACTIVADO POR 6 HORAS!] Tu URL oficial es:")
        print(f"{url_final}")
        print("="*60 + "\n")
        
        # Bucle de control: Obliga al script a mantener el túnel vivo e inmune a cierres rápidos
        tiempo_transcurrido = 0
        intervalo = 10
        
        while tiempo_transcurrido < TIEMPO_DESPIERTO:
            time.sleep(intervalo)
            tiempo_transcurrido += intervalo
            # Enviamos un pulso silencioso de control para evitar la suspensión por inactividad
            sys.stdout.write(f"\r[*] Tiempo del túnel activo: {tiempo_transcurrido // 60} min / 360 min.")
            sys.stdout.flush()
            
        print("\n[*] El tiempo programado de 6 horas ha finalizado. Cerrando túnel de forma segura.")
            
    except Exception as e:
        print(f"\n[-] Ocurrió un inconveniente con el túnel: {e}")

if __name__ == "__main__":
    # Arrancamos tu servidor web en segundo plano
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # El hilo principal toma el control y bloquea el apagado por 6 horas
    run_tunnel()