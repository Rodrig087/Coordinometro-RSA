import numpy as np
import cv2
from datetime import date
from datetime import datetime
import os
from picamera import PiCamera
from time import sleep
import time
import RPi.GPIO as GPIO
from time import sleep
import json

camera = PiCamera()
bandera=False
print(str(time.strftime("%H"))+":"+str(time.strftime("%M"))+":"+str(time.strftime("%S")))

def TomarFotografia(direccionCarpeta):
       now = datetime.now()       
       
       GPIO.setmode(GPIO.BCM)
       GPIO.setwarnings(False)
       GPIO.setup(12, GPIO.OUT)
       #GPIO.output(12, GPIO.HIGH)
       pwm = GPIO.PWM(12, 100)
       pwm.start(100)
       sleep(1)
       try:
                            
       ##########################-Captura de Imagen-###########################
       ########################################################################
              camera.resolution= (600,300)
              #camera.rotation = 180
              camera.start_preview()
              #camera.capture(direccionCarpeta+'imagenSinZoom.jpeg')
              sleep(1)
              camera.zoom = (0.3, 0.5, 0.4, 0.4)
              sleep(1)
              imagenZoomx2 = direccionCarpeta +str(now)+'.jpg'
              camera.capture(imagenZoomx2)
              camera.stop_preview()
              sleep(1)
              pwm.stop()   
       except:
              print("No se puede capturar la imagen")
              pwm.stop()
       
       return imagenZoomx2,now

def ProcesarImagenV3(pathImagen,directorioTMP,directorioResult,directorioLogFile):
       Imagen = pathImagen[-30:]
       Imagen = Imagen[0:26]
       pathFoto = pathImagen
       mat_datos_x = []
       BordeMenor = 0

       try:  
              tiempoImagen = Imagen[0:19]
              tiempoImagen_dt = datetime.strptime(tiempoImagen, '%Y-%m-%d %H_%M_%S')
              tiempoImagen_str = tiempoImagen_dt.strftime('%Y-%m-%dT%H:%M:%S')

              img = cv2.imread(pathFoto)
              gris = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
              gauss = cv2.medianBlur(gris, 13)
              gauss = cv2.equalizeHist(gauss)

              # Define los pares de umbrales para probar con Canny 

              canny_thresholds = [(30, 90), (30, 60), (20, 60), (20, 40), (10, 30), (10, 20), (5,15), (5,10), (2,6), (2,4), (1,3), (1,2)]
              canny_thresholds.reverse()
              lines_found1 = False

              val_x = [(0,300),(300,600)]
              y_min = 0  # Valor mínimo en píxeles para y
              y_max = 300 # Valor máximo en píxeles para y

              alm_lines = []
              for k in val_x:
                     for thresholds in canny_thresholds:
                            # if not lines_found:
                            # Recortar la imagen a la región de interés
                            roi = gauss[y_min:y_max, k[0]:k[1]]
                            canny = cv2.Canny(roi, thresholds[0], thresholds[1])
                            lines = cv2.HoughLinesP(image=canny, rho=1, theta=np.pi / 180, threshold=100, lines=np.array([]),
                                                 minLineLength=180, maxLineGap=100)
                            if lines is not None:
                                   lines_found1 = True
                                   alm_lines.append(lines)
                                   break

              if not lines_found1:
                     msg = f"En la imagen {Imagen}.jpg no se pudo detectar lineas en cualquiera de los umbrales disponibles \n"
                     make_file_log(directorioLogFile,msg)
                     print("Error: No se encontro ninguna linea en la imagen")
              else: 
                     conta = 0
                     for k1 in alm_lines:
                            for line in k1:
                                   x_min = val_x[conta][0]
                                   x1, y1, x2, y2 = line[0]

                                   # Ajustar las coordenadas x1, y1, x2, y2 a la posición original en la imagen completa
                                   x1 += x_min
                                   x2 += x_min
                                   y1 += y_min
                                   y2 += y_min

                                   # Considerar la línea como vertical:
                                   if abs(x1 - x2) < 15:
                                          cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3, cv2.LINE_AA)
                                          mat_datos_x.append(x1)
                            conta += 1

                     if mat_datos_x:
                            # Guardar la imagen después de procesar todas las líneas
                            cv2.imwrite(directorioTMP + Imagen + '.jpg', img)
                            BordeMayor = max(mat_datos_x)
                            BordeMenor = min(mat_datos_x)
                            anchoCable = BordeMayor - BordeMenor
                            
                            relacionPixel=2/anchoCable
                            print(anchoCable)
                            print(str(BordeMenor*relacionPixel)+' mm')
                            
                            f = open(directorioResult+"datosMedidos.csv","a")

                            if (BordeMayor<(BordeMenor+50)):
                                   # Borde unico en un archivo de texto
                                   if (BordeMayor<(BordeMenor+25)):
                                          anchoCable = 'null'
                                          mediaBordeDifuso = (BordeMayor-BordeMenor)/2
                                          BordeMenor = BordeMenor+int(mediaBordeDifuso)
                                          BordeMayor = BordeMenor
                                   msg = f"En la imagen {Imagen}.jpg se detecto un unico borde, cuyos resultados son\n\tBorde Menor: {BordeMenor}\n\tBorde Mayor: {BordeMayor}\n\tAncho del Cable: {BordeMenor*relacionPixel}mm \n"
                                   make_file_log(directorioLogFile,msg)
                            else:
                                   f.write(str(horaFecha)+","+str(BordeMenor)+","+ str(BordeMayor)+","+str(BordeMenor*relacionPixel)+"\n")
                                   f.close

                            # break  # Salir del bucle si se han encontrado líneas
       except Exception as e:
              msg = f"No se pudo procesar la {Imagen}.jpg al presentar este error {e}" 
              make_file_log(directorioLogFile,msg)

       
def read_file_json(path_json):        
       with open(path_json) as archivo_json:
              datos = json.load(archivo_json)
       
       return datos

def make_file_log(path_log,msg): 
       fecha = str(time.strftime("%d-%m-%y"))
       hora  = str(time.strftime("%H:%M:%S"))
       f = open(path_log+fecha+'.log',"a")
       f.write(hora+"\t"+msg)
       f.close



directorio_json = '/home/rsa/configuracion/DatosConfiguracion.json'
datos_config  = read_file_json(directorio_json)

now = datetime.now()

fecha = time.strftime("%d-%m-%y")
hora  = time.strftime("%H:%M:%S")

# Directorios 
directorioFotos   = datos_config["directorios"]["fotos"]
directorioResult  = datos_config["directorios"]["resultados-csv"]
directorioLogFile = datos_config["directorios"]["log-files"]
directorioTMP     = datos_config["directorios"]["archivos-tmp"]

imagenTomada,horaFecha=TomarFotografia(directorioFotos)

ProcesarImagenV3(imagenTomada,directorioTMP,directorioResult,directorioLogFile)

