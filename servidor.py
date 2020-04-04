import socket
import struct
import cv2
import numpy as np

# Cositas varias
IP     = "224.1.1.1"
Puerto   = 20001

# Crear socket
Socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Que los mensajes vivan un segundo!
Socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

# Cargar video
def cargar(ruta):
    p=[]
    Video = cv2.VideoCapture(ruta)
    if (Video.isOpened()== False):
        print("Error cargando el video")
        return None
    while(Video.isOpened()):
        ret, frame = Video.read()
        if ret == True:
            p.append(frame)
        else:
            break
    Video.release()
    return p

# Obtener video
v=cargar('Video.mp4')

# Informar
print("Arranqué en la IP: "+IP+" y puerto: "+str(Puerto))

# Transmitir
while(True):
    for i in v:
        # Se envia el tamaño anunciando un nuevo frame
        Socket.sendto(np.array([np.size(i[0,:,0]),np.size(i[0,0,:]),np.size(i[:,0,0])]).tobytes(), (IP,Puerto))
        # Se secciona el frame y se envia
        for j in range(np.size(i[:,0,0])):
            Socket.sendto(i[j,:,:].tobytes(), (IP,Puerto))
