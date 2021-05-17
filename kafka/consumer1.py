from confluent_kafka import Consumer, KafkaException
import json
import time
import requests

#############################################################################
# For Ubidots:
TOKEN = "BBFF-SPONj6AlHG36Okio1VdmISf9jX55G2"  # Put your TOKEN here
DEVICE_LABEL = "KAFKA-BLUBU"  # Put your device label here
rl = "light_status"  # Put your first variable label here
eg = "energy_generator"
woe = "weight_on_elevator"

def build_payload(variable_1, value_1):
    payload = {variable_1: value_1}
    return payload

def post_request(payload, device_label, token):
    # Creates the headers for the HTTP requests
    url = "http://industrial.api.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, device_label)
    headers = {"X-Auth-Token": token, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True

#############################################################################
# For Kafka:
conf = {'bootstrap.servers': "localhost:9092",
        'group.id': "foo",
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)

def msg_process(msg):
    data = json.loads(msg.value())
    #print("{}\t{}".format(str(msg.key()),data["value"]))
    print("{}\t{}".format(str(msg.key()),str(msg.value())))
    if rl in str(msg.key()):
        post_request(build_payload(rl,json.loads(msg.value())['value']),DEVICE_LABEL,TOKEN)
    if eg in str(msg.key()):
        post_request(build_payload(eg,json.loads(msg.value())['value']),DEVICE_LABEL,TOKEN)
    if woe in str(msg.key()):
        post_request(build_payload(woe,json.loads(msg.value())['value']),DEVICE_LABEL,TOKEN)





def basic_consume_loop(consumer, topics):
    while True:
        try:
            consumer.subscribe(topics)
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else: 
                msg_process(msg)

        except KeyboardInterrupt:
            consumer.close()

basic_consume_loop(consumer, [woe, eg, rl]) # Put the name of your topics here.
