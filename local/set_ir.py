from miio import ChuangmiIr
import base64
import time
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

# 設定設備的 IP 和 Token
ip = os.getenv("IP")
token = os.getenv("TOKEN")

# 初始化 Chuangmi IR 遙控器
remote = ChuangmiIr(ip, token)

# 1. 學習紅外線命令
def learn_ir_command(key: int):
    """學習紅外線命令並儲存到指定槽位"""
    print(f"開始學習紅外線命令，將儲存至金鑰槽位 {key}...")
    try:
        response = remote.learn(key)
        print(f"學習成功，命令已儲存至槽位 {key}")
    except Exception as e:
        print(f"學習過程中出現錯誤: {e}")

# 2. 讀取已學習的紅外線命令
def read_ir_command(key: int):
    """讀取已學習的紅外線命令"""
    print(f"正在讀取金鑰槽位 {key} 的命令...")
    try:
        response = remote.read(key)
        if "code" in response:
            code = response["code"]
            print(f"讀取到的命令: {code}")
            return code
        else:
            print(f"未找到命令，錯誤: {response['error']}")
            return None
    except Exception as e:
        print(f"讀取過程中出現錯誤: {e}")
        return None

# 3. 發射紅外線命令
def play_ir_command(command: str):
    """發射紅外線命令"""
    print(f"正在發射命令: {command}")
    try:
        response = remote.play_raw(command)
        print("命令發射成功")
    except Exception as e:
        print(f"發射過程中出現錯誤: {e}")
import json

def save_command_to_file(command: str, filename: str = "ir_commands.json"):
    """保存命令到本地文件"""
    try:
        with open(filename, "w") as file:
            json.dump({"command": command}, file)
        print("命令已成功保存到本地文件")
    except Exception as e:
        print(f"保存命令時出現錯誤: {e}")

# 示例流程
def main():
    key = 1  # 儲存紅外線命令的金鑰槽位

    # 學習命令
    learn_ir_command(key)

    # 等待一段時間，讓學習過程完成
    time.sleep(5)

    # 讀取命令
    command = read_ir_command(key)
    save_command_to_file(command)
    # 如果成功讀取到命令，則發射該命令
    if command:
        play_ir_command(command)

if __name__ == "__main__":
    main()
