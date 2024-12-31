import RPi.GPIO as GPIO

# 開燈函式
def led_on():
    IN1 = 22  # GPIO 接 L298N 的 IN1
    IN2 = 27  # GPIO 接 L298N 的 IN2

    # GPIO 初始化
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.output(IN1, GPIO.HIGH)  
    GPIO.output(IN2, GPIO.LOW)  


# 關燈函式
def led_off():
    IN1 = 22  # GPIO 接 L298N 的 IN1
    IN2 = 27  # GPIO 接 L298N 的 IN2

    # GPIO 初始化
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.output(IN1, GPIO.LOW)   
    GPIO.output(IN2, GPIO.LOW)  


# 檢查燈狀態函式
def get_led_status():
    IN1 = 22  # GPIO 接 L298N 的 IN1
    IN2 = 27  # GPIO 接 L298N 的 IN2

    # 確保 GPIO 已初始化
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)

    # 讀取腳位狀態
    in1_status = GPIO.input(IN1)
    in2_status = GPIO.input(IN2)

    if in1_status == GPIO.HIGH and in2_status == GPIO.LOW:
        return "ON"
    elif in1_status == GPIO.LOW and in2_status == GPIO.LOW:
        return "OFF"
    else:
        return "UNKNOWN"


if __name__ == "__main__":
    led_on()
    print("LED Status:", get_led_status())  # 應該輸出 "ON"
    led_off()
    print("LED Status:", get_led_status())  # 應該輸出 "OFF"