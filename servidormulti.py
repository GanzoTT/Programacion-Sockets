# Importamos las librerías necesarias para trabajar con sockets y monitorear conexiones
import socket
import select

# Creamos un socket para el servidor
# Este socket se configura para usar direcciones IP (IPv4) y el protocolo TCP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Asociamos el socket a la dirección "0.0.0.0" para aceptar conexiones desde cualquier interfaz y al puerto 8080
server.bind(("0.0.0.0", 8080))
# Habilitamos el servidor para escuchar en el puerto 8080 y limitamos las conexiones pendientes a 5
server.listen(5)
# Creamos una lista para seguir y monitorear las conexiones (incluyendo el socket del servidor)
sockets = [server]

# Bucle infinito para mantener el servidor funcionando
while True:
    # El método `select.select()` se usa para esperar hasta que haya algo que leer en los sockets
    # Esta función se bloquea hasta que al menos uno de los sockets está listo para ser leído
    # `readable` es la lista de sockets que están listos para ser leídos
    readable, _, _ = select.select(sockets, [], [])

    # Iteramos sobre todos los sockets listos para leer
    for s in readable:
        # Si el socket que está listo es el del servidor (indica una nueva conexión de cliente)
        if s is server:
            # Aceptamos la nueva conexión del cliente y obtenemos su socket y dirección
            client_socket, addr = server.accept()
            # Mostramos la dirección del cliente que se ha conectado
            print(f"Conexión desde {addr}")
            # Añadimos el socket del cliente a nuestra lista de sockets para monitorear
            sockets.append(client_socket)
        # Si el socket es uno de los clientes conectados
        else:
            # Recibimos datos del cliente (hasta 1024 bytes)
            data = s.recv(1024)

            # Si hay datos recibidos
            if data:
                # Mostramos los datos recibidos del cliente
                # Convertimos los datos de bytes a texto
                print(f"Recibido: {data.decode()}")
                # Enviamos una respuesta al cliente (mensaje HTTP con saludo)
                # Se envía como bytes, por eso usamos el prefijo 'b'
                s.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
            # Si no se reciben datos (el cliente cerró la conexión)
            else:
                # Informamos que el cliente se desconectó
                print("Cliente desconectado")
                # Removemos el socket del cliente de la lista de sockets a monitorear
                sockets.remove(s)
                # Cerramos la conexión con el cliente
                s.close()
