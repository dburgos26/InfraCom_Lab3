import sys
import socket
import threading
import hashlib

HOST = '192.168.223.131'
PORT = 5000

MAX_CONNECTIONS = 0
ACT_CONNECTIONS = 0

FILE_TO_SEND = 'AtlanticoCNPV2018.csv'

connected_clients = []

def handle_client(conn, addr, active_conns, data):
    print(f'Cliente {active_conns} conectado: {addr}')

    connected_clients.append(conn)

    # El programa espera hasta que todos los clientes se hayan conectado
    while len(connected_clients) < MAX_CONNECTIONS:
        pass

    threading.Thread(target=send_file, args=(conn, data, active_conns)).start()

def send_file(conn, data, active_conns):
    # Se calcula el valor de hash con la función SHA-256 y se envia al cliente junto con el archivo
    try:
        conn.send(hashlib.sha256(data).digest())
        conn.sendall(data)
    except OSError as e:
        print(e)
    conn.close()
    print(f'Cliente {active_conns} desconectado: {addr}')

MAX_CONNECTIONS = int(input("Ingrese el numero de clientes esperados: "))
print("\nEl servidor cuenta con 2 archivos:")
print("1. AtlanticoCNPV2018.csv (100 MB)")
print("2. BogotaCNPV2018.csv (250 MB)\n")
selected_file = int(input("Seleccione 1 o 2 segun el archivo que quiera enviar: "))
FILE_TO_SEND = 'AtlanticoCNPV2018.csv' if selected_file == 1 else 'BogotaCNPV2018.csv'

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(MAX_CONNECTIONS)

# Se envia el nombre del archivo y el numero de conexiones al cliente
temp_conn, temp_addr = server_socket.accept()
temp_conn.send(str(MAX_CONNECTIONS).encode("utf-8"))
temp_conn.send(FILE_TO_SEND.encode("utf-8"))

# Se recibe el mensaje de confirmacion enviado por el cliente para iniciar la transferencia
conf_cl = temp_conn.recv(1024).decode("utf-8")
temp_conn.close()

if conf_cl != 'READY':
    sys.exit()

print(f'Servidor escuchando en {HOST} : {PORT}')

with open(FILE_TO_SEND, 'rb') as f:  
    data = f.read()

while True:
    conn, addr = server_socket.accept()
    ACT_CONNECTIONS += 1
    threading.Thread(target=handle_client, args=(conn, addr, ACT_CONNECTIONS, data)).start()
