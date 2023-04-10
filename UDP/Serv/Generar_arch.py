import os

# Tamaño máximo del archivo en bytes
tamanio_maximo = 100 * 1024 * 1024

# Nombre del archivo y ruta
ruta_archivo = 'textoPequeño1.txt'

# Abrir archivo en modo de escritura
with open(ruta_archivo, 'w') as archivo:
    # Escribir párrafo en archivo hasta alcanzar el tamaño máximo
    while os.path.getsize(ruta_archivo) < tamanio_maximo:
        # Párrafo a escribir
        parrafo = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam faucibus pellentesque orci, at dapibus magna consectetur sed. Donec ac leo libero. Suspendisse potenti. Sed suscipit leo in risus aliquet, vel bibendum dolor pulvinar. Nullam ullamcorper velit nec dolor blandit, eu tincidunt enim venenatis. Quisque condimentum purus sit amet lobortis pharetra. Suspendisse vel metus sagittis, convallis ipsum eu, aliquet justo. Integer vel odio at magna pulvinar porttitor. Nulla facilisi. Sed hendrerit luctus velit, vel pharetra elit rhoncus in. Nunc cursus tellus id augue consequat, sed bibendum urna pellentesque. Aenean consequat elit ac magna feugiat blandit. \n'
        
        # Escribir párrafo en archivo
        archivo.write(parrafo)

# Cerrar archivo
archivo.close()

print('Archivo generado correctamente')

