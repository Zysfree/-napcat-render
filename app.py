import asyncio
import websockets
import requests
import json
import re

# 部署后从 NapCat WebUI 获取 Token 再替换这里
NAPCAT_TOKEN = "REPLACE_ME_LATER"
NAPCAT_HTTP_URL = "http://127.0.0.1:3000"
LISTEN_HOST = "0.0.0.0"
LISTEN_PORT = 8082

def send_group_msg(gid, msg):
    try:
        resp = requests.post(
            f"{NAPCAT_HTTP_URL}/send_group_msg",
            headers={"Authorization": f"Bearer {NAPCAT_TOKEN}"},
            json={"group_id": gid, "message": msg},
            timeout=5
        )
        print(f"[SEND OK] code={resp.status_code} | {msg}")
    except Exception as e:
        print(f"[SEND ERR] {e}")

async def handle_conn(websocket):
    print("✅ NapCat 已连接到 8082 端口！")
    async for raw in websocket:
        try:
            data = json.loads(raw)
            if data.get("message_type") != "group":
                continue
            gid = data.get("group_id")
            raw_msg = data.get("raw_message", "")
            text = re.sub(r"\[CQ:.+?\]", "", raw_msg).strip()
            print(f"📩 收到群消息：{text}")

            if text == "测试":
                send_group_msg(gid, "✅ Render 部署成功！端口监听正常！")
        except Exception as e:
            print(f"[HANDLE ERR] {e}")

async def main():
    print(f"🚀 启动 WebSocket 监听 {LISTEN_HOST}:{LISTEN_PORT}")
    async with websockets.serve(handle_conn, LISTEN_HOST, LISTEN_PORT):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())