from confluent_kafka import Producer
import socket
import json
from time import sleep
from random import randint

TOPIC = "energy_generator" # Put the name of your topic here.

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: {}: {}".format(str(msg), str(err)))
    else:
        print("Message produced: {}\t{}".format(str(msg.key()),str(msg.value())))

conf = {'bootstrap.servers': "localhost:9092",
        'client.id': socket.gethostname()}

producer = Producer(conf)

try:
    while True:
        record_key = "energy_generator"
        record_value = json.dumps({'value': randint(20,2000)})
        print("Producing record: {}\t{}".format(record_key, str(json.loads(record_value)['value'])))
        #p.produce(topic, , on_delivery=acked)
        producer.produce(topic=TOPIC, key=record_key, value=record_value, callback=acked)
        # Wait up to 1 second for events. Callbacks will be invoked during
        # this method call if the message is acknowledged.
        producer.poll(1)
        sleep(1)
except KeyboardInterrupt:
    print("Done!")
