import random
from paho.mqtt import client as mqtt_client

broker = '172.21.3.184'
port = 1883
topic = "zones"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
# username = 'emqx'
# password = 'public'
zones = ["Z00", "Z15", "Z30", "Z45"]
maximum_time = 20 
round = 0
current_time = maximum_time 
current_green_light = 0
reduce_zone = ''

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)
    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        global current_time, current_green_light, maximum_time, round, reduce_zone
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        message = msg.payload.decode()
        msg_list = message.split('|')

        current_time = (current_time - 1) % maximum_time
        if current_time == maximum_time - 1:
            current_green_light = (current_green_light + 1) % 4
        next_zone = zones[(current_green_light + 1) % 4]
        for zone in msg_list:
            zone = zone.strip()
            key = zone[:zone.find(':')]
            has_vehicle = zone[zone.find(':')+3: zone.find(' L')]
            boo_has_vehicle = bool(int(has_vehicle))
            if next_zone == key and not boo_has_vehicle and current_time < 3:
                reduce_zone = next_zone
                print(f"Reducing {reduce_zone} going time")
            if reduce_zone == zones[current_green_light]:
                print(f"Before reduce: {current_time}")
                current_time = int(current_time/2) 
                print(f"Current Time: {current_time}")
                reduce_zone = ""       
        client.publish("zone-response", f"Green Light: {zones[current_green_light]}: {current_time} sec remaining | next is {next_zone}")
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
