import paho.mqtt.client as mqttclient
import time
import json
import random
import geocoder

BROKER_ADDRESS = "demo.thingsboard.io"
PORT = 1883
THINGS_BOARD_ACCESS_TOKEN = "3ZndOZls9AUGTR2xj4qH"

print("Xin chào ThingsBoard")


def subscribed(client, userdata, mid, granted_qos):
    print("Subscribed...")


def recv_message(client, userdata, message):
    print("Received: ", message.payload.decode("utf-8"))
    temp_data = {'value': True}
    try:
        jsonobj = json.loads(message.payload)
        if jsonobj['method'] == "setValue":
            temp_data['value'] = jsonobj['params']
            client.publish('v1/devices/me/attributes', json.dumps(temp_data), 1)
    except:
        pass


def connected(client, usedata, flags, rc):
    if rc == 0:
        print("Thingsboard connected successfully!!")
        client.subscribe("v1/devices/me/rpc/request/+")
    else:
        print("Connection is failed")


client = mqttclient.Client("Gateway_Thingsboard")
client.username_pw_set(THINGS_BOARD_ACCESS_TOKEN)
client.on_connect = connected
client.connect(BROKER_ADDRESS, 1883)
client.loop_start()
client.on_subscribe = subscribed
client.on_message = recv_message

temp = 30
humi = 50
light = 100
counter = 0

provinces = ['Đà Lạt', 'Điện Biên Phủ', 'Huế', 'Nha Trang', 'Phan Thiết', 'Cà Mau', 'Bến Tre', 'Hội An', 'Vũng Tàu', 'Quảng Ngãi']
locations = [geocoder.arcgis(province, maxRows=1) for province in provinces]

latitude, longitude = locations[0].latlng
location_name = locations[0].address


while True:
    collect_data = {'temperature': temp, 'humidity': humi, 'light':light, 'longitude':longitude, 'latitude':latitude, 'location_name': location_name}

    latitude, longitude = locations[counter].latlng
    location_name = locations[counter].address
    temp = random.randint(20, 100)
    humi = random.randint(40, 100)
    light = random.randint(90, 100)
    counter = random.randint(0, len(locations)-1)

    client.publish('v1/devices/me/telemetry', json.dumps(collect_data), 1)
    time.sleep(4)