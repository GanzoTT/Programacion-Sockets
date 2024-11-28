# Programacion-Sockets

## 1. Servidor con Hilos (Threads)

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

## 2. Servidor con Multiprocesamiento (Multiprocessing)

### Funcionalidad general: 

El servidor actúa como un administrador que:
- Acepta conexiones entrantes de clientes.
- Delega la gestión de cada cliente a procesos independientes, lo que permite que varios clientes se manejen de forma simultánea y eficiente.

Este proceso asegura que el servidor sea capaz de:
- Escuchar nuevas conexiones mientras otros clientes están siendo atendidos.
- Aislar la lógica de cada cliente en un proceso separado, reduciendo el riesgo de interferencia entre clientes.

### Importaciones

    import socket
    import multiprocessing

- Socket: Permite la creación y uso de sockets para la comunicación en red, utilizando el protocolo TCP en este caso.
- Multiprocessing: Proporciona herramientas para crear y manejar procesos independientes. Es una alternativa a los hilos y permite un verdadero paralelismo aprovechando múltiples núcleos de la CPU.

### Función handle_client

    def handle_client(client_socket):
        request = client_socket.recv(1024)
        print(f"Recibido: {request.decode()}")
        client_socket.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
        client_socket.close()
    
      1.  Def handle_client(client_socket)::
            Define la lógica para manejar la conexión con un cliente individual. Recibe como parámetro el socket del cliente.
    
      2.  Request = client_socket.recv(1024):
            Espera datos enviados por el cliente y lee hasta 1024 bytes del mensaje.
    
      3.  Print(f"Recibido: {request.decode()}"):
            Imprime los datos recibidos en la consola, convirtiéndolos de bytes a cadena de texto.
    
      4.  Client_socket.send(b"HTTP/1.1 200 OK\n\nHola, cliente!"):
            Responde al cliente con un mensaje en formato HTTP, indicando éxito (200 OK) y un saludo ("Hola, cliente!").
    
      5.  Client_socket.close():
            Cierra la conexión con el cliente, liberando recursos.

### Configuración del servidor

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    print("Servidor escuchando en puerto 8080...")
    
    1. Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM):
            Crea un socket que usa:
                AF_INET: Dirección IPv4.
                SOCK_STREAM: Protocolo TCP, orientado a conexión.
    
    2. Server.bind(("0.0.0.0", 8080)):
            Asocia el socket al puerto 8080, escuchando conexiones en todas las interfaces de red locales (0.0.0.0).
    
    3. Server.listen(5):
            Configura el socket para aceptar conexiones entrantes, con una cola máxima de 5 conexiones en espera.
    
    4. Print("Servidor escuchando en puerto 8080..."):
            Mensaje informativo indicando que el servidor está listo para recibir clientes.

### Bucle principal

    while True:
        client_socket, addr = server.accept()
        print(f"Conexión desde {addr}")
        client_process = multiprocessing.Process(target=handle_client, args=(client_socket,))
        client_process.start()
    
    1. While True::
        Inicia un bucle infinito que permite al servidor aceptar conexiones continuamente.
    
    2. Client_socket, addr = server.accept():
            Espera hasta que un cliente se conecte al servidor.
            Devuelve:
               - client_socket: El socket que representa la conexión con el cliente.
               - addr: La dirección IP y el puerto del cliente.
    
    3. Print(f"Conexión desde {addr}"):
            Imprime la dirección y el puerto del cliente conectado.
    
    4. Multiprocessing.Process(...):
            Crea un proceso independiente para manejar la conexión con el cliente.
            - target=handle_client: Especifica que la función handle_client manejará la conexión.
            - args=(client_socket,): Pasa el socket del cliente como argumento.
    
    5. Client_process.start():
            Inicia el proceso para que handle_client se ejecute en paralelo con otros procesos y el servidor principal.

### Definición del proceso que realiza el código

    El código implementa un servidor TCP concurrente que utiliza procesos independientes para manejar múltiples conexiones de clientes simultáneamente. A continuación, se describe en detalle el flujo del proceso:
    
    1. Inicialización del servidor:
    Se configura un socket TCP que escucha en el puerto 8080 y espera conexiones entrantes.
    
    2. Aceptación de conexiones:
    El servidor entra en un bucle infinito donde:
        - Espera que un cliente se conecte.
        - Establece una conexión con el cliente mediante accept(), lo que genera un socket específico para esa conexión.
    
    3. Creación de un proceso independiente:
    Cada vez que un cliente se conecta, se crea un nuevo proceso utilizando la biblioteca multiprocessing.
    Este proceso ejecuta la función handle_client, que gestiona la comunicación con ese cliente en particular.
    
    4. Manejo de la comunicación con el cliente:
    El proceso hijo (independiente del servidor principal) realiza las siguientes acciones:
        - Recibe datos enviados por el cliente.
        - Imprime los datos recibidos en la consola del servidor.
        - Envía una respuesta estándar en formato HTTP con el mensaje: "Hola, cliente!".
        - Cierra la conexión con el cliente para liberar recursos.
    
    5. Ciclo continuo:
    Mientras el servidor principal está activo, sigue esperando nuevas conexiones y creando procesos para manejarlas.
    
### Ventajas del manejo con procesos

    1. Paralelismo real:
    Aprovecha completamente los núcleos de CPU, permitiendo manejar muchas conexiones simultáneamente con buen rendimiento.

    2. Mayor aislamiento:
    Cada proceso tiene su propia memoria, lo que reduce el riesgo de errores relacionados con la sincronización o condiciones de carrera.

    3. Escalabilidad:
    Más adecuado que los hilos para sistemas con alta concurrencia y tareas intensivas en CPU.

### Desventajas del manejo con procesos

    1. Mayor consumo de recursos:
    Crear procesos consume más memoria y tiempo de arranque en comparación con los hilos.

    2. Sobrecarga en sistemas grandes:
    Manejar miles de procesos puede saturar el sistema operativo.

    3. Comunicación más compleja:
    Compartir información entre procesos requiere mecanismos adicionales, como colas o pipes, lo que complica el diseño.

## 3. Servidor con Multiplexación de Entrada/Salida (select)

### Funcionalidad general: 

Este código implementa un servidor TCP no bloqueante que utiliza la función select.select() para manejar múltiples conexiones de clientes simultáneamente, dentro de un solo proceso. La principal característica de este enfoque es la multiplexación de entradas/salidas (E/S), lo que permite al servidor monitorear varios sockets (conexiones de clientes y su propio socket de escucha) de manera eficiente sin necesidad de crear hilos o procesos adicionales.

### Importaciones

    import socket
    import select

- Socket: Proporciona las herramientas necesarias para crear sockets y establecer comunicaciones en red.
- Select: Permite supervisar múltiples sockets y determina cuáles están listos para leer, escribir o han encontrado un error, sin necesidad de bloquear el programa.

### Configuración del servidor

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 8080))
    server.listen(5)
    sockets = [server]
    
    1. Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM):
        Crea un socket para la comunicación TCP utilizando direcciones IPv4.
    2. Server.bind(("0.0.0.0", 8080)):
        Asocia el socket al puerto 8080 en todas las interfaces de red locales (0.0.0.0).
    3. Server.listen(5):
        Configura el socket para escuchar conexiones entrantes, permitiendo hasta 5 conexiones en espera.
    4. Sockets = [server]:
        Se inicializa una lista para almacenar los sockets activos. Comienza con el socket del servidor.

### Bucle principal

    while True:
        readable, _, _ = select.select(sockets, [], [])
        for s in readable:
            if s is server:
                client_socket, addr = server.accept()
                print(f"Conexión desde {addr}")
                sockets.append(client_socket)
            else:
                data = s.recv(1024)
                if data:
                    print(f"Recibido: {data.decode()}")
                    s.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
                else:
                    print("Cliente desconectado")
                    sockets.remove(s)
                    s.close()
    
    1. While True::
        Inicia un bucle infinito que mantiene el servidor ejecutándose y gestionando conexiones.
    
    2. Readable, _, _ = select.select(sockets, [], []):
        Usa select.select() para monitorear los sockets en la lista sockets:
            - Readable: Contiene los sockets listos para leer datos (clientes activos o el servidor listo para aceptar conexiones).
            - Los otros dos parámetros ([], []) se utilizan para monitorear sockets listos para escribir o errores, que no se manejan en este caso.
    
    3. For s in readable::
        Itera sobre los sockets listos para leer.

### Nuevo cliente

    if s is server:
        client_socket, addr = server.accept()
        print(f"Conexión desde {addr}")
        sockets.append(client_socket)
    
    - Si el socket en readable es el servidor (s is server):
        1. Client_socket, addr = server.accept():
            Acepta una nueva conexión de un cliente, devolviendo:
                - client_socket: El socket para comunicarse con el cliente.
                - addr: Dirección IP y puerto del cliente.
        2. Sockets.append(client_socket):
            Agrega el socket del cliente a la lista sockets para monitorearlo en futuros ciclos del bucle.

### Datos de un cliente existente
    
    else:
        data = s.recv(1024)
        if data:
            print(f"Recibido: {data.decode()}")
            s.send(b"HTTP/1.1 200 OK\n\nHola, cliente!")
        else:
            print("Cliente desconectado")
            sockets.remove(s)
            s.close()
    
    - Si el socket no es el servidor, es un cliente existente que ha enviado datos o ha cerrado la conexión:
        1. Data = s.recv(1024):
            Intenta leer hasta 1024 bytes de datos del cliente.
        2. If data::
            Si se reciben datos:
                - Imprime el mensaje recibido.
                - Envía una respuesta en formato HTTP.
        3. Else::
            Si no se reciben datos:
                - Significa que el cliente cerró la conexión.
                - El socket del cliente se elimina de la lista sockets.
                - Se cierra el socket para liberar recursos.
    
### Definición del proceso que se realiza

    El proceso implementado es el de un servidor no bloqueante con multiplexación de E/S, capaz de manejar múltiples conexiones concurrentes dentro de un único proceso. Este enfoque utiliza select.select() para:
    
    - Supervisar el estado de múltiples sockets sin bloquear la ejecución del programa.
    - Permitir que el servidor responda rápidamente a clientes activos mientras sigue escuchando nuevas conexiones.

### Ventajas de este enfoque

    1. Eficiencia en el manejo de recursos:
    No se crean hilos o procesos adicionales, reduciendo el consumo de memoria y CPU.
    
    2. Escalabilidad para muchas conexiones:
    Adecuado para aplicaciones con alta concurrencia, donde no todas las conexiones están activas simultáneamente.
    
    3. Simplicidad de diseño:
    No requiere mecanismos complejos de sincronización entre hilos o procesos.

### Desventajas de este enfoque

    1. Complejidad de código:
    El manejo manual de listas de sockets puede volverse complicado en aplicaciones más grandes.
    
    2. No es ideal para tareas intensivas en CPU:
    Aunque es eficiente para manejar E/S concurrente, este enfoque no aprovecha múltiples núcleos de CPU.
    
    3. Limitaciones de select.select():
    En sistemas con demasiados sockets, el rendimiento puede degradarse, ya que select revisa toda la lista en cada iteración.
    
    Alternativas como epoll (en Linux) o kqueue (en macOS/BSD) son más eficientes para muchos sockets.
