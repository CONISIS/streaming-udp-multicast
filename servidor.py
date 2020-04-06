import socket
import struct
import cv2
import numpy as np
import time
import threading
from os import walk
import argparse
import sys
from pynput import keyboard
import select

# Obtener argumentos
parser = argparse.ArgumentParser()
parser.add_argument('--ip', type=str, help='La IP donde el servidor escucha nuevos clientes', default="127.0.0.1")
parser.add_argument('--puerto', type=int, help='El puerto donde el servidor escucha nuevos clientes', default=20001)
args = parser.parse_args()

# Variables de conexion con clientes
IP = args.ip
Puerto = args.puerto
TamBuffer = 1024

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

# Inicia un canal de broadcast
def canal(IP = "224.1.1.1",Puerto = 20001,v=cargar('Video.mp4'),e=0):
    global estado
    # Crear socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as Socket:

        # Que los mensajes vivan un segundo!
        Socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, struct.pack('b', 1))

        # Informar
        print("Canal "+str(e)+": Arranqué en "+IP+":"+str(Puerto))

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

    print("Canal "+str(e)+": Termine en "+IP+":"+str(Puerto))

# Escuchar teclado para detectar interrupcion
interrumpir = True
def on_press(tecla):
    global interrumpir
    if tecla == keyboard.KeyCode.from_char("q"):
        print ("\nApagando...")
        interrumpir = False
        return False


print ("\nBienvenido al servidor de streaming por broadcast UDP (presione 'q' para salir)\n")

# Cargar contenido
print ("Cargando contenido...")
v=cargar('Video.mp4')

print("Iniciando canales...")
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

# Loop principal
# Inicia escucha de teclado
with keyboard.Listener(on_press=on_press) as listener:
    # Crear socket
    with socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM) as Socket:
        # Conecta socket a ip y puerto
        Socket.bind((IP, Puerto))
        # Iniciando escucha de clientes
        print("Escuchando clientes en: "+IP+":"+str(Puerto)+"\n")
        while interrumpir:
            # Verifica si llego mensaje
            leer, escribir, error = select.select([Socket],[],[],10)
            # Si llego
            if Socket in leer:
                recibido = Socket.recvfrom(TamBuffer)
                # Verifica mensaje
                if recibido[0].decode() == "Hola":
                    # Informa solicitud
                    print("Solicitud de catalogo: "+recibido[1][0]+":"+str(recibido[1][1]))
                    # Envia catalogo
                    s = "Canales disponibles: "
                    for i in ca:
                        s=s+i[0]+" "
                    Socket.sendto(str.encode(s), recibido[1])
    listener.join()

# Detener threads
print("Apagando canales...")
for i in range(len(estado)):
    estado[i]=False
for i in ca:
    i[1].join()
print()
