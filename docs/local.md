# 本地端相關程式碼說明文件
## 概述

[[直接跳到安裝步驟](#安裝步驟)]

使用者可以通過 Discord 聊天機器人發送指令。

## 檔案說明

以下此部分各個 Python 檔案的功能說明：

1.  **`discord_bot.py`**:
    *   **功能**: 建立一個 Discord 機器人，接收使用者指令，並透過 HTTP 請求將指令傳送至 Flask API。
    *   **主要功能**:
        可使用`/`命令(推薦使用)或是使用`![指令名稱]`(不推薦)
        *   `!synccommands`：同步斜線命令。
        *   `!開大燈`：開啟宿舍大燈。
        *   `!關大燈`：關閉宿舍大燈。
        *   `!溫濕度`：查詢宿舍溫濕度。
        *   `!開夜燈`：開啟夜燈。
        *   `!關夜燈`：關閉夜燈。
        *   `!警報模式`：開啟或關閉警報模式。
        *   `!宿舍狀態`：查詢宿舍與模式狀態。
        *   `!濕度通知`：開啟或關閉濕度通知。
        *   `!設定通知濕度 [濕度]`：設定濕度通知閾值。
        *   `!感應夜燈模式`：開啟或關閉感應夜燈模式。
        *   `!開電扇`：開啟電扇。
        *   `!關電扇`：關閉電扇。

2.  **`ir.py`**:
    *   **功能**: 控制小米萬能遙控器，發射紅外線指令。
    *   **主要功能**:
        *   使用 `miio` 庫與小米萬能遙控器互動。
        *   `play_ir_command(command: str)`: 發射紅外線命令。
        *   `turn_on_fan()`: 發射開啟電風扇的紅外線命令。
        *   `turn_off_fan()`: 發射關閉電風扇的紅外線命令。

3.  **`set_ir.py`**:
    *   **功能**: 學習並儲存紅外線命令。
    *   **主要功能**:
        *   使用 `miio` 庫學習紅外線命令。
        *   `learn_ir_command(key: int)`: 學習紅外線命令。
        *   `read_ir_command(key: int)`: 讀取已學習的紅外線命令。
        *   `play_ir_command(command: str)`: 發射紅外線命令。
         *  `save_command_to_file(command: str, filename: str = "ir_commands.json")` :保存紅外線命令到本地json檔案。

5.  **`.env.example`**:
    *   **功能**: 範例環境變數設定檔案。
    *   **主要內容**:
        *   `DISCORD_TOKEN`: Discord 機器人的 TOKEN。
        *   `FLASK_API_URL`: Flask API 的 URL。
        *   `IP`: 小米萬能遙控器的 IP 位址。
        *   `TOKEN`: 小米萬能遙控器的 Token。
    *   **說明**: 提供範例，使用者需要複製此檔案並更名為 `.env`，並填入實際的值。

## 環境設定

1.  **安裝 Python 函式庫**: 開啟終端機，輸入以下指令安裝所需的 Python 函式庫：
    ```bash
    pip3 install discord.py python-dotenv requests miio
    ```
2.  **設定環境變數**:
    *   複製 `.env.example` 檔案並更名為 `.env`。
    *   編輯 `.env` 檔案，填入你的 **Discord 機器人 TOKEN** 、 **Flask API 的 URL** 、 **小米萬能遙控器的 IP 和 Token**。
       ```
       DISCORD_TOKEN=YOUR_DISCORD_BOT_TOKEN
       FLASK_API_URL=YOUR_FLASK_API_URL
       IP=YOUR_MI_IR_CONTROLLER_IP
       TOKEN=YOUR_MI_IR_CONTROLLER_TOKEN
       ```
    *   **建立 Discord 機器人與取得 TOKEN** : 
        - 第1步: 請至 [Discord Developer Portal](https://discord.com/developers/applications) 建立一個應用程式並取名。
        ![discord_1](/docs/discord_1.png)

        - 第2步: 在左側欄點選 **Bot**  ；點選 **Reset Token**，並複製得到的 Discord 機器人 TOKEN
        ![discord_2](/docs/discord_2.png)

        - 第3步: 關閉 **PUBLIC BOT** 選項、開啟 **MESSAGE CONTENT INTENT** 選項。
        ![discord_3](/docs/discord_3.png)

        - 第4步: 在左側欄點選 **OAuth2** ；在 OAuth2 URL Generator 的 SCOPES 選擇 **bot** 並在下方 Bot Permissions 中選擇 **Administrator** 。
        ![discord_4](/docs/discord_4.png)

        - 第5步: 複製在 第4步 的Generated URL ，利用該 URL 邀請機器人加入 Discord 伺服器。
        ![discord_5](/docs/discord_5.png)

    詳細的操作流程可以參考 [YouTube 教學影片](https://youtu.be/equ42VBYPrc?feature=shared)
    *   **Flask API URL** : 我們使用Vercel部署我們的Flask程式，操作方法請參考 [使用 Vercel 部署 Flask API 說明文件](/docs/Vercel.md)。
    *   **小米萬能遙控器 IP 與 Token**:
        *   請確保你的小米萬能遙控器與電腦已連上同個的 Wi-Fi 網路，並透過小米智慧家庭 App 完成設定。
        *   取得 IP 與 Token 的方法，請參考 [Easily Retrieve Xiaomi and Roborock Vacuum Token & Add to Home Assistant](https://youtu.be/m11qbkgOz5o?si=5vTI0yFyxGTooz-P&t=175)

3.  **取得紅外線指令**: 使用 `set_ir.py` 來學習紅外線指令。
    ```bash
    python3 set_ir.py
    ```
    *   執行後程式碼會引導你學習按鈕，並將指令儲存至 `ir_commands.json` 檔案。
    *   請將學習到的指令，複製並貼到 `ir.py` 中 `turn_on_fan` 與 `turn_off_fan` 的 `command` 變數中。
    ```python
    # 讀取命令
    command = "YOUR_LEARNED_IR_COMMAND"
    ```

## 安裝步驟

1.  **安裝 Python 函式庫**: 請參考 [環境設定](#環境設定) 中的步驟。
2.  **設定環境變數**: 請參考 [環境設定](#環境設定) 中的步驟。
3.  **複製程式碼**: 將 `discord_bot.py`、`ir.py`、`set_ir.py`、`.env` 檔案複製到你的電腦上。
4.  **取得紅外線指令**: 請參考 [環境設定](#環境設定) 中的步驟，並修改 `ir.py`。

### 如何使用

1.  **啟動 Discord 機器人**: 開啟終端機，切換到你的程式碼目錄，執行以下指令啟動 Discord 機器人：
    ```bash
    python3 discord_bot.py
    ```
3.  **在 Discord 中使用指令**:
    *   在 Discord 伺服器中，先輸入`!synccommands`：同步斜線命令，重新載入後就可使用`/`命令較為方便(推薦使用)或是使用指令前綴 `!`，例如：
        *   `!開大燈`: 開啟大燈。
        *   `!關大燈`: 關閉大燈。
        *   `!溫濕度`: 查詢溫濕度。
        *   `!開夜燈`: 開啟夜燈。
        *   `!關夜燈`: 關閉夜燈。
        *   `!警報模式`: 開啟或關閉警報模式(需點擊按鈕)。
        *   `!宿舍狀態`: 查詢宿舍狀態。
        *   `!濕度通知`: 開啟或關閉濕度通知(需點擊按鈕)。
         *  `!設定通知濕度 [濕度]`: 設定濕度通知閾值 (例: !設定通知濕度 70)。
         *  `!感應夜燈模式`：開啟或關閉感應夜燈模式(需點擊按鈕)。
        *  `!開電扇`: 開啟電扇。
        *   `!關電扇`: 關閉電扇。
    *   機器人會根據你的指令，回傳對應的訊息。


## 常見問題處理

1.  **機器人無法連線**:
    *   檢查你的 Discord 機器人 TOKEN 是否正確。
    *   檢查你的網路連線是否正常。
    *   檢查你是否已將機器人加入你的 Discord 伺服器。
2.  **指令無法執行**:
    *   檢查你在Vercel的 Flask API 是否正在運作，且 URL 設定正確。
    *   檢查你的紅外線遙控器是否已連上網路，且 IP 和 Token 設定正確。
    *   檢查你的紅外線指令是否正確，請重新使用 `set_ir.py` 學習指令。
3.  **環境變數**:
    *   檢查你的 `.env` 檔案是否正確放置在你的程式碼目錄下。
    *   檢查你的環境變數是否已正確設定。
4.  **看不到斜線指令**:
    *   請檢查是否已成功同步斜線指令。
        * 使用指令 `!synccommands` 同步斜線指令。
5.  **`miio` 庫無法找到裝置**：
     *  請確保你的小米萬能遙控器和電腦在同一個網路中。
     *  請檢查IP是否正確，並檢查小米萬能遙控器是否有啟動。

[[返回主文件](../README.md#快速開始)]