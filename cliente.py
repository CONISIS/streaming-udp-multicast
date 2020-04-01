import socket
import struct
import cv2
import numpy as np

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

# Variables varias
m=None # Arreglo con  tamaños
Alto=0 # Alto del frame
Capas=0 # Capas de color del Frame
n=0 # Contador
Ancho=0 # Ancho del frame
p=[] #Lista de

# Recibir
while True:
    # Recibir mensaje
    mensaje = Socket.recvfrom(TamBuffer)
    # Si se tiene un nuevo frame se espera un mensaje con el tamaño
    if mensaje[0]==b"Nuevo Frame":
        # Se recibe tamaño
        mensaje = Socket.recvfrom(TamBuffer)
        m = np.frombuffer(mensaje[0],dtype='int64')
        if np.size(m)==3:
            Alto=m[0]
            Capas=m[1]
            Ancho=m[2]
        # Se genera el frame
        frame=np.array(p)
        # Se verifica y proyecta el frame
        if np.size(frame)>5:
            cv2.imshow('Frame', frame)
            cv2.waitKey(100)
        # Reiniciar variables
        p=[]
        n=0
    # Recibir fragmentos de un frame
    if n<Ancho:
        u=np.frombuffer(Socket.recvfrom(Alto*Capas*8)[0],dtype='uint8')
        if len(u)==Alto*Capas:
            p.append(u.reshape(Alto,Capas))
        n=n+1
