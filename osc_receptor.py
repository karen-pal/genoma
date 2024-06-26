from pythonosc import dispatcher
from pythonosc import osc_server

# Función de manejador para los mensajes recibidos
def message_handler(address, *args):
    print(f"Received OSC message at {address}: {args}")

# Configurar el dispatcher
disp = dispatcher.Dispatcher()
disp.map("/estado", message_handler)  # Mapea la dirección OSC /estado a la función message_handler

# Configurar el servidor OSC
ip = "127.0.0.1"  # La IP del servidor OSC (asegúrate de que sea la misma IP que el cliente)
port = 8000       # El puerto en el que el servidor escuchará (asegúrate de que sea el mismo puerto que el cliente)

server = osc_server.ThreadingOSCUDPServer((ip, port), disp)
print(f"Serving on {server.server_address}")

# Ejecutar el servidor OSC
server.serve_forever()

