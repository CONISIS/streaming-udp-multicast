# Python Streaming UDP Multicast Service
**Contents/Contenido**

[TO CM]
## English
### Description
This is a UDP multicast streaming service fully developed on Python. It comes with a server and a client. The server reads videos from the channels folder and broadcasts them in a loop. The server generates a different IP for each channel detected. The client connects to the server, and after obtaining the catalog from the server, allows the user to pick a channel and start viewing. Currently, this is a video-only service and does not support audio: but it can be extended for this purpose. The streaming serviced is based on the Socket library for communication and on OpenCV for dealing with video. Other libraries such as Pynput are used to enhance the experience by allowing exit on keypress.

### Prerequisites
You must have the following libraries:
- OpenCV:
```python
pip3 install opencv-python-headless
```
- NumPy:
```python
pip3 install numpy
```
- Pynput:
```python
pip3 install pynput
```

### Usage
This streaming service consists of two scripts: _servidor.py_ and _cliente.py_. The first one -the server- is in charge of doing the broadcast. For this, it first scans for directories on the directory _canales_, that must be in the same location as the scripts. Each directory found in this folder corresponds to one channel. The videos for each channel must be inside the directory that corresponds to that channel: right now mp4 format is required, all other formats are ignored. The following is an example of this scheme:

├── canales

│   ├── Canal1

│   │   ├── Video1.mp4

│   │   └── Video2.mp4

│   ├── Canal2

│   │   └── Video3.mp4

│   └── Canal3

├── cliente.py

└── servidor.py

In this case, the server would interpret this as 3 channels: _Canal1_, _Canal2_, and _Canal3_. _Canal1_ would have _Video1_ and _Video2_, _Canal2_ would have _Video3_ and _Canal3_ would be empty. The server would broadcast only the first two channels as the third one is empty. Once the data is loaded the transmission begins. The server can be ended at any time by pressing the _z_ key.

The second script -the client- scans for the server and request the channel catalog and displays it. Once one channel is chosen the streaming begins. A window will open displaying the channel content, it can be quitted any time by pressing the _q_ key. Then a new channel can be selected or the client can be exited pressing _x_.

#### Server
The server broadcasts each channel at la IP `224.1.1.x: 20001` where `x` corresponds to a consecutive number assigned to the channel when the data is loaded. The server can be contacted by the clients to get the catalog at an IP and port of your choosing. To select the port use the option as `--puerto` (integer input) and to choose the IP use `--ip` (string input); this values default to `25000` and `127.0.0.1`.

Run the server:
```python
python3 servidor.py
```

Run the server with options:
```python
python3 servidor.py --ip "0.0.0.0" --puerto 20001
```

#### Client
The client contacts the server to at `127.0.0.1: 25000`, but this address can be changed using the options: `--ip` and `--puerto`. The client comes with an extra feature that allows the window to be dynamic. Usually the window will display black lines when too much data is lost, but it can be set to change the size of the window instead. This can be done setting the option `--variable` to `True`.

Run the client:
```python
python3 cliente.py
```

Run the client with dynamic window:
```python
python3 cliente.py --variable True
```

Run the client with a different address:
```python
python3 cliente.py --puerto 8000 --ip "192.168.1.1"
```

## Spanish
### Descripción
Este es un servicio de transmisión de multidifusión UDP completamente desarrollado en Python. Viene con un servidor y un cliente. El servidor lee videos de la carpeta de canales y los transmite en un bucle. El servidor genera una IP diferente para cada canal detectado. El cliente se conecta al servidor y, después de obtener el catálogo del servidor, permite al usuario elegir un canal y comenzar a verlo. Actualmente, este es un servicio de solo video y no admite audio: pero puede extenderse para este propósito. El servicio de transmisión se basa en la biblioteca Socket para comunicación y en OpenCV para tratar con video. Otras bibliotecas, como Pynput, se utilizan para mejorar la experiencia al permitir salir al presionar teclas.

### Prerrequisitos
Debe tener las siguientes bibliotecas:
- OpenCV:
```python
pip3 install opencv-python-headless
```
- NumPy:
```python
pip3 install numpy
```
- Pynput:
```python
pip3 install pynput
```

### Uso
Este servicio de transmisión consta de dos scripts: _servidor.py_ y _cliente.py_. El primero, el servidor, se encarga de hacer la transmisión. Para esto, primero busca directorios en los canales del directorio _canales_, que deben estar en la misma ubicación que los scripts. Cada directorio encontrado en esta carpeta corresponde a un canal. Los videos para cada canal deben estar dentro del directorio que corresponde a ese canal: en este momento se requiere el formato mp4, todos los demás formatos se ignoran. El siguiente es un ejemplo de este esquema:

├── canales

│   ├── Canal1

│   │   ├── Video1.mp4

│   │   └── Video2.mp4

│   ├── Canal2

│   │   └── Video3.mp4

│   └── Canal3

├── cliente.py

└── servidor.py

En este caso, el servidor interpretaría esto como 3 canales: _Canal1_, _Canal2_ y _Canal3_. _Canal1_ tendría _Video1_ y _Video2_, _Canal2_ tendría _Video3_ y _Canal3_ estaría vacío. El servidor transmitiría solo los primeros dos canales ya que el tercero está vacío. Una vez que se cargan los datos, comienza la transmisión. El servidor se puede finalizar en cualquier momento presionando la tecla _z_.

El segundo script, el cliente, busca el servidor y solicita el catálogo de canales y lo muestra. Una vez que se elige un canal, comienza la transmisión. Se abrirá una ventana que muestra el contenido del canal, se puede cerrar en cualquier momento presionando la tecla _q_. Luego se puede seleccionar un nuevo canal o se puede salir del cliente presionando _x_.

#### Servidor
El servidor transmite cada canal en la IP `224.1.1.x: 20001` donde` x` corresponde a un número consecutivo asignado al canal cuando se cargan los datos. Los clientes pueden contactar al servidor para obtener el catálogo en una IP y puerto de su elección. Para seleccionar el puerto, use la opción como `--puerto` (entrada entera) y para elegir la IP use `--ip` (entrada de cadena); estos valores predeterminados son `25000` y `127.0.0.1`.

Ejecute el servidor:
```python
python3 servidor.py
```

Ejecute el servidor con opciones:
```python
python3 servidor.py --ip "0.0.0.0" --puerto 20001
```

#### Cliente
El cliente se pone en contacto con el servidor en `127.0.0.1: 25000`, pero esta dirección se puede cambiar usando las opciones: `--ip` y `--puerto`. El cliente viene con una función adicional que permite que la ventana sea dinámica. Por lo general, la ventana mostrará líneas negras cuando se pierden demasiados datos, pero se puede configurar para cambiar el tamaño de la ventana. Esto se puede hacer configurando la opción `--variable` a `True`.

Ejecute el cliente:
```python
python3 cliente.py
```

Ejecute el cliente con ventana dinámica:
```python
python3 cliente.py --variable True
```

Ejecute el cliente con una dirección diferente:
```python
python3 cliente.py --puerto 8000 --ip "192.168.1.1"
```

-------------
By: Andrés Martínez Silva
