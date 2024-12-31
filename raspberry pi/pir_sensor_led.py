from gpiozero import MotionSensor
from signal import pause
from led import *
from datetime import datetime
import threading


def run_pir_sensor(pin, night_light_event):
    pir = MotionSensor(pin)

    def motion_detected():
        if night_light_event.is_set():
            print("偵測到人體移動！")
            led_on()

    def motion_stopped():
        if night_light_event.is_set():
            print("人體移動停止！")
            led_off()

    pir.when_motion = motion_detected
    pir.when_no_motion = motion_stopped

    print("PIR 感應器已啟動，正在等待訊號...")
    pause()
