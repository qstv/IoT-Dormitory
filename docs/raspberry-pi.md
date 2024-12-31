# Raspberry pi 相關程式說明

## 概述 
[[跳到安裝步驟](#安裝步驟)]

透過 MQTT 協議進行通訊，並能將事件通知發送到 Discord。

*   **霍爾感測器**: 偵測門的開啟狀態，觸發警報。
*   **溫濕度感測器**: 監測環境的溫濕度，並在濕度通知模式下，濕度過高時發出通知。
*   **PIR 人體紅外線感測器**: 在夜燈模式下偵測人體移動，自動開啟或關閉 LED 燈。
*   **蜂鳴器**: 在警報模式下發出聲音警報。
*   **伺服馬達**: 控制燈的開關。
*   **LED 燈**: 作為夜燈。
*   **攝影機**: 拍攝照片並上傳至 GitHub，同時將圖片網址發送到 Discord。
*   **MQTT 通訊**: 接收指令並發送狀態回報。
*   **Discord 通知**: 發送警報訊息、圖片和濕度通知。

## 檔案說明

以下此部分各個 Python 檔案的功能說明：

1.  **`buzzer.py`**:
    *   **功能**: 控制蜂鳴器發出不同頻率的聲音，用於警報或提示。
    *   **主要函式**:
        *   `play_tone(buzzer, frequency, duration)`: 播放指定頻率和持續時間的音調。
        *   `buzzer_alert()`: 播放警報音。
        *   `buzzer_notify1()`: 播放提示音 1。
        *   `buzzer_notify2()`: 播放提示音 2。
    *   **說明**: 使用 `RPi.GPIO` 庫來控制 GPIO 腳位，產生 PWM 訊號以驅動蜂鳴器。

2.  **`camera.py`**:
    *   **功能**: 使用樹莓派攝影機拍攝照片。
    *   **主要函式**:
        *   `take_photo(file_path='photo.jpg', resolution=(1024, 768))`: 拍攝照片並儲存到指定路徑。
    *   **說明**: 使用 `picamera` 庫來控制攝影機，可以設定照片的解析度。

3.  **`door.py`**:
    *   **功能**: 偵測門的狀態。
    *   **主要函式**:
        *   `door_detected()`: 偵測門的狀態，回傳 `True` (門關閉) 或 `False` (門開啟)。
    *   **說明**: 使用 `RPi.GPIO` 庫來讀取 GPIO 腳位的輸入，判斷是否有磁場。

4.  **`get_image_url.py`**:
    *   **功能**: 將照片上傳到 GitHub 並獲取圖片的原始 URL。
    *   **主要函式**:
        *   `upload_to_github(image_data)`: 上傳圖片到 GitHub，並返回圖片的原始 URL。
    *   **說明**: 使用 `requests` 庫與 GitHub API 互動，需要設定 GitHub Repository名稱和存取權杖。

5.  **`main.py`**:
    *   **功能**: 主程式，整合所有功能，處理 MQTT 通訊，執行背景執行緒。
    *   **主要功能**:
        *   設定 MQTT 客戶端，處理連線、訂閱和訊息。
        *   啟動背景執行緒，監控警報、濕度以及 PIR 感測器。
        *   處理接收到的 MQTT 指令，控制設備的開關、設定模式。
        *   回傳溫濕度數據和系統狀態。
    *   **說明**: 使用 `paho-mqtt` 庫進行 MQTT 通訊，並使用 `threading` 庫建立多執行緒。

6.  **`led.py`**:
    *   **功能**: 控制 LED 燈的開關。
    *   **主要函式**:
        *   `led_on()`: 開啟 LED 燈。
        *   `led_off()`: 關閉 LED 燈。
		*   `get_led_status()`: 讀取 LED 燈的狀態。
    *   **說明**: 使用 `RPi.GPIO` 庫來控制 GPIO 腳位，驅動 LED 燈。

7.  **`pir_sensor_led.py`**:
    *   **功能**: 偵測人體移動，並根據夜燈模式控制 LED 燈的開關。
    *   **主要函式**:
        *   `run_pir_sensor(pin, night_light_event)`: 啟動 PIR 感測器監測。
    *   **說明**: 使用 `gpiozero` 庫來監測 PIR 感測器的狀態，並根據 `night_light_event` 來決定是否開啟/關閉 LED 燈。

8.  **`servo.py`**:
    *   **功能**: 控制伺服馬達轉動到指定角度。
    *   **主要函式**:
        *   `servo_motor(pin)`: 控制伺服馬達。
    *   **說明**: 使用 `RPi.GPIO` 庫來控制 PWM 訊號，驅動伺服馬達。

9.  **`temp.py`**:
    *   **功能**: 讀取 DHT22 溫濕度感測器的數據。
    *   **主要函式**:
        *   `get_temp()`: 讀取並返回溫度和濕度數據。
    *   **說明**: 使用 `adafruit_dht` 庫來讀取溫濕度數據。

10. **`send_to_discord.py`**:
    *   **功能**: 發送訊息到 Discord 頻道。
    *   **主要函式**:
        *   `send_message(webhook_url, content, username="", avatar_url="", embed=None, image_url=None)`: 發送訊息到 Discord。
    *   **說明**: 使用 `requests` 庫向 Discord webhook 發送 HTTP POST 請求。

## 安裝步驟

1.  **安裝 Raspberry Pi OS**: 在您的 Raspberry Pi 上安裝此[作業系統](https://drive.google.com/file/d/1p2kfjPk8NvDR2WBNdOTHHJzF7M0_ilpD/view)
2.  **使用RealVNC操作**: 操作說明請參考影片[Connecting to Raspberry Pi with RealVNC](https://www.youtube.com/watch?v=8bwbbG1mCzs)
3.  **安裝 Python 函式庫**: 開啟終端機，輸入以下指令安裝所需的 Python 函式庫：
    ```bash
    sudo apt update
    sudo apt install python3-pip
    pip3 install paho-mqtt picamera requests gpiozero adafruit-circuitpython-dht
    ```
4.  **複製程式碼**: 將 raspberry pi 資料夾中所有 `.py` 檔案複製到你的樹莓派上。
5.  **設定 GitHub 存取權杖**: 修改 `get_image_url.py` 檔案，選一個用來當圖床的GitHub Repository，填入你的 GitHub Repository名稱和存取權杖。如果不知道如何取得可以[點此](https://www.youtube.com/watch?v=ZQspooxvaHc&t=218s)查看教學。

    ```python
    repo_name = "YOUR_REPO_NAME"  # 替換為你的Repository名稱
    token = "YOUR_GITHUB_TOKEN" # 替換為你的 GitHub 存取權杖
    ```
6. **設定 Discord Webhook URL**: 修改 `send_to_discord.py` 和 `main.py` 檔案，填入你的 Discord Webhook URL。如果不知道如何取得可以[點此](https://www.youtube.com/watch?v=6m6YmRUaWBM)查看教學。
    ```python
    WEBHOOK_URL ="your_discord_WEBHOOK_URL_here"
    ```
7. **設定 MQTT 憑證**: 修改 `main.py` 檔案，填入你的 MQTT 伺服器位址、使用者名稱和密碼。

    查看MQTT 伺服器URL, PORT
    ![MQTT 伺服器位址](/docs/mqtt1.png)

    建立一個使用者
    ![使用者名稱和密碼](/docs/mqtt2.png)



    填入你的
     ```python
    # Set username and password
    client.username_pw_set("Your_MQTT_USERNAME", "Your_MQTT_PASSWORD")
    # Connect to HiveMQ Cloud on port 8883
    client.connect("Your_MQTT_BROKER_URL", 8883)
     ```


## 如何使用

1.  **執行程式**: 開啟終端機，切換到你的程式碼目錄，執行以下指令啟動程式：
    ```bash
    python3 main.py
    ```


## 注意事項

*   請確保你的樹莓派已正確連接所有元件。
*   請確保你已設定好 GitHub 存取權杖，並有權限將圖片上傳到你的Repository。
*   請確保你已設定好 Discord Webhook URL。
*   請確保你的 MQTT 伺服器位址、使用者名稱和密碼設定正確。
*   可以根據需求調整程式碼中的預設常數，例如：警報間隔、濕度閾值等。

[[返回主文件](../README.md#快速開始)]

