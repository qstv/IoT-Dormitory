from flask import Flask, request, jsonify
import threading
import uuid
import os
import time
import paho.mqtt.client as paho
from paho import mqtt

# MQTT 設定
MQTT_TOPIC_COMMAND = "iot/API"  # 發送指令的主題
MQTT_TOPIC_RESPONSE = "iot/pi"  # 接收回應的主題
MQTT_BROKER_URL = os.environ['CLUSTER_URL']
MQTT_BROKER_PORT = int(os.environ['BROKER_PORT'])
MQTT_USERNAME = os.environ['USERNAME']
MQTT_PASSWORD = os.environ['PASSWORD']

# 全域變數
pending_requests = {}  # 存放等待回應的請求，格式：{correlation_id: {"event": Event, "response": str}}

# MQTT 回呼函數
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"CONNACK received with code {rc}")
    if rc == 0:
        print("Connected successfully")
        client.subscribe(MQTT_TOPIC_RESPONSE, qos=1)
    else:
        print("Connection failed")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message: {payload}")

    try:
        correlation_id, response_message = payload.split(":", 1)
    except ValueError:
        print("Invalid message format")
        return

    # 查找對應的請求
    if correlation_id in pending_requests:
        pending_requests[correlation_id]["response"] = response_message
        pending_requests[correlation_id]["event"].set()  # 通知主線程

# 初始化 MQTT 客戶端
client = paho.Client()
client.on_connect = on_connect
client.on_message = on_message

# 啟用 TLS 並設置認證
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.connect(MQTT_BROKER_URL, MQTT_BROKER_PORT, keepalive=60)

# 啟動 MQTT 客戶端執行緒
client.loop_start()

# Flask 應用程式
app = Flask(__name__)
@app.route('/', methods=['GET'])
def index():
    return "Hello, World!"

@app.route('/api/light/on', methods=['POST'])
def light_on():
    return handle_mqtt_command("LightOn")

@app.route('/api/light/off', methods=['POST'])
def light_off():
    return handle_mqtt_command("LightOff")

@app.route('/api/temperature-humidity', methods=['GET'])
def temperature_humidity():
    return handle_mqtt_command("Temp")

@app.route('/api/led/on', methods=['POST'])
def led_on():
    return handle_mqtt_command("LedOn")

@app.route('/api/led/off', methods=['POST'])
def led_off():
    return handle_mqtt_command("LedOff")

@app.route('/api/alert/on', methods=['POST'])
def alert_on():
    return handle_mqtt_command("AlertOn")

@app.route('/api/alert/off', methods=['POST'])
def alert_off():
    return handle_mqtt_command("AlertOff")

@app.route('/api/status', methods=['GET'])
def status():
    return handle_mqtt_command("Status")

@app.route('/api/humidity-notify/on', methods=['POST'])
def humidity_notify_on():
    return handle_mqtt_command("HumidityNotifyOn")

@app.route('/api/humidity-notify/off', methods=['POST'])
def humidity_notify_off():
    return handle_mqtt_command("HumidityNotifyOff")

@app.route('/api/set/humidity/<humidity>', methods=['POST'])
def set_humidity(humidity):
    return handle_mqtt_command(f"Set/humidity/{humidity}")

@app.route('/api/night-light-mode/on', methods=['POST'])
def night_light_on():
    return handle_mqtt_command("NightLightModeOn")

@app.route('/api/night-light-mode/off', methods=['POST'])
def night_light_off():
    return handle_mqtt_command("NightLightModeOff")




def handle_mqtt_command(command):
    # 為此請求生成唯一識別碼
    correlation_id = str(uuid.uuid4())
    event = threading.Event()
    pending_requests[correlation_id] = {"event": event, "response": None}

    # 發送指令到 MQTT，附加識別碼
    client.publish(MQTT_TOPIC_COMMAND, payload=f"{correlation_id}:{command}", qos=1)

    # 等待回應，最多等待 8 秒
    if event.wait(timeout=8):
        response = pending_requests[correlation_id]["response"]
        del pending_requests[correlation_id]  # 清理已完成的請求
        return jsonify({"status": "success", "response": response})
    else:
        del pending_requests[correlation_id]  # 清理已超時的請求
        return jsonify({"status": "timeout", "message": "No response received"}), 504

if __name__ == "__main__":
    app.run()
