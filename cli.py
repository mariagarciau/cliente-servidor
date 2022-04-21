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


#Variables
host = 'localhost'
port = 8050
#Se importa el módulo
import socket
 
#Creación de un objeto socket (lado cliente)
obj = socket.socket()
 
#Conexión con el servidor. Parametros: IP (puede ser del tipo 192.168.1.1 o localhost), Puerto
obj.connect((host, port))
print("Conectado al servidor")
 
#Creamos un bucle para retener la conexion
while True:
    #Instanciamos una entrada de datos para que el cliente pueda enviar mensajes
    mens = raw_input("Mensaje desde Cliente a Servidor >> ")
 
    #Con el método send, enviamos el mensaje
    obj.send(mens)

#Cerramos la instancia del objeto servidor
obj.close()

#Imprimimos la palabra Adios para cuando se cierre la conexion
print("Conexión cerrada")