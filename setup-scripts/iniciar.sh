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