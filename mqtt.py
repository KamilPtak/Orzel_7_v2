import paho.mqtt.client as paho
import logger

Logging = logger.Logger()

broker = "127.0.0.1"
port = 1883

def on_message(client, userdata, msg):
    if msg.topic == "robot/pid":
        # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        Logging.pid_call(msg.payload.decode())
    elif msg.topic == "robot/currnet":
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        Logging.current_call_call(msg.payload.decode())

def on_publish(client,userdata,result):
    pass

def on_connect(client,userdata,result, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

client1 = paho.Client("control1")
client1.on_publish = on_publish
client1.on_connect = on_connect
client1.on_message = on_message

client1.connect(broker, port, keepalive=60, bind_address="")

def subscibe():
    client1.subscribe("robot/pid")
    client1.loop_forever()

def publish(topic, msg):
    ret = client1.publish(topic,msg)
    if ret[0] == 0:
        print(f"Data published: {msg}, with exit code: {ret[0]}")
    else:
        print("Failed to publish data")
        print("Trying to reconnect to broker...")
        client1.connect(broker, port, keepalive=60, bind_address="")
