# 使用 Vercel 部署 Flask API 說明文件

## 概述
[[直接跳到部署步驟](#部署步驟)]

這是一個基於 Flask 的 API 服務，它透過 MQTT 協議與樹莓派進行通訊，接收來自用戶端的 HTTP 請求，並將指令轉發至 MQTT Broker，同時接收來自 MQTT Broker 的回覆，並回傳給用戶端。

## 檔案說明

以下為此部分各個檔案的功能說明：

1.  **`api/main.py`**:
    *   使用 `Flask` 框架建立 API 伺服器。
    *   使用 `paho-mqtt` 函式庫，透過 MQTT 協議與後端裝置溝通。
    *   使用 `threading` 函式庫，建立執行緒來處理 MQTT 訊息和回應。
    *   接收到指令後，會使用 UUID 生成唯一的 `correlation_id`，並將此 ID 與指令一同發送至 MQTT Broker。
    *   使用 `threading.Event()` 來實現等待回應的功能。當接收到帶有相同 `correlation_id` 的 MQTT 訊息時，會喚醒等待中的執行緒。
    *   如果等待超過 8 秒沒有收到回應，則會回傳超時錯誤。
2.  **`vercel.json`**:
    *   定義了所有請求都將導向 `/api/main` 的路由規則。
    *   這是 Vercel 部署 Flask 應用程式的必要設定。
3.  **`requirements.txt`**:
    *   定義了專案所需的函式庫，包含 `Flask` 和 `paho-mqtt`。
    *   Vercel 會自動根據此檔案安裝必要的函式庫。

## 部署步驟

以下是將 Flask API 部署到 Vercel 的詳細步驟：

#### 0. **複製檔案**

1.  **建立專案目錄**: 在你的電腦上，建立一個新的資料夾來存放專案檔案。
2.  **複製檔案**: 將以下三個檔案 `api/main.py`、`vercel.json` 和 `requirements.txt` 複製到你剛建立的專案目錄中。

#### 1. 建立 GitHub Repository

1.  **初始化 Git**: 在你的專案目錄下，使用以下指令初始化 Git Repository：
    ```bash
    git init
    ```
2.  **加入檔案**: 使用以下指令將專案檔案加入 Git Repository：
    ```bash
    git add .
    ```
3.  **提交變更**: 使用以下指令提交變更：
    ```bash
    git commit -m "Initial commit"
    ```
4.  **建立 GitHub Repository**: 在 GitHub 上建立一個新的Repository。
5.  **推送程式碼**: 將你的本地程式碼推送至 GitHub Repository：
    ```bash
    git remote add origin <你的 GitHub Repository URL>
    git push -u origin main
    ```

#### 2. 建立 Vercel 專案

1.  **註冊 Vercel 帳號**: 如果你還沒有 Vercel 帳號，請先[註冊](https://vercel.com/)一個。
2.  **導入 GitHub 專案**:
    *   登入 Vercel 後，點擊 **Add New Project** 按鈕。
    *   選擇 **Import Git Repository**。
    *   選擇你的 GitHub 帳號，並找到你剛才建立的 GitHub Repository。
    *   點擊 **Import** 按鈕。

#### 3. 設定 Vercel 環境

在 Vercel 專案設定頁面中，你需要設定環境變數：

1.  進入專案設定頁面Framework選擇**Other**。
2.  **選擇 Environment Variables**: 找到環境變數設定。
3.  **新增環境變數**: 點擊 **Add More** 按鈕，新增以下環境變數：
![vercel 環境](<vercel 環境.png>)
    *   **`CLUSTER_URL`**:  MQTT Broker 的 URL。
    *   **`BROKER_PORT`**: MQTT Broker 的 Port。
    *   **`USERNAME`**: MQTT Broker 的使用者名稱。
    *   **`PASSWORD`**: MQTT Broker 的密碼。
    *   輸入數值後，點選 **Save** 儲存。

        *   **注意**: 請確保這些變數與你的 MQTT Broker 設定一致。

#### 4. 部署專案

1.  **點擊 Deploy**: 在 Vercel 專案設定頁面中，點擊 **Deploy** 按鈕。
2.  **等待部署完成**: Vercel 會自動建置並部署你的專案。你可以在部署過程中查看進度。
3.  **訪問你的 API**: 部署完成後，你將會看到 **Holle World!** 畫面，同時獲得一個 Vercel 提供的 URL，你可以使用這個 URL 來訪問你的 API。
![vercel部署完成](<vercel部署完成.png>)


#### 5. 測試你的 API

*   可以使用工具（如 `curl`, `Postman`）或撰寫程式碼發送 HTTP 請求，來測試你的 API 是否正常運作。
    * 例如發送 POST 請求到 `https://<你的vercel網址>/api/light/on` 應該會讓你的樹莓派收到訊息。


## 常見問題

1.  **部署失敗**:
    *   檢查你的 GitHub Repository是否包含所有必要的檔案（`api/main.py`、`vercel.json` 和 `requirements.txt`）。
    *   檢查**環境變數**是否正確。
    *   查看 Vercel 的部署日誌，尋找錯誤訊息。

3.  **接收不到 MQTT 回應**:
    *   檢查你的 MQTT Broker 的設定是否正確。
    *   檢查你的樹莓派是否成功發送回應。

[[返回主文件](../README.md#快速開始)]
