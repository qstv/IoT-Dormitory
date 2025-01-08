# Flask API 文件

## 簡介

這個 API 服務基於 Flask 框架構建，透過 MQTT 協議控制樹莓派，它接收來自用戶端的 HTTP 請求，並將指令轉發至 MQTT Broker，同時接收來自 MQTT Broker 的回覆，並回傳給用戶端。

## API 端點

### 1. 根目錄 (`/`)

* **方法：** `GET`
* **描述：** 返回 "Hello, World!" 字串，用於測試 API 是否正常運作。
* **請求：**
    ```
    GET https://<你的vercel網址>/
    ```
* **回應：**
    ```
    "Hello, World!"
    ```

### 2. 開啟大燈 (`/api/light/on`)

* **方法：** `POST`
* **描述：** 發送指令以開啟宿舍大燈。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/light/on
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Light/on"
    }
    ```

### 3. 關閉大燈 (`/api/light/off`)

* **方法：** `POST`
* **描述：** 發送指令以關閉宿舍大燈。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/light/off
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Light/off"
    }
    ```

### 4. 查詢溫濕度 (`/api/temperature-humidity`)

* **方法：** `GET`
* **描述：** 查詢宿舍的溫度和濕度。
* **請求：**
    ```
    GET https://<你的vercel網址>/api/temperature-humidity
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Temp/25.5/60.2"
    }
    ```

### 5. 開啟夜燈 (`/api/led/on`)

* **方法：** `POST`
* **描述：** 發送指令以開啟 LED 夜燈。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/led/on
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Led/on"
    }
    ```

### 6. 關閉夜燈 (`/api/led/off`)

* **方法：** `POST`
* **描述：** 發送指令以關閉 LED 夜燈。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/led/off
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Led/off"
    }
    ```

### 7. 開啟警報模式 (`/api/alert/on`)

* **方法：** `POST`
* **描述：** 發送指令以開啟警報模式。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/alert/on
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Alert/on"
    }
    ```

### 8. 關閉警報模式 (`/api/alert/off`)

* **方法：** `POST`
* **描述：** 發送指令以關閉警報模式。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/alert/off
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "Alert/off"
    }
    ```

### 9. 查詢目前狀態 (`/api/status`)

* **方法：** `GET`
* **描述：** 查詢系統的狀態，包含警報模式、夜燈模式、濕度通知、溫濕度等。
* **請求：**
    ```
    GET https://<你的vercel網址>/api/status
    ```
* **回應範例 (成功)：**
    ```json
    {
      "status": "success",
      "response": "{'警報模式': '關閉', '夜燈模式': '關閉', '濕度通知': '關閉', '濕度通知閾值': 80.0, '室內溫度': '25.5 °C', '室內溼度': '60.2 %', '夜燈': '關閉', '門': '關閉'}"
    }
    ```

### 10. 開啟濕度通知 (`/api/humidity-notify/on`)

* **方法：** `POST`
* **描述：** 發送指令以開啟濕度通知功能。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/humidity-notify/on
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "HumidityNotify/on"
    }
    ```

### 11. 關閉濕度通知 (`/api/humidity-notify/off`)

* **方法：** `POST`
* **描述：** 發送指令以關閉濕度通知功能。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/humidity-notify/off
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "HumidityNotify/off"
    }
    ```

### 12. 設定濕度通知閾值 (`/api/set/humidity/<humidity>`)

* **方法：** `POST`
* **描述：** 發送指令以設定濕度通知閾值。
* **路徑參數：**
    * `<humidity>`: 濕度閾值，必須是整數。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/set/humidity/75
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "ok! Humidity threshold set to 75"
    }
    ```
* **回應 (輸入值錯誤)：**
    ```json
    {
        "status": "success",
        "response": "Error: Invalid humidity value"
    }
    ```

### 13. 開啟感應夜燈模式 (`/api/night-light-mode/on`)

* **方法：** `POST`
* **描述：** 發送指令以開啟感應夜燈模式。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/night-light-mode/on
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "NightLightMode/on"
    }
    ```

### 14. 關閉感應夜燈模式 (`/api/night-light-mode/off`)

* **方法：** `POST`
* **描述：** 發送指令以關閉感應夜燈模式。
* **請求：**
    ```
    POST https://<你的vercel網址>/api/night-light-mode/off
    ```
* **回應 (成功)：**
    ```json
    {
        "status": "success",
        "response": "NightLightMode/off"
    }
    ```

## 錯誤回應

所有端點在發生**timeout**錯誤時都會回傳以下 JSON 格式的錯誤訊息：

```json
{
    "status": "timeout",
    "message": "No response received"
}
```

*   `status`: 錯誤狀態，例如："timeout"。
*   `message`: 錯誤訊息，例如："No response received"。