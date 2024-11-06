#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import json
import logging

# Configuration
mqttServer = "chirpstack.iut-blagnac.fr"
topic_subscribe = "AM107/#"
logging.basicConfig(level=logging.INFO)

# Callback de réception des messages
def on_message(client, userdata, msg):
    print(f"Message reçu sur le topic {msg.topic}: OK")
    try:
        # Désérialisation du message
        payload_str = msg.payload.decode()
        #print("Payload brut:", payload_str)
        jsonMsg = json.loads(payload_str)
        
        # Vérifier si le message est une liste avec au moins 2 éléments
        if isinstance(jsonMsg, list) and len(jsonMsg) >= 2:
            # Le premier élément contient les données des capteurs
            sensor_data = jsonMsg[0]
            # Le second élément contient les informations de l'appareil
            device_info = jsonMsg[1]
            
            # Extraction des informations de température
            temperature = sensor_data.get('temperature')
            # Extraction des informations de salle
            room = device_info.get('room')
            
            if temperature is not None and room is not None:
                print(f"Température: {temperature} °C dans la salle {room}")
            else:
                logging.error("Température ou salle non trouvée dans les données")
        else:
            logging.error("Format de message inattendu")
    
    except json.JSONDecodeError as e:
        logging.error("Erreur de décodage JSON : %s", e)

# Connexion et souscription
client = mqtt.Client()
client.on_message = on_message
client.connect(mqttServer, port=1883, keepalive=60)
client.subscribe(topic_subscribe, qos=0)
client.loop_forever()