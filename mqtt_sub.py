import paho.mqtt.client as mqtt
import mysql.connector
import struct
import configparser

def connectDB():
   server_name = cp['database']['server_name']   
   port = cp['database']['port']
   user = cp['database']['user']
   password = cp['database']['pass']
   db_name = cp['database']['database_name']
   #mydb = mysql.connector.connect(host="localhost", port="3306",user="root",password="abcd24",database="dist_social")
   mydb = mysql.connector.connect(host=server_name, port=port,user=user,password=password,database=db_name)
   return mydb

def insertTable(data):
   try:      
      if conn.is_connected():
         status_registro = 1
         camara_id = 1
         tipo_id = 1
         nombre = 'prom'
         valor = float(data)
         sql = 'INSERT INTO registros (status, camara_id, valor, tipo_id, nombre) VALUES ({}, {}, {}, {}, "{}")'.format(status_registro, camara_id, valor, tipo_id, nombre)         
         mycursor.execute(sql)
         conn.commit()
   except mysql.connector.Error as error:
      print("Failed to insert record into registros table {}".format(error))
   finally:
      if (conn.is_connected()):
         #conn.close()
         print("MySQL connection is closed")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
   print("Connected with result code "+str(rc))

   # Subscribing in on_connect() means that if we lose the connection and
   # reconnect then subscriptions will be renewed.
   client.subscribe("home/cam1")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
   #print(msg.topic+" "+str(msg.payload))
   insertTable(msg.payload)
   

cp = configparser.ConfigParser()
cp.read('config.ini')
#MQTT Server
server_name_mqtt = cp['MQTT']['server_name']
port_mqtt = cp['MQTT']['port']
keepalive = cp['MQTT']['keepalive']

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
conn = connectDB()
mycursor = conn.cursor()
port_mqtt = int(port_mqtt)
keepalive = int(keepalive)
client.connect(server_name_mqtt, port_mqtt, keepalive)

client.loop_forever()