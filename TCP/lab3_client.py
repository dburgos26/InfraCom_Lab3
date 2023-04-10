import os
import sys
import socket
import threading
import hashlib
import time
from datetime import datetime

HOST = '192.168.223.131'
PORT = 5000

BUFFER_SIZE = 1024000

FILE_TO_SAVE = ''

CLIENT_NUMBER = 0
SELECTED_FILE = ''

check_dict = {} 
time_dict = {}
hash_dict = {}
current_clients = []

def new_client(client_id, total_clients):
    # Se establece la conexion con el servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print(f"Cliente {client_id} iniciado")

    FILE_TO_SAVE = f"ArchivosRecibidos/Cliente{client_id}-Prueba{total_clients}.csv"
    
    # Se recibe el valor de hash enviado por el servidor
    server_hcode = client_socket.recv(BUFFER_SIZE)
    
    # Se recibe el archivo enviado por el servidor dividido en chunks
    data = b''
    t1 = time.perf_counter()
    while True:
        chunk = client_socket.recv(BUFFER_SIZE)
        if not chunk:
            break
        data += chunk
    t2 = time.perf_counter()

    # Se calcula el valor de hash con la función SHA-256 y se compara con el valor enviado por el servidor
    client_hcode = hashlib.sha256(data).digest()
    hash_dict[client_id] = (server_hcode == client_hcode)

    # Se escribe la informacion recibida en el archivo
    with open(FILE_TO_SAVE, 'wb') as f:
        f.write(data)

    # Se verifica que el archivo haya sido transferido en su totalidad
    size_check = 100000 if SELECTED_FILE == 'AtlanticoCNPV2018.csv' else 250000
    with open(FILE_TO_SAVE,'r') as v:
        v.seek(0, os.SEEK_END)
        check_dict[client_id] = (v.tell() >= size_check)

    # Se guarda el tiempo de transferencia
    time_dict[client_id] = t2-t1
    client_socket.close()
    print(f"Cliente {client_id} desconectado")
    current_clients.append(True)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
CLIENT_NUMBER = int(client_socket.recv(BUFFER_SIZE).decode("utf-8"))
SELECTED_FILE = client_socket.recv(BUFFER_SIZE).decode("utf-8")

print(f'\nSe van a iniciar {CLIENT_NUMBER} conexiones...')

# Se envia el mensaje de confirmacion al servidor para iniciar la transferencia
conf = input("\nEscriba READY para notificar que el cliente se encuentra listo: ")
client_socket.send(conf.encode("utf-8"))

if conf != 'READY':
    sys.exit()

test_date = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
LOG_FILE_NAME = f"Logs/{test_date}-log.txt"

# Se inician los clientes definidos por consola
for i in range(CLIENT_NUMBER):
    threading.Thread(target=new_client, args=(str(i+1), CLIENT_NUMBER)).start()

# El programa espera hasta que todos los clientes hayan finalizado la transferencia 
while len(current_clients) < CLIENT_NUMBER:
    pass

# Se crea el archivo de log
with open(LOG_FILE_NAME, 'w') as l:
    l.write(f'PRUEBA CON {CLIENT_NUMBER} CLIENTES\n\n')
    l.write(f'Archivo enviado: {SELECTED_FILE}\n')
    l.write('Datos transferidos: 100 MB\n') if SELECTED_FILE == 'AtlanticoCNPV2018.csv' else l.write('Datos transferidos: 250 MB\n')
    l.write('\n')
    for i in range(CLIENT_NUMBER):
        l.write(f'----- CLIENTE {i+1}\n')
        l.write('Transferencia: EXITOSA\n') if check_dict[str(i+1)] else l.write('Transferencia: FALLIDA\n')
        l.write('Archivo transferido sin modificaciones: SI\n') if hash_dict[str(i+1)] else l.write('Archivo transferido sin modificaciones: NO\n')
        l.write(f'Tiempo de transferencia: {time_dict[str(i+1)]} segundos\n')
        l.write('\n')