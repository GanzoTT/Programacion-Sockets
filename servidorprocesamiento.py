# Importamos las librerías necesarias para manejar conexiones de red y procesos
import socket
import multiprocessing

# Definimos la función que maneja cada conexión de cliente
def handle_client(client_socket):
    # Recibimos hasta 1024 bytes de datos del cliente
    request = client_socket.recv(1024)
    # Mostramos los datos que hemos recibido del cliente
    # Como recibimos los datos en formato byte, los convertimos a texto para poder verlos
    print(f"Datos recibidos: {request.decode()}")
    # Enviamos una respuesta al cliente (mensaje HTTP 200 OK)
    # El prefijo `b` indica que estamos enviando bytes, no texto
    client_socket.send(b"HTTP/1.1 200 OK\n\n¡Hola, cliente!")
    # Cerramos la conexión con el cliente (terminamos la comunicación)
    client_socket.close()

# Creamos el socket para el servidor
# El servidor usará el protocolo TCP y direcciones IPv4
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asociamos el socket del servidor a la dirección "0.0.0.0" para aceptar conexiones desde cualquier red y al puerto 8080
server.bind(("0.0.0.0", 8080))
# Habilitamos el servidor para escuchar hasta 5 conexiones a la vez
server.listen(5)
# Imprimimos un mensaje para indicar que el servidor está escuchando
print("Servidor escuchando en puerto 8080...")

# Bucle infinito para que el servidor esté siempre disponible para aceptar nuevas conexiones
while True:
    # Aceptamos una nueva conexión de un cliente
    # El servidor devuelve un nuevo socket para la comunicación con el cliente y la dirección de este
    client_socket, addr = server.accept()
    # Mostramos la dirección desde la que el cliente se está conectando
    print(f"Conexión desde {addr}")
    # Creamos un nuevo proceso para manejar la comunicación con el cliente
    # Le pasamos el socket del cliente a la función `handle_client`
    client_process = multiprocessing.Process(target=handle_client, args=(client_socket,))
    # Iniciamos el proceso, lo que permite que el servidor pueda manejar múltiples clientes simultáneamente
    client_process.start()
