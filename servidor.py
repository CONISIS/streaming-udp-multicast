import socket
import struct
import cv2
import numpy as np
import time
import threading

#Canales activos
ca = []
estado = [True]

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


def canal(IP = "224.1.1.1",Puerto = 20001,v=cargar('MoratS.mp4'),e=0):
    global estado
    # Crear socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as Socket:

        # Que los mensajes vivan un segundo!
        Socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

        # Informar
        print("Arranqué en la IP: "+IP+" y puerto: "+str(Puerto))

        # Transmitir
        while estado[e]:
            for i in v:
                # Se envia el tamaño anunciando un nuevo frame
                Socket.sendto(np.array([np.size(i[0,:,0]),np.size(i[0,0,:]),np.size(i[:,0,0])]).tobytes(), (IP,Puerto))
                # Se secciona el frame y se envia
                for j in range(np.size(i[:,0,0])):
                    # Transformar seccion a bytes
                    enviar = bytearray(i[j,:,:].tobytes())
                    # Agregar info de posicion
                    enviar.extend(j.to_bytes(2, byteorder='big'))
                    # Enviar
                    Socket.sendto(enviar, (IP,Puerto))

    print("Termine en la IP: "+IP+" y puerto: "+str(Puerto))


v=cargar('Video.mp4')

print("Iniciando canales")
#Inicia canal

estado.append(True)
t1 = threading.Thread(target = canal,kwargs={'IP':"224.1.1.1",'v':v,'e':1})
t1.start()
ca.append(("224.1.1.1",t1))


#Inicia canal
estado.append(True)
t2 = threading.Thread(target = canal,kwargs={'IP':"224.1.1.2",'v':v,'e':2})
t2.start()
ca.append(("224.1.1.2",t2))
time.sleep(10)
estado[1]=False
time.sleep(10)
estado[2]=False

t1.join()
t2.join()
