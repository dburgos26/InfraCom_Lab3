from asyncio import wait
import socket
import threading
import logging
import time


HOST = 'localhost' #IP server
PORT = 5000 #Puerto server
FILE_PATH = 'textoPequeño1.txt'
BLOCK_SIZE = 1024
logging.basicConfig(filename='logs/server.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')
CONEXIONESGEN = 0

logging.info("===" * 100)


with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:

    server_socket.bind((HOST, PORT))

    logging.info(f'Servidor escuchando en {HOST}:{PORT}')

    with open(FILE_PATH, 'rb') as file:
        file_data = file.read()

    def client_thread(client_address):

       
        global CONEXIONESGEN
        CONEXIONES = CONEXIONESGEN
        CONEXIONESGEN += 1

        logging.info(f'Conexión #{CONEXIONES} -- inicio conexcion con {client_address}')

        #cantidad de bloques
        blocks = len(file_data) // BLOCK_SIZE
        try:
            server_socket.sendto(str(blocks).encode(), client_address)
            logging.info(f'Conexión #{CONEXIONES} -- Enviando cantidad de bloques: {blocks}')
        except:
            logging.info(f'Conexión #{CONEXIONES} -- Error al enviar la cantidad de bloques a {client_address}')


        try:
            start_time = time.time()

            cont = 0

            with open(FILE_PATH, 'rb') as file:
                while True:
                    data = file.read(BLOCK_SIZE)
                    if not data:
                        break
                    s_time = time.time()
                    server_socket.sendto(data, client_address)
                    e_time = time.time()
                    cont += 1
                    logging.info(f'Conexión #{CONEXIONES} -- Bloque #{cont} enviado en {e_time - s_time} segundos')

            end_time = time.time()

            transfer_time = end_time - start_time

            logging.info(f'Conexión #{CONEXIONES} -- Tiempo de transferencia total: {transfer_time} segundos')

            logging.info(f'Conexión #{CONEXIONES} -- Archivo enviado a {client_address}')
            
        except:
            logging.info(f'Conexión #{CONEXIONES} -- Error al enviar el archivo a {client_address}')

        wait(5)

        server_socket.sendto("TRANSFERENCIA COMPLETADA.".encode(), client_address)


        logging.info(f'Conexión #{CONEXIONES} -- Cerrando conexión con {client_address}')
    
    
    while True:
        data, client_address = server_socket.recvfrom(65535)

        logging.info(f'Mensaje recibido de {client_address}: {data.decode()}')

        threading.Thread(target=client_thread, args=(client_address,)).start()