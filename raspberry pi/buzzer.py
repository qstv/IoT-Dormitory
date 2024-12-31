import RPi.GPIO as GPIO
import time


# 設置音階的頻率（Hz）
tones = {
    'C': 523.3,
    'D': 587.4,
    'E': 659.4,
    'F': 698.7,
    'G': 784.3,
    'A': 880,
    'B': 987.8,
    'C_high': 1046.5
}



"""初始化蜂鳴器"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)
buzzer = GPIO.PWM(21, 1) 

def play_tone(buzzer, frequency, duration):
    """播放指定頻率的音調"""
    buzzer.ChangeFrequency(frequency)
    buzzer.start(50)  
    time.sleep(duration)
    buzzer.stop()


def buzzer_alert():
    """蜂鳴器警報音"""
    try:

        alert_sequence = [('C', 0.2), ('G', 0.2), ('C', 0.2), ('G', 0.2) ]

        for _ in range(3): 
            for note, duration in alert_sequence:
                if note in tones:
                    play_tone(buzzer, tones[note], duration)
                else:
                    time.sleep(duration)

    except:
        print("buzzer alert error")

def buzzer_notify1():
    """提示音1"""
    
    try:
        sound_sequence = [('C', 0.2), ('D', 0.2), ('E', 0.2)]
        

        for note, duration in sound_sequence:
            if note in tones:
                play_tone(buzzer, tones[note], duration)
            else:
                time.sleep(duration)

    except:
        print("buzzer alert error")
        
def buzzer_notify2():
    """提示音2"""
    
    try:
        sound_sequence = [('E', 0.2), ('D', 0.2), ('C', 0.2)]
        

        for note, duration in sound_sequence:
            if note in tones:
                play_tone(buzzer, tones[note], duration)
            else:
                time.sleep(duration)

    except:
        print("buzzer alert error")


if __name__ == "__main__":
    buzzer_alert()
    buzzer_notify2()

