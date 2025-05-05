import network,ujson
from time import sleep
from umqtt.simple import MQTTClient

# Replace these values with your own


def kubiosconnecton(data):
    global msg
    json={"id":223,"type":"RRI","data":data,"analysis":{"type":"readiness"}}
    answer="Nan"
    json=ujson.dumps(json)
    #Connect to WLAN
    netti=connect_wlan()
    # Connect to MQTT
    if not netti:
        return False
    try:
        mqtt_client=connect_mqtt()
    except Exception as e:
        print(f"Failed to connect to MQTT: {e}")
        
    mqtt_client.set_callback(callbackfunction)
    
    topic = "kubios-request"
    massage = json
    mqtt_client.publish(topic, json)
    mqtt_client.subscribe("kubios-response")
    data = None
    mqtt_client.wait_msg()
    msg=parse_json(msg)
    return msg

def parse_json(list):
    return [list["data"]["analysis"]["mean_hr_bpm"],list["data"]["analysis"]["mean_rr_ms"],list["data"]["analysis"]["rmssd_ms"],list["data"]["analysis"]["sdnn_ms"],list["data"]["analysis"]["sns_index"],list["data"]["analysis"]["pns_index"],list["data"]["analysis"]["physiological_age"]]
    
def callbackfunction(topic,message):
    global msg
    msg = ujson.loads(message)

def connect_wlan():
    x=10
    # Connecting to the group WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect("KMD657_Group_2", "6yhm2EHS@1")
    # Attempt to connect once per second
    while wlan.isconnected() == False and x!=10:
        wlan.connect("KMD657_Group_2", "6yhm2EHS@1")
        print("Connecting... ")
        sleep(10)
        x+=1
    # Print the IP address of the Pico
    if wlan.isconnected():
        print("Connection successful. Pico IP:", wlan.ifconfig()[0])
        return True
    else:
        print("connection not success")
        return False
        
def connect_mqtt():
        mqtt_client=MQTTClient("", "192.168.2.253",port=21883)
        mqtt_client.connect(clean_session=True)
        return mqtt_client
#list=kubiosconnecton([800,750,700,900,950,888,777,999,666,878,800,750,700,900,950,888,777,999,666,878,800,750,700,900,950,888,777,999,666,878])

print()