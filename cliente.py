import socket
import struct

# Cositas varias
IP     = "224.1.1.1"
Puerto   = 20001
TamBuffer  = 1024

# Crear socket
Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Conectar socket a un puerto
Socket.bind(('',Puerto))

# Conectarse al grupo multicast...
grupo = socket.inet_aton(IP)
Socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sL', grupo, socket.INADDR_ANY))

#Recibir
while True:
    mensaje = Socket.recvfrom(TamBuffer)
    print("Message from Server {}".format(mensaje[0]))
