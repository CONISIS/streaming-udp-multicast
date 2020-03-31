import socket
import struct

# Cositas varias
IP     = "224.1.1.1"
Puerto   = 20001

# Crear socket
Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Que los mensajes vivan un segundo!
Socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

# Informar
print("Arranqué en la IP: "+IP+" y puerto: "+str(Puerto))

# Transmitir
while(True):
    Socket.sendto(str.encode("Buenaaas"), (IP,Puerto))
