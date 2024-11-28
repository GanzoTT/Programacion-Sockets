# Importamos las librerías necesarias para trabajar con conexiones y hilos
import socket
import threading

# Esta función maneja la comunicación con el cliente
def handle_client(client_socket):
    # Usamos un bloque try-except-finally para asegurarnos de que el socket siempre se cierre
    try:
        # Recibimos datos del cliente (hasta 1024 bytes)
        request = client_socket.recv(1024)
        # Mostramos lo que recibimos del cliente
        # Convertimos los datos de bytes a texto para verlos en la consola
        print(f"Datos recibidos: {request.decode()}")
        # Enviamos una respuesta al cliente (un mensaje simple)
        # Notar que usamos 'b' para enviar bytes en lugar de texto
        client_socket.send(b"HTTP/1.1 200 OK\n\n¡Hola, cliente!")
    finally:
        # Independientemente de lo que pase, cerramos la conexión con el cliente
        client_socket.close()

# Creamos un socket que permitirá la comunicación con los clientes
# El socket usará direcciones IP y el protocolo TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Decimos que el servidor escuchará en todas las direcciones y en el puerto 8080
server.bind(("0.0.0.0", 8080))
# El servidor puede aceptar hasta 5 conexiones al mismo tiempo antes de rechazar nuevas
server.listen(5)
# Informamos que el servidor está listo y esperando conexiones
print("Servidor escuchando en puerto 8080...")

# Bucle infinito para que el servidor esté siempre escuchando y aceptando conexiones
while True:
    # Esperamos una conexión y, cuando se establece, obtenemos el socket del cliente
    client_socket, addr = server.accept()
    # Mostramos la dirección del cliente que se conecta
    print(f"Cliente conectado desde {addr}")
    # Creamos un nuevo hilo para manejar la comunicación con este cliente sin bloquear el servidor
    # Le pasamos el socket del cliente para que pueda comunicarse con él
    client_handler = threading.Thread(target=handle_client, args=(client_socket,))
    # Iniciamos el hilo para que se ejecute en paralelo con el resto del código
    client_handler.start()
