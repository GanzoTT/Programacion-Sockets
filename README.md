# Programacion-Sockets

## Servidor con Hilos (Threads)

### Funcionalidad general:

Este servidor puede aceptar múltiples conexiones simultáneamente gracias a los hilos. Cada cliente conectado recibe una respuesta estándar (HTTP/1.1 200 OK\n\nHola, cliente!). Si un cliente envía datos al servidor, estos se imprimen en la consola del servidor.
    
### Importaciones:

    import socket
    import threading

  - Socket: Proporciona herramientas para la comunicación entre dispositivos en una red, implementando los conceptos básicos de red como direcciones IP, puertos, y protocolos como TCP/IP.
  - Threading: Permite la creación y gestión de hilos, lo que es útil para manejar varias conexiones al mismo tiempo.
  
### Función handle_client:
    
        def handle_client(client_socket):
            try:
                request = client_socket.recv(1024)
                print(f"Recibido: {request.decode()}")
                client_socket.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
            finally:
                client_socket.close()
    
    - Entrada de la función: Toma un objeto client_socket que representa la conexión con un cliente.
    
          1. Request = client_socket.recv(1024): Recibe datos del cliente, leyendo hasta 1024 bytes. Esto puede ser un mensaje HTTP, texto plano, etc.
          2. Print(f"Recibido: {request.decode()}"): Convierte los datos recibidos (en bytes) a una cadena de texto para su impresión.
          3. Client_socket.send(b"HTTP/1.1 200 OK\n\nHola, cliente!"): Responde al cliente con un mensaje en formato HTTP indicando éxito (200 OK) y un saludo.
          4. Client_socket.close(): Libera la conexión con el cliente para ahorrar recursos.
  
### Configuración del servidor:

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("0.0.0.0", 8080))
        server.listen(5)
        print("Servidor escuchando en puerto 8080...")
    
    1. Socket.socket(socket.AF_INET, socket.SOCK_STREAM):
    
           Crea un objeto socket.
           AF_INET: Indica el uso de direcciones IPv4.
           SOCK_STREAM: Especifica que se utilizará el protocolo TCP (orientado a conexión).
    
    2. Server.bind(("0.0.0.0", 8080)):
    
           Asocia el socket al puerto 8080 y permite que escuche conexiones en todas las interfaces de red locales (0.0.0.0).
       
    3. Server.listen(5):
    
           Configura el socket para aceptar conexiones entrantes.
           5 define el tamaño máximo de la cola de conexiones en espera.
    
    4. Print("Servidor escuchando en puerto 8080..."): Muestra un mensaje indicando que el servidor está listo para recibir clientes.

### Bucle principal:

        while True:
            client_socket, addr = server.accept()
            print(f"Conexión desde {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    
    1. Client_socket, addr = server.accept():
    
           Espera una conexión entrante.
           Devuelve el socket para comunicarse con el cliente y la dirección del cliente (addr).
    
    2. Print(f"Conexión desde {addr}"): Muestra la dirección IP y el puerto del cliente que se ha conectado.
       
    3. Threading.Thread(...):
    
            Crea un nuevo hilo para manejar al cliente.
            target=handle_client: Especifica que la función handle_client manejará la conexión.
            args=(client_socket,): Pasa el socket del cliente como argumento.
    
    4. Client_handler.start(): Inicia el hilo para manejar al cliente.

### Definición del proceso que realiza el código

    El código implementa un servidor concurrente basado en hilos que maneja múltiples conexiones de clientes de manera simultánea. Su flujo general es:
    
      1. Inicialización del servidor: Se crea un socket para escuchar en un puerto específico.
      2. Aceptación de conexiones: En un bucle infinito, el servidor espera que los clientes se conecten.
      3. Manejo de clientes en hilos:
    
        - Cada cliente se gestiona en un hilo independiente, lo que permite que varios clientes interactúen con el servidor al mismo tiempo.
        - El servidor recibe datos del cliente, imprime los datos recibidos y envía una respuesta predefinida en formato HTTP.
    
      4. Finalización: El hilo que maneja a un cliente termina su ejecución después de responder, y el servidor queda listo para atender nuevas conexiones.

### Ventajas de este estilo de programación concurrente

    1. Paralelismo y multitarea:
        El uso de hilos permite atender múltiples clientes de forma simultánea, aprovechando los núcleos disponibles del procesador.
        Esto mejora la capacidad del servidor para manejar múltiples usuarios sin retrasos importantes.

    2. Simplicidad del diseño:
        Implementar hilos en Python es relativamente sencillo usando la biblioteca estándar (threading).
        El código es más legible y fácil de seguir que otras técnicas concurrentes más complejas, como manejo manual de selectores.

    3. Desempeño aceptable para tareas ligeras:
        Cada hilo maneja una tarea específica, como recibir y responder datos, lo que facilita el desarrollo para aplicaciones con lógica simple.

### Desventajas de este estilo de programación concurrente

    1. Sobrecarga de hilos:
        Creación de hilos: Cada cliente conectado genera un hilo nuevo, lo que aumenta el consumo de recursos del sistema (memoria y CPU). Si hay miles de clientes, el servidor podría colapsar.
        Límite de hilos: Los sistemas operativos tienen un número máximo de hilos que se pueden ejecutar simultáneamente.

    2. Complejidad de depuración:
        Depurar programas concurrentes puede ser más complicado, ya que los hilos pueden interactuar de formas no esperadas.

    3. Menor escalabilidad en sistemas de alta concurrencia:
        Para sistemas de alto rendimiento, este enfoque no es óptimo. Alternativas como asynchronous I/O (asyncio) o servidores basados en eventos (ej., Node.js) pueden manejar cientos de miles de           conexiones con menor uso de recursos.

