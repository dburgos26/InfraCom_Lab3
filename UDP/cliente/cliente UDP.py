import socket
import threading
import logging
import time
import os
logging.basicConfig(filename='logs/client.log', level=logging.INFO,format='%(asctime)s - %(levelname)s - %(message)s')

HOST = 'localhost' #IP server
PORT = 5000 #Puerto server

logging.info("===" * 10)

def client_thread(client_id,cantClientes):

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

        filename = f'cliente{client_id}-prueba{cantClientes}.txt'



        logging.info(f'Cliente {client_id}: enviando solicitud de archivo {filename}')

        s.sendto(filename.encode(), (HOST, PORT))


        DatosBloq, server = s.recvfrom(16384)

        try:
            cantBloques = int(DatosBloq.decode())
            logging.info(f'Cliente {client_id}: cantidad de bloques a recibir: {cantBloques}')
        except:
            cantBloques = 100000
            logging.info(f'Cliente {client_id}: cantidad por default a recibir: {cantBloques}')

        start_time = time.time()
        data, server = s.recvfrom(16384)
        end_time = time.time()

        transfer_time = end_time - start_time

        logging.info(f'Cliente {client_id}: tiempo de recibir del elemento 1: {transfer_time} segundos')


        if data:

            received_data = b'' # Almacenará el archivo recibido
            total_size = 0 # Almacenará el tamaño total del archivo recibido

            received_data += data

            cont = 1

            s.settimeout(5)

            while True:

                try:
                
                    s_time=time.time()
                    data, server = s.recvfrom(65535) # Recibe una parte del archivo
                    e_time=time.time()

                    transfer_time = e_time - s_time

                    logging.info(f'Cliente {client_id}: tiempo de recibir del elemento {cont}: {transfer_time} segundos')

                    cont+=1

                    if data.decode() == "TRANSFERENCIA COMPLETADA.":
                        logging.info(f"Cliente {client_id}: transferencia completada")
                        break

                    received_data += data # Agrega la parte recibida al archivo completo
                    total_size += len(data) # Actualiza el tamaño del archivo recibido

                except socket.timeout:
                    logging.info(f"Cliente {client_id}: se ha superado el tiempo de espera")
                    break
        else:
            logging.info(f'Cliente {client_id}: error al recibir el archivo')

    
    with open(f'ArchivosRecibidos/{filename}', 'wb') as f:

        f.write(received_data)

    logging.info(f'Cliente {client_id}: finalizado')

    if cantBloques > cont:
        logging.info(f'Cliente {client_id}: se han recibido menos bloques de los esperados: {cont-1} de {cantBloques}')
    elif cantBloques < cont:
        logging.info(f'Cliente {client_id}: se han recibido más bloques de los esperados: {cont-1} de {cantBloques}')
    else:
        logging.info(f'Cliente {client_id}: se han recibido la cantidad de bloques esperados: {cont-1} de {cantBloques}')
        


if __name__ == '__main__':
    num_clients = int(input('Ingrese la cantidad de clientes: '))
    threads = []
    for i in range(num_clients):
        thread = threading.Thread(target=client_thread, args=(i+1,num_clients,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
