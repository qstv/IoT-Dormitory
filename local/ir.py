from miio import ChuangmiIr
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



# 3. 發射紅外線命令
def play_ir_command(command: str):
    """發射紅外線命令"""
    print(f"正在發射命令")
    try:
        response = remote.play_raw(command)
        print("命令發射成功")
        return True
    except Exception as e:
        print(f"發射過程中出現錯誤: {e}")
        return False

def turn_on_fan():
    # 讀取命令
    command = "YOUR_LEARNED_IR_COMMAND"

    # 如果成功讀取到命令，則發射該命令
    if command:
        return play_ir_command(command)
    else:
        print("缺少command")
        return False

def turn_off_fan():
    # 讀取命令
    command = "YOUR_LEARNED_IR_COMMAND"

    # 如果成功讀取到命令，則發射該命令
    if command:
        return play_ir_command(command)
    else:
        print("缺少command")
        return False

if __name__ == "__main__":
    turn_on_fan()
    time.sleep(3)
    turn_off_fan()
