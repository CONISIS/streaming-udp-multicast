import socket
import struct
import cv2
import numpy as np
import threading
from queue import Queue

#Control para terminar captura
cap=True
#Buffer de frames
buff=Queue()

def capturar(IP="224.1.1.1",Puerto=20001,TamBuffer= 1024):
    global cap
    global buff
    # Crear socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as Socket:

        # Conectar socket a un puerto
        Socket.bind(('',Puerto))

        # Conectarse al grupo multicast...
        grupo = socket.inet_aton(IP)
        Socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack('4sL', grupo, socket.INADDR_ANY))
        print("Iniciando captura en la IP: "+IP+" y puerto: "+str(Puerto))

        # Variables varias
        m=None # Arreglo con  tamaños
        Alto=0 # Alto del frame
        Capas=0 # Capas de color del Frame
        n=0 # Contador
        Ancho=0 # Ancho del frame
        p=[] #Lista de

        # Recibir
        while cap:
            # Recibir mensaje
            mensaje = Socket.recvfrom(TamBuffer)
            # Si se tiene un nuevo frame se espera un mensaje con el tamaño
            if len(mensaje[0])==24:
                # Se recibe tamaño
                m = np.frombuffer(mensaje[0],dtype='int64')
                Alto=m[0]
                Capas=m[1]
                Ancho=m[2]
                # Se genera el frame
                frame=np.array(p)
                # Se verifica y proyecta el frame
                if np.size(frame)>5:
                    buff.put(frame)
                # Reiniciar variables
                p=[]
                n=0
            # Recibir fragmentos de un frame
            if n<Ancho:
                recibido=np.frombuffer(Socket.recvfrom(Alto*Capas*8)[0],dtype='uint8')
                if len(recibido)==Alto*Capas:
                    p.append(recibido.reshape(Alto,Capas))
                n=n+1
    print("Captura en la IP: "+IP+" y puerto: "+str(Puerto)+" terminada")

#Inicia captura
t1 = threading.Thread(target = capturar)
t1.start()

#Inicia reproduccion
while True:
    # revisar que el buffer tenga mas de un frame
    if buff.qsize() > 0:
        cv2.imshow('Streaming UDP', buff.get())
        # Salir al presionar q
        if cv2.waitKey(50) & 0xFF == ord('q'):
            break
cv2.destroyAllWindows()

# Terminar captura
cap=False
t1.join()
