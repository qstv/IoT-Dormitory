import paho.mqtt.client as paho
from paho import mqtt
import os
import RPi.GPIO as GPIO
import threading
import time
from servo import *
from led import *
from door import *
from buzzer import *
from temp import *
from send_to_discord import *
from camera import *
from get_image_url import *
from pir_sensor_led import run_pir_sensor


# Configuration Constants
ALERT_MODE = False
Captured = False
NIGHT_LIGHT_MODE = False
last_alert_time = 0
HUMIDITY_NOTIFY = False
HUMIDITY_THRESHOLD = 80.0
ALERT_INTERVAL = 600 # 濕度通知間隔設為600秒(10 分鐘)
WEBHOOK_URL ="your_discord_WEBHOOK_URL_here"


night_light_event = threading.Event()


# Background Threads
def alert_monitor():
    global Captured
    while True:
        if ALERT_MODE and not door_detected():
            buzzer_alert()
            handle_photo_and_upload()
        else:
            Captured = False
        time.sleep(0.1)

def humidity_monitor():
    global last_alert_time
    while True:
        if HUMIDITY_NOTIFY:
            data = get_temp()
            if data is not None:
                humidity = data[1]
                if humidity > HUMIDITY_THRESHOLD:
                    current_time = time.time()
                    if current_time - last_alert_time > ALERT_INTERVAL:
                        send_message(WEBHOOK_URL, f"[通知]目前濕度為{humidity}，請注意!")
                        last_alert_time = current_time
        time.sleep(1)

def handle_photo_and_upload():
    global Captured
    if not Captured:
        Captured = True
        photo_thread = threading.Thread(target=take_photo)
        photo_thread.start()
        photo_thread.join()
        with open("photo.jpg", "rb") as image_file:
            image_data = image_file.read()
        upload_thread = threading.Thread(target=upload_and_notify, args=(image_data,))
        upload_thread.start()


def upload_and_notify(image_data):
    raw_url = upload_to_github(image_data)
    send_message(
        WEBHOOK_URL,
        "",
        embed={
            "title": "警報模式",
            "description": "倒楣鬼拍了一張照片",
            "color": 16711680,
        },
        image_url=raw_url
    )





# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"CONNACK received with code {rc}")
    if rc != 0:
        print("Connection failed. Trying to reconnect...")

def on_publish(client, userdata, mid, properties=None):
    print(f"mid: {mid}")

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print(f"Subscribed: {mid} {granted_qos}")

def on_message(client, userdata, msg):
    message = msg.payload.decode()
    global HUMIDITY_THRESHOLD

    try:
        correlation_id, command = message.split(":", 1)
    except ValueError:
        print("Invalid message format")
        return

    actions = {
        "LightOn": lambda: (servo_motor(17), client.publish("iot/pi", payload=f"{correlation_id}:Light/on", qos=1)),
        "LightOff": lambda: (servo_motor(18), client.publish("iot/pi", payload=f"{correlation_id}:Light/off", qos=1)),
        "LedOn": lambda: (led_on(), client.publish("iot/pi", payload=f"{correlation_id}:Led/on", qos=1)),
        "LedOff": lambda: (led_off(), client.publish("iot/pi", payload=f"{correlation_id}:Led/off", qos=1)),
        "AlertOn": lambda: (set_alert_mode(True), client.publish("iot/pi", payload=f"{correlation_id}:Alert/on", qos=1)),
        "AlertOff": lambda: (set_alert_mode(False), client.publish("iot/pi", payload=f"{correlation_id}:Alert/off", qos=1)),
        "Temp": lambda: handle_temp(correlation_id),
        "HumidityNotifyOn": lambda: (set_humidity_notify(True), client.publish("iot/pi", payload=f"{correlation_id}:HumidityNotify/on", qos=1)),
        "HumidityNotifyOff": lambda: (set_humidity_notify(False), client.publish("iot/pi", payload=f"{correlation_id}:HumidityNotify/off", qos=1)),
        "NightLightModeOn": lambda: (set_night_light_mode(True), client.publish("iot/pi", payload=f"{correlation_id}:NightLightMode/on", qos=1)),
        "NightLightModeOff": lambda: (set_night_light_mode(False), client.publish("iot/pi", payload=f"{correlation_id}:NightLightMode/off", qos=1)),
        "Status": lambda: client.publish("iot/pi", payload=f"{correlation_id}:{str(get_status())}", qos=1),
    }

    try:
        if command in actions:
            actions[command]()
        elif command.startswith("Set/humidity/"):
            try:
                HUMIDITY_THRESHOLD = int(command.split("/")[-1])
                client.publish("iot/pi", payload=f"{correlation_id}:ok! Humidity threshold set to {HUMIDITY_THRESHOLD}", qos=1)
            except ValueError:
                client.publish("iot/pi", payload=f"{correlation_id}:Error: Invalid humidity value", qos=1)
    except Exception as e:
        print(f"Error handling message '{message}': {e}")
        client.publish("iot/pi", payload=f"{correlation_id}:Error: Command execution failed", qos=1)


# 回傳溫度/濕度資料
def handle_temp(correlation_id):
    data = get_temp()
    client.publish("iot/pi", payload=f"{correlation_id}:Temp/{data[0]}/{data[1]}", qos=1)

def get_status():
    data = get_temp()
    led_status = get_led_status()

    led_status_translation = {
        "ON": "開啟",
        "OFF": "關閉",
        "UNKNOWN": "未知"  
    }
    
    
    led_status_chinese = led_status_translation.get(led_status)
    return {
        "警報模式": "開啟" if ALERT_MODE else "關閉",
        "夜燈模式": "開啟" if NIGHT_LIGHT_MODE else "關閉",
        "濕度通知": "開啟" if HUMIDITY_NOTIFY else "關閉",
        "濕度通知閾值": HUMIDITY_THRESHOLD,
        "室內溫度": f"{data[0]} °C",
        "室內溼度": f"{data[1]} %",
        "夜燈": led_status_chinese,
        "門": "開啟" if not door_detected() else "關閉",
    }


# 模式設定
def set_alert_mode(state):
    global ALERT_MODE
    ALERT_MODE = state
    if state:
        buzzer_notify1()
    else:
        buzzer_notify2()

def set_humidity_notify(state):
    global HUMIDITY_NOTIFY
    HUMIDITY_NOTIFY = state

def set_night_light_mode(state):
    global NIGHT_LIGHT_MODE
    if state:
        night_light_event.set()
    else:
        night_light_event.clear()
    NIGHT_LIGHT_MODE = state


# MQTT Client Setup
client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish

# Enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# Set username and password
client.username_pw_set("Your_MQTT_USERNAME", "Your_MQTT_PASSWORD")

# Connect to HiveMQ Cloud on port 8883
client.connect("Your_MQTT_BROKER_URL", 8883)

# Subscribe to topics
client.subscribe("iot/API", qos=1)

# Publish initial message
client.publish("iot/pi", payload="raspberry pi: hello", qos=1)

# Start MQTT loop
client.loop_start()

# Start background threads
alert_thread = threading.Thread(target=alert_monitor, daemon=True)
alert_thread.start()
humidity_thread = threading.Thread(target=humidity_monitor, daemon=True)
humidity_thread.start()
pir_thread = threading.Thread(target=run_pir_sensor, args=(16, night_light_event), daemon=True)
pir_thread.start()


# Main Loop
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Disconnected")
    GPIO.cleanup()
    client.loop_stop()
    client.disconnect()

