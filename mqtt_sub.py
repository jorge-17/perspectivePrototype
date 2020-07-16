import paho.mqtt.client as mqtt
import mysql.connector
import struct

def connectDB():
   mydb = mysql.connector.connect(host="localhost", port="3306",user="root",password="abcd24",database="dist_social")
   return mydb

def insertTable(data):
   try:      
      if conn.is_connected():
         status_registro = 1
         camara_id = 1
         tipo_id = 1
         nombre = 'prom'
         valor = float(data)
         print(valor)  
         sql = 'INSERT INTO registros (status, camara_id, valor, tipo_id, nombre) VALUES ({}, {}, {}, {}, "{}")'.format(status_registro, camara_id, valor, tipo_id, nombre)
         print(sql)
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
   



client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
conn = connectDB()
mycursor = conn.cursor()
client.connect("localhost", 1883, 60)

client.loop_forever()