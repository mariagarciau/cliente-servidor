# cliente-servidor
Se desea realizar un programa para obtener periódicamente(Deberás establecer primero una conexión inicial para comprobar su funcionamiento y más tarde una conexión múltiple) datos meteorológicos de un determinado lugar remoto. Los datos que se pueden solicitar son: temperatura mínima, temperatura máxima, presión y pluviometría. Cada uno de estos datos se puede pedir de forma independiente. Para ello se utilizará una comunicación donde

Servidor: Se queda esperando peticiones de conexión. Recibe peticiones de información y devuelve el valor correspondiente. Los valores devueltos son del tipo float. La atención al servicio se realizará utilizando un servidor multihilo. 

Cliente: Periódicamente (defina una constante para este periodo) se conecta al servidor meteorológico y solicita por orden la temperatura mínima, temperatura máxima, presión y pluviometría, e imprime todos los valores recibidos por pantalla.


Conceptos
https://rico-schmidt.name/pymotw-3/index.html

Un cliente es todo programa que hace solicitudes a un servidor y recibe información de este, como por ejemplo: navegadores web, aplicaciones de chat y correo electrónico, entre otras.

Un servidor es un programa que recibe y maneja las peticiones de los clientes para entregar cada pieza de información al cliente que la solicitó. Algunas aplicaciones servidor son: la misma web, bases de datos, chats y correos electrónicos, etc.

Los sockets son los extremos de un canal de comunicación bidireccional. Los sockets se pueden comunicar dentro de un proceso, entre procesos dentro de la misma máquina o entre procesos de máquinas de continentes diferentes.

Los sockets pueden ser implementados a través de un diferente número de canales: sockets de dominio UNIX, TCP, UDP, etc. La librería 

socket
de python provee clases específicas para manejar el transporte común así como también una interfaz genérica para controlar todo lo demás.
El módulo 

socket
de Python provee una interfaz para la API de los sockets Berkeley (otro nombre para los sockets de Internet). Varias de las operaciones principales para usar sockets con este módulo son:
socket()
bind()
listen()
accept()
connect()
connect_ex()
send()
recv()
close()
Iniciando en la programación de redes con Python
La programación de redes en Python depende de los objetos socket. Para crear un objeto de este tipo en Python, debemos utilizar la función 

socket.socket()
disponible en el módulo socket, con la siguiente sintaxis:
socket_0 = socket.socket(socket_family, socket_type, protocol=0)
Veamos una descripción detallada de los parámetros:

socket_family: es la familia de protocolos que es usada como mecanismo de transporte. Estos valores son constantes tales como AF_INET, PF_INET, PF_UNIX, PF_X25, entre otras.
socket_type: el tipo de comunicación entre los dos extremos de la conexión, usualmente se usa SOCK_STREAM para protocolos orientados a conexiones y SOCK_DGRAM para protocolos sin conexiones.
protocol: Normalmente es 0, este parámetro es usado para identificar la variante de un protocolo dentro de una familia y tipo de socket.
Métodos de los objetos socket
socket.bind() -> este método vincula una dirección (hostname, número de puerto) a un socket.
socket.listen() -> configura e inicia un oyente TCP.
socket.accept() -> esta función acepta pasivamente una conexión de cliente TCP, esperando hasta que la conexión llegue.
Para una información más detallada en cuanto a los métodos en el módulo socktet, puedes visitar la documentación en este link.

Sockets TCP
Como verás en un momento, crearemos objetos socket usando la función 

socket.socket()
 y especificando el tipo de socket como 
socket.SOCK_STREAM
. Cuando hacemos esto, el protocolo predeterminado que usa es el Protocolo de Control de Transmisión (TCP).
Pero, ¿por qué deberíamos usar TCP?:

Es confiable: los paquetes caídos en la red son detectados y reenviados por el remitente.
Tiene una entrega de datos ordenada: los datos son leídos por tu aplicación en el orden en el que los envió el remitente.
 

Código para iniciar un servidor
El siguiente código iniciará un servidor web usando la librería sockets. El script espera a que una conexión sea hecha y si esta es recibida, mostrará los bytes recibidos.

import socket

host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024 # Usamos un número pequeño para tener una respuesta rápida 

'''Los objetos socket soportan el context manager type
así que podemos usarlo con una sentencia with, no hay necesidad
de llamar a socket_close()
'''
# Creamos un objeto socket tipo TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:

    socket_tcp.bind((host, port)) 
    socket_tcp.listen(5) # Esperamos la conexión del cliente 
    conn, addr = socket_tcp.accept() # Establecemos la conexión con el cliente 
    with conn:
        print('[*] Conexión establecida') 
        while True:
            # Recibimos bytes, convertimos en str
            data = conn.recv(BUFFER_SIZE)
            # Verificamos que hemos recibido datos
            if not data:
                break
            else:
                print('[*] Datos recibidos: {}'.format(data.decode('utf-8'))) 
            conn.send(data) # Hacemos echo convirtiendo de nuevo a bytes

En la programación de redes en Python, para escribir servidores de internet creamos un objeto socket en nuestro código y luego usamos este para llamar a otras funciones del módulo.

Veamos que hace detalladamente este script.

Definimos el host (huesped), el puerto y el tamaño del buffer de datos que recibirá la conexión
Vinculamos estas variables a nuestro objeto socket con el método 
socket.bind()
Establecemos la conexión, aceptamos los datos y mostramos los mismos.
Este script no nos muestra ningún resultado si lo ejecutamos ya que hace falta una pieza importante en nuestro modelo cliente-servidor: el cliente. El programa solo se ejecuta hasta que llamamos a la función 

socket_0.accept()
 ya que necesita un programa cliente que se conecte a él.
Código para iniciar un cliente
Vamos a escribir un programa que defina un cliente que abra la conexión en un puerto y host dado. Esto es muy simple de hacer con la función 

socket.connect(hostname, port)
 que abre una conexión TCP al hostname en el puerto port.  Una vez hayamos abierto un objecto socket podemos leer y escribir en este como cualquier otro objeto de entrada y salida(IO), siempre recordando cerrarlo tal como cerramos archivos después de trabajar con estos.
import socket

# El cliente debe tener las mismas especificaciones del servidor
host = socket.gethostname()
port = 12345
BUFFER_SIZE = 1024
MESSAGE = 'Hola, mundo!' # Datos que queremos enviar

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_tcp:
    socket_tcp.connect((host, port))
    # Convertimos str a bytes
    socket_tcp.send(MESSAGE.encode('utf-8'))
    data = socket_tcp.recv(BUFFER_SIZE)

Este script es parecido al anterior, solo que esta vez, definimos una variable 

MESSAGE
que simulan los paquetes de datos, realizamos la conexión igual que antes y llamamos al método 
socket.send(data)
después de convertir nuestra str a bytes, para asegurar la integridad de nuestros datos.
Para ejecutar este par de scripts de ejemplo, primero tenemos que ejercutar el servidor:

(aprendePython) ➜ python server.py &
Anexamos el ampersand (&) para que se ejecute esa línea y quede el proceso abierto esperando otro comando (al presionar Enter, se ejecutará el servidor hasta que ejecutemos el cliente) y luego iniciamos el cliente:

(aprendePython) ➜ python client.py
El resultado que tenemos es el siguiente:

(aprendePython) ➜ python server.py &
[1] 15024
(aprendePython) ➜ python client.py
[*] Conexión establecida
[*] Datos recibidos: Hola, mundo!
Limitaciones en el código
Si ejecutamos estos scripts e intentamos conectarnos a ese mismo servidor desde otra terminal, este simplemente rechazará la conexión. También debemos tener en cuenta que cuando el cliente realiza la llamada a 

socket_tcp.recv(1024)
, es posible que la función retorne solo un byte b’H’ de todo el mensage b’Hola mundo!’.
La variable 

BUFFER_SIZE
de valor 1024 es la cantidad máxima de datos que pueden ser recibidos de una sola vez. Pero esto no significa que la función retornará 1024 bytes. La función 
send()
también tiene este comportamiento. 
send()
retorna el número de bytes enviados, los cuales pueden ser menos que el tamaño de los datos que se envían. Debemos controlar ambas deficiencias en nuestro código.
Normalmente en la programación de redes para hacer que un  servidor maneje múltiples conexiones al mismo tiempo, se implementa la concurrencia o paralelismo.

El problema con la concurrencia es que es complicado hacer que funcione. Hay muchos matices que considerar y situaciones de las cuales protegerse. Claro, no estamos tratando de que el lector no aprenda programación concurrente, si un programa necesita escalabilidad, es casi una obligación aplicar la concurrencia para el uso de más de un procesador o núcleo.

En cambio en este tutorial usaremos algo que es más simple que el paralelismo y mucho más fácil de usar: la librería 

selectors
.
Modelo cliente-servidor de conexiones múltiples
Primero veamos como implementar un servidor que controle varias conexiones:

Servidor
import selectors
import types
import socket
selector = selectors.DefaultSelector()
def accept_conn(sock):
conn, addr = sock.accept()
print('Conexión aceptada en {}'.format(addr))
# Ponemos el socket en modo de no-bloqueo
conn.setblocking(False)
data = types.SimpleNamespace(addr=addr, inb=b'', outb=b'')
events = selectors.EVENT_READ | selectors.EVENT_WRITE
selector.register(conn, events, data=data)
def service_conn(key, mask):
sock = key.fileobj
data = key.data
if mask & selectors.EVENT_READ:
recv_data = sock.recv(BUFFER_SIZE)
if recv_data:
data.outb += recv_data
else:
print('Cerrando conexion en {}'.format(data.addr))
selector.unregister(sock)
sock.close()
if mask & selectors.EVENT_WRITE:
if data.outb:
print('Echo desde {} a {}'.format(repr(data.outb), data.addr))
sent = sock.send(data.outb)
data.outb = data.outb[sent:]
if __name__ == '__main__':
host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024 # Usamos un número pequeño para tener una respuesta rápida
# Creamos un socket TCP
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Configuramos el socket en modo de no-bloqueo
socket_tcp.setblocking(False)
socket_tcp.bind((host, port))
socket_tcp.listen()
print('Socket abierto en {} {}'.format(host, port))
socket_tcp.setblocking(False)
# Registramos el socket para que sea monitoreado por las funciones selector,.select()
selector.register(socket_tcp, selectors.EVENT_READ, data=None)
while socket_tcp:
events = selector.select(timeout=None)
for key, mask in events:
if key.data is None:
accept_conn(key.fileobj)
else:
service_conn(key, mask)
socket_tcp.close()
print('Conexión terminada.')
Detallemos un poco más nuestra implementación:

Al igual que antes definimos las variables necesarias a vincular con el socket, estas son: 
host, port, BUFFER_SIZE, MESSAGE
Configuramos el socket para en modo no-bloqueo con: 
socket_tcp.setblocking(False)
. Las funciones del módulo 
socket
no retornan un valor inmediatamente, estas tienen que esperar que se complete una llamada del sistema para retornar un valor. Cuando configuramos el socket en no-bloqueo, hacemos que nuestra aplicación no se detenga esperando una respuesta del sistema.
Comenzamos un ciclo while en el cual, la primera línea es: 
events = sel.select(timeout=None)
. Esta función bloquea hasta que haya sockets listos para ser escritos/leídos. Luego retorna una lista de pares (clave, evento), uno por cada socket. La clave es un 
SelectorKey
que contiene un atributo 
fileobj
. 
key.fileobj
es el objeto socket y 
mask
 es una máscara de evento para las operaciones que están listas.
Si 
key.data
es None, entonces sabemos que viene del socket que está abierto y necesitamos aceptar la conexión. Llamamos a la función 
accept_conn()
que hemos definido para manejar esta situación.
Si 
key.data
 no es None, entonces es un socket cliente que está listo para ser aceptado y necesitamos atenderlo. Así que llamamos a la función 
service_conn()
 con 
key
y 
mask
como argumentos, que contienen todo lo que necesitamos para operar el socket.
Cliente
Ahora veamos una implementación de un cliente. Es bastante parecida a la implementación del servidor pero en lugar de esperar conexiones, el cliente empieza a iniciar conexiones con la función 

start_connections()
.
import socket
import selectors
import types
selector = selectors.DefaultSelector()
messages = [b'Mensaje 1 del cliente', b'Mensaje 2 del cliente']
BUFFER_SIZE = 1024
def start_connections(host, port, num_conns):
server_address = (host, port)
for i in range(0, num_conns):
connid = i + 1
print('Iniciando conexión {} hacia {}'.format(connid, server_address))
socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Conectamos usando connect_ex() en lugar de connect()
# connect() retorna una excepcion
# connect_ex() retorna un aviso de error
socket_tcp.connect_ex(server_address)
events = selectors.EVENT_READ | selectors.EVENT_WRITE
data = types.SimpleNamespace(connid=connid,
msg_total=sum(len(m) for m in messages),
recv_total=0,
messages=list(messages),
outb=b'')
selector.register(socket_tcp, events, data=data)
events = selector.select()
for key, mask in events:
service_connection(key, mask)
def service_connection(key, mask):
sock = key.fileobj
data = key.data
if mask & selectors.EVENT_READ:
recv_data = sock.recv(BUFFER_SIZE) # Debe estar listo para lectura
if recv_data:
print('Recibido {} de conexión {}'.format(repr(recv_data), data.connid))
data.recv_total += len(recv_data)
if not recv_data or data.recv_total == data.msg_total:
print('Cerrando conexión', data.connid)
selector.unregister(sock)
sock.close()
if mask & selectors.EVENT_WRITE:
if not data.outb and data.messages:
data.outb = data.messages.pop(0)
if data.outb:
print('Enviando {} a conexión {}'.format(repr(data.outb), data.connid))
sent = sock.send(data.outb) # Debe estar listo para escritura
data.outb = data.outb[sent:]
if __name__ == '__main__':
host = socket.gethostname() # Esta función nos da el nombre de la máquina
port = 12345
BUFFER_SIZE = 1024 # Usamos un número pequeño para tener una respuesta rápida
start_connections(host, port, 2)
