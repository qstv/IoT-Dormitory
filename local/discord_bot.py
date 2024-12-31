import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os
from ir import *

# 載入環境變數
load_dotenv()

# DISCORD TOKEN
token = os.getenv("DISCORD_TOKEN")

# FLASK API URL
api_url = os.getenv("FLASK_API_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def call_api(endpoint, is_get=False):
    """
    通用 API 請求函數，返回格式化的資料與狀態

    :param endpoint: API 路徑（相對於基礎 URL）
    :param is_get: 是否為 GET 請求，默認為 False（即 POST 請求）
    :return: 返回一個元組，包含狀態（成功或失敗）與資料型態是字串（或錯誤訊息）
    """
    try:
        if is_get:
            response = requests.get(endpoint, timeout=10)
        else:
            response = requests.post(endpoint, timeout=10)

        if response.status_code == 200:
            data = response.json()  
            if data:
                return True, data.get("response","")
            else:
                return False, "資料為空或格式錯誤"
        else:
            return False, f"錯誤，狀態碼: {response.status_code}"
    except requests.exceptions.Timeout:
        return False, "請求超時，請稍後再試！"
    except Exception as e:
        return False, f"發生錯誤: {e}"

# 指令同步
@bot.command()
async def synccommands(ctx):
    """
    同步斜線命令到 Discord 伺服器
    """
    try:
        await bot.tree.sync()  # 同步斜線命令
        await ctx.send("斜線命令已同步完成！")
    except Exception as e:
        await ctx.send(f"同步失敗：{e}")


# 以下為 discord 指令
@bot.hybrid_command()
async def 開大燈(ctx):
    """
    開啟宿舍大燈指令
    """
    await ctx.defer() # 延遲回應，告知正在處理
    api_endpoint = f"{api_url}/api/light/on"
    success, result = await call_api(api_endpoint)
    if success:
        await ctx.send(f"大燈已開啟！💡")
    else:
        await ctx.send(f"開啟大燈失敗：{result}")

@bot.hybrid_command()
async def 關大燈(ctx):
    """
    關閉宿舍大燈指令
    """
    await ctx.defer() # 延遲回應，告知正在處理
    api_endpoint = f"{api_url}/api/light/off"
    success, result = await call_api(api_endpoint)
    if success:
        await ctx.send(f"大燈已經關掉囉！")
    else:
        await ctx.send(f"關閉大燈失敗：{result}")

@bot.hybrid_command()
async def 溫濕度(ctx):
    """
    查詢宿舍溫濕度指令
    """
    await ctx.defer() # 延遲回應，告知正在處理
    api_endpoint = f"{api_url}/api/temperature-humidity"
    success, result = await call_api(api_endpoint, is_get=True)
    if success:
        formatted_data = f"溫度: {result.split("/")[1]}°C\n濕度: {result.split("/")[2]}%"
        await ctx.send(f"已經查詢到溫濕度資料！\n{formatted_data}")
    else:
        await ctx.send(f"查詢失敗：{result}")

@bot.hybrid_command()
async def 開夜燈(ctx):
    """
    開啟夜燈指令
    """
    await ctx.defer() # 延遲回應，告知正在處理
    api_endpoint = f"{api_url}/api/led/on"
    success, result = await call_api(api_endpoint)
    if success:
        await ctx.send(f"夜燈已開啟！💡")
    else:
        await ctx.send(f"開啟夜燈失敗：{result}")

@bot.hybrid_command()
async def 關夜燈(ctx):
    """
    關閉夜燈指令
    """
    await ctx.defer() # 延遲回應，告知正在處理
    api_endpoint = f"{api_url}/api/led/off"
    success, result = await call_api(api_endpoint)
    if success:
        await ctx.send(f"夜燈已關閉！")
    else:
        await ctx.send(f"關閉夜燈失敗：{result}")

class AlarmView(discord.ui.View):
    # 開啟按鈕
    @discord.ui.button(label="開啟", style=discord.ButtonStyle.success)
    async def activate_alarm(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_endpoint = f"{api_url}/api/alert/on"
        success, result = await call_api(api_endpoint)
        if success:
            await interaction.response.send_message(f"警報已開啟！🔔")
        else:
            await interaction.response.send_message(f"開啟警報失敗：{result}", ephemeral=True)

    # 關閉按鈕
    @discord.ui.button(label="關閉", style=discord.ButtonStyle.danger)
    async def deactivate_alarm(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_endpoint = f"{api_url}/api/alert/off"
        success, result = await call_api(api_endpoint)
        if success:
            await interaction.response.send_message(f"警報已關閉！🔕")
        else:
            await interaction.response.send_message(f"關閉警報失敗：{result}", ephemeral=True)

    # 取消按鈕
    @discord.ui.button(label="取消", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("操作已取消。", ephemeral=True)

@bot.hybrid_command()
async def 警報模式(ctx):
    """
    啟動警報模式，顯示選項按鈕供用戶選擇操作。
    """
    await ctx.defer() # 延遲回應，告知正在處理
    await ctx.send("請選擇操作：", view=AlarmView())

@bot.hybrid_command()
async def 宿舍狀態(ctx):
    """
    查詢宿舍與模式狀態指令
    """
    await ctx.defer() # 延遲回應，告知正在處理
    api_endpoint = f"{api_url}/api/status"
    success, result = await call_api(api_endpoint, is_get=True)
    if success:
        formatted_data = "\n".join([f"{key} : {value}" for key, value in eval(result).items()])
        await ctx.send(formatted_data)
    else:
        await ctx.send(f"查詢失敗：{result}")



class NotifyView(discord.ui.View):
    # 開啟按鈕
    @discord.ui.button(label="開啟", style=discord.ButtonStyle.success)
    async def activate_Notify(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_endpoint = f"{api_url}/api/humidity-notify/on"
        success, result = await call_api(api_endpoint)
        if success:
            await interaction.response.send_message(f"濕度通知啟動！🔔")
        else:
            await interaction.response.send_message(f"開啟濕度通知失敗：{result}", ephemeral=True)

    # 關閉按鈕
    @discord.ui.button(label="關閉", style=discord.ButtonStyle.danger)
    async def deactivate_Notify(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_endpoint = f"{api_url}/api/humidity-notify/off"
        success, result = await call_api(api_endpoint)
        if success:
            await interaction.response.send_message(f"濕度通知已關閉！")
        else:
            await interaction.response.send_message(f"關閉濕度通知失敗：{result}", ephemeral=True)

    # 取消按鈕
    @discord.ui.button(label="取消", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("操作已取消。", ephemeral=True)



@bot.hybrid_command()
async def 濕度通知(ctx):
  '''
  開啟或關閉濕度通知功能指令
  '''
  await ctx.defer() # 延遲回應，告知正在處理
  await ctx.send("請選擇操作：", view=NotifyView())


@bot.hybrid_command()
async def 設定通知濕度(ctx, 濕度: int):
    """
    設定濕度通知的濕度指令
    :param 濕度: 使用者輸入的濕度值（整數）。
    """
    await ctx.defer() # 延遲回應，告知正在處理
    if 0 <= 濕度 <= 100:  # 檢查濕度是否在合理範圍
        api_endpoint = f"{api_url}/api/set/humidity/{濕度}"
        success, result = await call_api(api_endpoint)
        if success:
            await ctx.send(f"成功設定通知濕度為 {濕度}%！")
        else:
            await ctx.send(f"設定通知濕度失敗：{result}")
    else:
        await ctx.send("請輸入一個介於 0 到 100 的有效濕度值！")

@設定通知濕度.error
async def 設定通知濕度_error(ctx, error):
    """
    捕捉與設定濕度相關的錯誤
    """
    if isinstance(error, commands.BadArgument):
        await ctx.send("無效輸入！請輸入一個整數作為濕度值，例如：`!設定濕度 60`")
    else:
        await ctx.send("發生未知錯誤，請稍後再試。")
        print(f"Unexpected error: {error}")

class View(discord.ui.View):
    # 開啟按鈕
    @discord.ui.button(label="開啟", style=discord.ButtonStyle.success)
    async def activate_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_endpoint = f"{api_url}/api/night-light-mode/on"
        success, result = await call_api(api_endpoint)
        if success:
            await interaction.response.send_message(f"感應夜燈模式已開啟！")
        else:
            await interaction.response.send_message(f"開啟感應夜燈模式失敗：{result}", ephemeral=True)

    # 關閉按鈕
    @discord.ui.button(label="關閉", style=discord.ButtonStyle.danger)
    async def deactivate_mode(self, interaction: discord.Interaction, button: discord.ui.Button):
        api_endpoint = f"{api_url}/api/night-light-mode/off"
        success, result = await call_api(api_endpoint)
        if success:
            await interaction.response.send_message(f"感應夜燈模式已關閉！")
        else:
            await interaction.response.send_message(f"關閉感應夜燈模式失敗：{result}", ephemeral=True)

    # 取消按鈕
    @discord.ui.button(label="取消", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("操作已取消。", ephemeral=True)

@bot.hybrid_command()
async def 感應夜燈模式(ctx):
    """
    開啟或關閉感應夜燈，顯示選項按鈕供用戶選擇操作。
    """
    await ctx.defer() # 延遲回應，告知正在處理
    await ctx.send("請選擇操作：", view=View())


@bot.hybrid_command()
async def 開電扇(ctx):
    '''
    打開宿舍電扇指令
    '''
    await ctx.defer() # 延遲回應，告知正在處理
    try:
        if turn_on_fan():
            await ctx.send("打開了", ephemeral=True)
        else:
            await ctx.send("哎呀! 出了點問題", ephemeral=True)
    except Exception as e:
        await ctx.send(f"發生錯誤: {e}", ephemeral=True)


@bot.hybrid_command()
async def 關電扇(ctx):
    '''
    關閉宿舍電扇指令
    '''
    await ctx.defer() # 延遲回應，告知正在處理
    try:
        if turn_off_fan():
            await ctx.send("關閉了", ephemeral=True)
        else:
            print(turn_off_fan)
            await ctx.send("哎呀! 出了點問題", ephemeral=True)
    except Exception as e:
        await ctx.send(f"發生錯誤: {e}", ephemeral=True)

# 啟動 Bot
bot.run(token)
