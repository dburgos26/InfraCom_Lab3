# InfraCom_Lab3
## Sección 3 - Grupo 1

Aquí están las instrucciones generales para iniciar los diferentes servidores

En los dos casos se tiene un archivo .zip donde están los archivos de texto con los tamaños definidos 

## Instrucciones del servidor TCP

1. En la constante *HOST*, de los archivos *lab3_client.py* y *lab3_server.py*, colocar la dirección IP de la máquina en la que se ejecutará el servidor
2. Desde una terminal en la máquina virtual, ejecutar el archivo de Python correspondiente a la aplicación del servidor con el comando *python lab3_server.py*. Se le pedirá ingresar el número de clientes esperados y el archivo que quiere transferir
3. Desde una terminal en la máquina local, ejecutar el archivo de Python correspondiente a la aplicación del cliente con el comando *python lab3_client.py*. Se le notificará que se iniciará la cantidad de clientes especificados en el servidor, posteriormente debe escribir **READY** desde la terminal para iniciar la transferencia del archivo a todos los clientes
4. Se imprimirá por la terminal cuando cada cliente inicie y también cuando finalice
5. Esperar hasta que todos los clientes hayan finalizado su proceso. Se habrán guardado los archivos transferidos a cada cliente y el archivo de log en las carpetas *ArchivosRecibidos* y *Logs*, respectivamente


## Instrucciones del servidor UDP

1. En la constante *HOST*, de los archivos *Serv UDP.py* y *cliente UDP.py*, colocar la dirección IP de la máquina en la que se ejecutará el servidor y revisar que en la variable *PORT* este el mismo puerto en los dos archivos
2. En el servidor escriba el nombre del archivo que se desea enviar
3. En la máquina virtual inicie el servidor desde consola ejecutando el archivo *Serv UDP.py* y abra el archivo *server.log* ya que en este aparecerá toda la información
4. En la máquina local ejecute el archivo *cliente UDP.py*, escriba el número de clientes por consola y abra el archivo *client.log* ya que en este aparecerá toda la información
5. Espere a que se envíen los archivos
6. Cuando se termine la transferencia la consola del servidor no cambiara y se terminara la ejecución del cliente, todos los detalles estarán en los archivos *.log*
