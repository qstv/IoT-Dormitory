import RPi.GPIO as GPIO

def door_detected():
    """
    :return: True (磁場存在，門關閉), False (無磁場，門開啟)
    """
    # 設定 GPIO 腳位
    digitalPin = 23  

    # GPIO 初始化
    GPIO.setmode(GPIO.BCM)          
    GPIO.setup(digitalPin, GPIO.IN)  

    # 讀取數位訊號
    digitalVal = GPIO.input(digitalPin)

    # 判斷磁場狀態
    if digitalVal == GPIO.HIGH:  # 當模組輸出 HIGH 表示檢測到磁場
        return True
    else:
        return False
    
if __name__ == "__main__":
    print(door_detected())
    
