#!/bin/bash

# Copia los scripts de Python a la carpeta /home/rsa/ejecutables
cp /home/rsa/Coordinometro-RSA/programas/*.py /home/rsa/ejecutables/

# Copia los task-scripts al directorio /usr/local/bin
sudo cp task-scripts/ayuda.sh /usr/local/bin/ayuda
sudo cp task-scripts/informacion.sh /usr/local/bin/informacion 
sudo cp task-scripts/comprobar.sh /usr/local/bin/comprobar