import json
import subprocess

def read_file_json(path_json):
    """Lee un archivo JSON y devuelve los datos deserializados."""
    with open(path_json) as archivo_json:
         datos = json.load(archivo_json)
    return datos

def create_wlan0_config(datas_json):
    """Genera el contenido de configuración para wlan0 usando los datos proporcionados."""
    contenido = f"""auto wlan0
iface wlan0 inet static
        address {datas_json['ip-local-host']}
        netmask 255.255.255.0
        broadcast 192.168.10.255
        wireless-channel 5
        wireless-essid {datas_json['essid']}
        wireless-mode ad-hoc
        wireless-key {datas_json['key']}
    """
    return contenido

def create_static_routes_config(datas_json, op):
    """Genera el contenido de configuración de rutas estáticas basado en la opción proporcionada."""
    if op == 2:
        contenido = f"""#!/bin/bash
ip route flush dev wlan0
route add {datas_json['ip-local-host']} dev wlan0
route add {datas_json['ip-gateway-intermedio']} gw {datas_json['ip-local-host']} metric 1 dev wlan0
route add {datas_json['ip-gateway-principal']} gw {datas_json['ip-gateway-intermedio']} metric 2 dev wlan0
route add -net 0.0.0.0 netmask 0.0.0.0 gw {datas_json['ip-gateway-intermedio']} metric 202 dev wlan0
sudo sysctl net.ipv4.ip_forward=1
        """
    else:
        contenido = f"""#!/bin/bash
ip route flush dev wlan0
route add {datas_json['ip-local-host']} dev wlan0
route add {datas_json['ip-cliente-2']} gw {datas_json['ip-gateway-intermedio']} metric 1 dev wlan0
route add {datas_json['ip-cliente-3']} gw {datas_json['ip-gateway-intermedio']} metric 1 dev wlan0
route add {datas_json['ip-gateway-principal']} gw {datas_json['ip-gateway-intermedio']} metric 1 dev wlan0
route add -net 0.0.0.0 netmask 0.0.0.0 gw {datas_json['ip-gateway-principal']} metric 202 dev wlan0
sudo sysctl net.ipv4.ip_forward=1
        """
    return contenido

def write_config(path_file, contenido):
    """Escribe el contenido de configuración en el archivo especificado."""
    with open(path_file, 'w') as archivo:
        archivo.write(contenido)

def restart_networking():
    """Reinicia el servicio de red para aplicar los cambios de configuración."""
    subprocess.run(['sudo', 'service', 'networking', 'restart'], check=True)

def main():
    path_filejson = '/home/rsa/configuracion/Configuracion_ad-hoc.json'
    path_file_wlan0 = '/etc/network/interfaces.d/wlan0'
    path_file_rutas = '/etc/network/rutasEstaticas.sh'

    # Cargar la configuración desde el archivo JSON
    datos_json = read_file_json(path_filejson)

    # Generar y escribir la configuración de wlan0
    contenido_wlan0 = create_wlan0_config(datos_json)
    write_config(path_file_wlan0, contenido_wlan0)

    # Determinar la opción para las rutas estáticas y generar/escribir la configuración
    op = 1 if datos_json["ip-local-host"] == datos_json["ip-gateway-intermedio"] else 2
    contenido_rutas = create_static_routes_config(datos_json, op)
    write_config(path_file_rutas, contenido_rutas)

    # Reiniciar el servicio de red
    restart_networking()

if __name__ == '__main__':
    main()
