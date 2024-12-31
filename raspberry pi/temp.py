import adafruit_dht
import board


def get_temp():

    dht_device = adafruit_dht.DHT22(board.D10, use_pulseio=False)
    # 不斷獲取資料直到抓到數值
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
            if temperature is not None and humidity is not None:
                return (temperature, humidity)
        except RuntimeError as error:
            pass
if __name__ == "__main__":
    print(get_temp())

