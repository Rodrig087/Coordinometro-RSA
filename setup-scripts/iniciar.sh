#!/bin/bash

# Copiar el directorio "configuracion" a la ruta /home/rsa/
cp -r configuracion /home/rsa/

# Crea los directorios necesarios
mkdir -p /home/rsa/ejecutables
mkdir -p /home/rsa/fotos
mkdir -p /home/rsa/fotos/tmp
mkdir -p /home/rsa/log-files
mkdir -p /home/rsa/resultados

# Copia los scripts de Python a la carpeta /home/rsa/ejecutables
cp /home/rsa/Coordinometro-RSA/programas/*.py /home/rsa/ejecutables/

# Copia los task-scripts al directorio /usr/local/bin
sudo cp task-scripts/ayuda.sh /usr/local/bin/ayuda
sudo cp task-scripts/informacion.sh /usr/local/bin/informacion 
sudo cp task-scripts/comprobar.sh /usr/local/bin/comprobar

# Conceder permisos de ejecucion a los task-scripts
sudo cp task-scripts/ayuda.sh /usr/local/bin/ayuda
sudo chmod +x /usr/local/bin/informacion
sudo chmod +x /usr/local/bin/comprobar