import configparser
import json

config = configparser.ConfigParser()
config.read('config.ini')

#Data Camaras
noCamaras = input("Ingresa el número de camaras: ")
if noCamaras != '':
    noCamaras = int(noCamaras)
    contCamaras = 1
    while noCamaras > 0:
        id_camara = input("Ingresa el ID de la camara {}: ".format(contCamaras))
        strIdCam = "id_camara{}".format(contCamaras)
        url_camara = input("Ingresa la URL de la camara {}: ".format(contCamaras))
        strUrlCam = "url_camara{}".format(contCamaras)
        config['camaras'][strIdCam] = id_camara
        config['camaras'][strUrlCam] = url_camara
        contCamaras += 1
        noCamaras -= 1
else:
    print("No ingresaste No. de camaras, permanecera el anterior...")


#Data Base de datos
askUpdateBD = input("Actualizar conexión a base de datos (s/n): ")
while askUpdateBD == 's' or askUpdateBD == 'n':
    if askUpdateBD == 's':
        for key in config['database']:
            value = config['database'][key]
            valueInput = input("Ingresa el valor de {}: ({}) ".format(key, value))            
            data = value if valueInput == '' else valueInput
            config['database'][key] = data
        askUpdateBD = ''
    else:
        print("No se actualizará la conexión a base de datos, permanecera el anterior...")
        askUpdateBD = ''

#Data MQTT
askUpdateMQTT = input("Actualizar conexión al servidor MQTT (s/n): ")
while askUpdateMQTT == 's' or askUpdateMQTT == 'n':
    if askUpdateMQTT == 's':
        for key in config['MQTT']:
            value = config['MQTT'][key]
            valueInput = input("Ingresa el valor de {}: ({}) ".format(key, value))            
            data = value if valueInput == '' else valueInput
            config['MQTT'][key] = data
        askUpdateMQTT = ''
    else:
        print("No se actualizará la conexión al servidor MQTT, permanecera el anterior...")
        askUpdateMQTT = ''

askSave = ''
while askSave != 's' and askSave != 'n':
    valCambios = input("¿Confirmas los cambios? (s/n): ")
    if valCambios == 's':
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        askSave = valCambios
    elif valCambios == 'n':
        print("El archivo de configuracion quedara sin cambios...")
        askSave = valCambios
