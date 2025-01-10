# IoT-Dormitory 智慧宿舍物聯網系統

## 專案簡介

在宿舍房間裡，我們常常幻想能舒舒服服地坐在座位或躺在床上，就輕鬆控制電燈，特別是當大家已經爬上床滑著手機，準備入睡的時候，最痛苦的莫過於決定某個倒楣鬼下床關燈的時刻。本專案致力於打造一個舒適的物聯網宿舍，一切都可以用手機、聲控或設定自動化來達成，使用 Raspberry Pi、多種感測器、 MQTT、Flask API，透過  Discord 機器人、Siri shortcuts 等方式進行控制。

> 可以先看看 [DEMO](https://youtu.be/jn-hajnLU68) 影片。


## 目錄

1.  [功能簡介](#功能簡介)
2.  [快速開始](#快速開始)
    * [Raspberry Pi 相關程式說明](/docs/raspberry-pi.md)
    * [使用 Vercel 部署 Flask API 說明文件](/docs/Vercel.md)
    * [本地端相關程式碼說明文件](/docs/local.md)
3.  [檔案結構](#檔案結構)
4.  [硬體元件](#硬體元件)
5.  [電路接法](#電路接法)
6.  [電路實際照片](#電路實際照片)
7.  [整體裝置樣貌](#整體裝置樣貌)
8.  [DEMO影片](#demo影片)
9.  [Siri 與 自動化](#siri-與-自動化)
10. [參考資料](#參考資料)

## 功能簡介

這個智慧宿舍系統具備以下功能：

1.  **遠端控制宿舍大燈：** 透過Discord、Siri 或 自動化控制宿舍大燈的開關。
2.  **遠端讀取宿舍溫濕度：** 隨時查詢宿舍的溫度和濕度。
3.  **遠端控制 LED 夜燈：** 過Discord、Siri 或 自動化控制夜燈的開關。
4.  **警報模式：** 在偵測到異常狀況時（例如門被打開），發出警報並發送通知。
5.  **查詢宿舍與模式狀態：** 隨時查詢宿舍溫溼度、門、夜燈等狀態和各模式的開關狀態。
6.  **濕度監控通知：** 當濕度超過設定值時，自動發送通知到Discord。
7.  **感應夜燈模式：** 在偵測到人體移動時，自動開啟夜燈。
8.  **智慧鬧鐘：** 可以根據手機鬧鐘時間自動開啟宿舍大燈。
9.  **遠端控制宿舍天花板電風扇：** 透過Discord控制電風扇的開關。
10. **其他自訂的自動化操作：** 透過參考 [API 文件](/docs/API.md) ，可以根據需求自訂其他自動化操作。

## 快速開始

立刻開始打造您的物聯網宿舍！

### 第一步

1.  **準備硬體：** 確認您已備妥所有 [硬體元件](#硬體元件)。
2.  **連接電路：** 依照 [電路接法](#電路接法) 的指示，仔細地將各個感測器和致動器連接到 Raspberry Pi 和麵包板。
3.  **註冊 HiveMQ：** HiveMQ Cloud 是一個基於雲端的 MQTT 訊息代理服務，這是樹莓派跟 Flask API 之間通訊的橋樑。請前往 [HiveMQ Cloud](https://www.hivemq.com/) 註冊，註冊後請先**建立**一個Cluster。
4.  **其他相關服務：** 確保您擁有以下網站帳號：
    *   [Discord](https://discord.com/)
    *   [Github](https://github.com/)
    *   [Vercel](https://vercel.com/)

### 第二步
1.  **Raspberry Pi 設定：** 首先，依照 [Raspberry Pi 相關程式說明](/docs/raspberry-pi.md) 完成安裝及設定，確保所有硬體元件都可以正常運作及控制。
2.  **Vercel 設定：** 接著，依照 [使用 Vercel 部署 Flask API 說明文件](/docs/Vercel.md) 完成部署及設定。
3.  **本地端設定：** 最後，依照 [本地端相關程式碼說明文件](/docs/local.md) 的說明，建立一個 Discord 機器人。

### 第三步

**恭喜！** 您已完成物聯網宿舍系統的設定，現在可以用 Discord 開始享受智慧化的宿舍生活了！除此之外，還可以發揮創意，或是根據自身需求設定更加有趣的玩法，可以查看 [siri與自動化](#siri-與-自動化) 章節。

> [!caution]
請務必妥善保管你的 Discord 機器人 Token、 Discord Webhook URL 、 GitHub Token、MQTT 連線憑證 、 Flask API URL等敏感資訊，避免洩漏在公開場合。

## 檔案結構

本專案的程式碼主要分為以下三個資料夾：

*   **`local/`：**  這個資料夾放著在本地端運行的 Discord 機器人與紅外線設定相關的檔案。
*   **`raspberry pi/`：** 這個資料夾包含了運行在 Raspberry Pi 上的主要程式碼和相關模組，用於控制硬體元件和 MQTT 通訊。
*   **`Vercel/`：** 這個資料夾包含了部署到 Vercel 平台的 Flask API 相關程式碼，作為控制中樞。

## 硬體元件

[[返回快速開始](#快速開始)]
*   Raspberry Pi 4 *1
*   6V 電池組 *1
*   5V LED 燈條 *1
*   蜂鳴器 *1
*   杜邦線 *依照需求
*   DHT22 溫濕度模組 *1
*   攝影鏡頭 *1
*   伺服馬達 SG90 *2
*   紅外線運動感測器 *1
*   線性霍爾磁力感測模組 *1
*   磁鐵 *1
*   小米萬能遙控器 *1
*   L298N 馬達控制板 *1
*   麵包板 *1
*   瓦楞板 *依照需求


## 電路接法
[[返回快速開始](#快速開始)]
> [!NOTE]
> 請善用麵包板將電路正確連接至以下所指示的 Raspberry Pi 腳位。

1.  **兩個伺服馬達 (Servo Motors):**
    *   紅線接 Raspberry Pi 的 `5V` 腳位。
    *   棕線接 Raspberry Pi 的 `GND` 腳位。
    *   作為 **開燈** 使用的橘線接 Raspberry Pi 的 `GPIO 17`。
    *   作為 **關燈** 使用的橘線接 Raspberry Pi 的 `GPIO 18`。

2.  **L298N 馬達控制模組 (Motor Control Module):**
    *   `OUT1` 和 `OUT2` 接 5V LED 燈條的正負極。
    *   `IN1` 接 Raspberry Pi 的 `GPIO 22`。
    *   `IN2` 接 Raspberry Pi 的 `GPIO 27`。
    *   `VCC` 接 6V 電池組的正極。
    *   `GND` 接 6V 電池組的負極。

3.  **線性霍爾磁力感測模組 (Hall Effect Sensor):**
    *   將模組的 `VCC` 接 Raspberry Pi 的 `3.3V` 腳位。
    *   將模組的 `GND` 接 Raspberry Pi 的 `GND` 腳位。
    *   將模組的 `D0` (數位訊號) 接 Raspberry Pi 的 `GPIO 23`。

4.  **無源蜂鳴器(沒有HSD字樣)(Passive Buzzer):**
    *   正極接 Raspberry Pi 的 `GPIO 21`。
    *   負極接 Raspberry Pi 的 `GND` 腳位。

5.  **DHT22 溫濕度感應器 (Temperature/Humidity Sensor):**
    *   `VCC` 接 Raspberry Pi 的 `3.3V` 腳位。
    *   `GND` 接 Raspberry Pi 的 `GND` 腳位。
    *   `DAT` 接 Raspberry Pi 的 `GPIO 2`。

6.  **攝影鏡頭 (Camera Module):**
    *   將攝影鏡頭的排線小心地插入 Raspberry Pi 上專為鏡頭設計的排線槽。

7.  **紅外線運動感測器 (PIR Motion Sensor):**
    *   `VCC` 接 Raspberry Pi 的 `5V` 腳位。
    *   `GND` 接 Raspberry Pi 的 `GND` 腳位。
    *   `OUT` 接 Raspberry Pi 的 `GPIO 16`。

## 電路實際照片
<p align="center">
    <img src="/docs/實際電路接法1.jpg" alt="電路實際照片1" width="500">
</p>
<p align="center">
    <img src="/docs/實際電路接法2.jpg" alt="電路實際照片2" width="500">
</p>

## 整體裝置樣貌

![整體裝置樣貌](/docs/裝置.jpg)
![三張照片](/docs/三張照片.png)


## DEMO影片
YouTube : [IoT Dormitory Project Demo](https://youtu.be/jn-hajnLU68)

[![IoT Dormitory Project Demo](https://img.youtube.com/vi/jn-hajnLU68/0.jpg)](https://youtu.be/jn-hajnLU68)

## Siri 與 自動化
「捷徑」(Shortcuts) 是 Apple 在 iOS、iPadOS 和 macOS 系統中內建的一款強大的自動化工具，它允許用戶將多個步驟組合成一個「捷徑」，通過點擊、語音指令（Siri）或自動化觸發來執行。

> #### 點擊[連結](https://www.icloud.com/shortcuts/d0a103f5f44c404f956df291a01a76a3)下載本專案使用的捷徑腳本
>在加入之前，需要先設定此捷徑 ，請依照畫面的提示，在文字輸入框中填入你的 Flask API 的 Base URL (https://<你的vercel網址>)。

### 嘿 Siri

1. 下載設定完成捷徑後，你可以對著你的裝置說出：「**嘿 Siri，倒楣鬼**」。
2. 可使用的指令如下：
   1. **開大燈**
   2. **關大燈**
   3. **開夜燈**
   4. **關夜燈**
   5. **開啟警報模式**
   6. **關閉警報模式**
   7. **開啟濕度通知**
   8. **關閉濕度通知**
   9. **開啟感應夜燈模式**
   10. **關閉感應夜燈模式**
   11. **查詢溫濕度**
   12. **查詢目前狀態**


### 自動化設定

1.  **在「捷徑」應用程式中點擊「自動化」標籤。**
2.  **點擊「+」按鈕** 建立新的自動化。
3.  **選擇觸發條件：** 例如：選擇「時間」作為觸發條件。
4.  **設定時間：** 設定你想自動執行捷徑的時間。
5.  **選擇「立即執行」選項**
6.  **點擊「下一步」。**
7.  **點一下「新增空白的自動化操作」。**
8. **加入執行動作**
     * 點擊 **加入動作**，在搜尋欄中輸入 **文字**，並點擊 `文字` 動作，在其文字框中輸入倒楣鬼的功能指令
     * 在搜尋欄中輸入 **執行捷徑**，並點擊 `執行捷徑` 動作，選擇剛剛下載的｢倒楣鬼｣這個捷徑。
9. **點擊「完成」。**

透過自動化與捷徑，你能盡情發揮自己的創意，創造出更多符合自身需求的功能。

> [!NOTE]
> 如果沒有捷徑(Shortcuts)，也可以使用 Android 的 [Tasker](https://play.google.com/store/apps/details?id=net.dinglisch.android.taskerm) App，或是 [IFTTT](https://ifttt.com/)、[Zapier](https://zapier.com/) 等服務達到類似的自動化效果，請參考 [API 文件](/docs/API.md) ，根據自身需求自訂自動化操作。

## 參考資料

- **GPIO Zero Documentation**  
  [Installing GPIO Zero](https://gpiozero.readthedocs.io/en/stable/installing.html): Instructions for installing the GPIO Zero library and its dependencies.

- **Discord Developer Documentation**  
  [Official Documentation](https://discord.com/developers/docs/intro): Comprehensive guide to building bots and integrations for the Discord platform.

- **Flask Documentation**  
  [Official Documentation](https://flask.palletsprojects.com/en/stable/): The official Flask web framework documentation for building Python-based web applications.

- **Implementing MQTT in Python**  
  [HiveMQ Blog](https://www.hivemq.com/blog/implementing-mqtt-in-python/): A tutorial on implementing MQTT protocol in Python, useful for IoT projects.

- **Vercel Documentation**  
  [Official Documentation](https://vercel.com/docs): Detailed instructions for deploying and managing applications on Vercel.

- **Flask Vercel Example**  
  [GitHub Repository](https://github.com/faraasat/flask-vercel-example): A demonstration of deploying a Python Flask API on Vercel.

- **Xiaomi Cloud Tokens Extractor**  
  [GitHub Repository](https://github.com/PiotrMachowski/Xiaomi-cloud-tokens-extractor): A tool to retrieve tokens for Xiaomi devices directly from the Xiaomi cloud.

- **Easily Retrieve Xiaomi and Roborock Vacuum Token & Add to Home Assistant**  
  [YouTube Video](https://youtu.be/m11qbkgOz5o?si=5vTI0yFyxGTooz-P&t=175): Step-by-step guide for integrating Xiaomi and Roborock vacuum tokens into Home Assistant.  

- **Python-miio**  
  [GitHub Repository](https://github.com/rytilahti/python-miio): A Python library for interacting with Xiaomi devices via the MiIO protocol.



- **iT 邦幫忙文章**  
  [Day19 - 物聯網基礎傳輸協議 - MQTT](https://ithelp.ithome.com.tw/articles/10224407): 介紹 MQTT 協議的基礎概念和應用。 
- **Discord bot**  
  [YouTube Video](https://youtu.be/equ42VBYPrc?si=iC0Wmg8z7rXVrmD2): 【python】十分钟带你从零开始做一个discord机器人


- **Discord Webhook**  
  [YouTube Video](https://www.youtube.com/watch?v=6m6YmRUaWBM): Webhook 說明及使用示範

- **GitHub Token**  
  [YouTube Video](https://www.youtube.com/watch?v=ZQspooxvaHc&t=218s): 用Emo Uploader將GitHub用做圖床，方便發佈、分享

- **RealVNC**  
  [YouTube Video](https://www.youtube.com/watch?v=8bwbbG1mCzs): Connecting to Raspberry Pi with RealVNC

- **Siri shortcuts**  
  [Apple 官方捷徑說明](https://support.apple.com/zh-tw/guide/shortcuts/welcome/ios): 捷徑使用手冊