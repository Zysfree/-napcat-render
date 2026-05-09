from fastapi import FastAPI
import uvicorn
import subprocess
import threading
import time
import os

app = FastAPI()

# 首页保活，防止 Render 休眠
@app.get("/")
def home():
    return {"status": "running", "note": "NapCat + Bot running on Render"}

# 自动安装并启动 NapCat（已修复404、权限、xvfb报错）
def install_and_start_napcat():
    print("📥 正在下载 NapCat（最新可用地址）...")
    # 1. 下载最新 NapCat 包（修复404）
    os.system("wget https://github.com/NapNeko/NapCatQQ/releases/latest/download/NapCat.Shell.zip -O napcat.zip")
    
    print("📂 正在解压 NapCat...")
    # 2. 解压
    os.system("unzip -o napcat.zip -d /opt/napcat")
    
    print("🚀 启动 NapCat 无头模式（无需xvfb）...")
    # 3. 无头启动，不需要图形界面/权限
    subprocess.Popen([
        "/opt/napcat/napcat",
        "run",
        "--no-ui"
    ])

# 启动机器人，等待 NapCat 就绪
def start_bot():
    time.sleep(60)  # 等待 NapCat 完全启动
    print("🤖 启动 Python 机器人...")
    while True:
        try:
            subprocess.run(["python3", "app.py"])
        except:
            pass
        print("⚠️  机器人异常退出，3秒后重启...")
        time.sleep(3)

if __name__ == "__main__":
    # 后台启动 NapCat
    threading.Thread(target=install_and_start_napcat, daemon=True).start()
    # 后台启动机器人
    threading.Thread(target=start_bot, daemon=True).start()
    # 启动保活服务
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
