
import asyncio
import threading
import json
import time
import pyxel
import websockets

# 自分の座標
x, y = 40, 40

# 相手の座標（補間用）
enemy_x, enemy_y = 100, 100
target_enemy_x, target_enemy_y = 100, 100
last_update_time = time.time()

SERVER_URI = "ws://localhost:8765"

# ネットワーク受信ループ
async def network_loop():
    global target_enemy_x, target_enemy_y, last_update_time
    async with websockets.connect(SERVER_URI) as websocket:
        while True:
            try:
                data = await websocket.recv()
                obj = json.loads(data)
                target_enemy_x, target_enemy_y = obj["x"], obj["y"]
                last_update_time = time.time()
            except:
                break

# 自分の位置送信ループ
def send_position():
    async def _send():
        async with websockets.connect(SERVER_URI) as websocket:
            while True:
                await websocket.send(json.dumps({"x": x, "y": y}))
                await asyncio.sleep(0.05)  # 20FPS送信
    asyncio.run(_send())

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel 1vs1 Lag Compensation")
        threading.Thread(target=lambda: asyncio.run(network_loop()), daemon=True).start()
        threading.Thread(target=send_position, daemon=True).start()
        pyxel.run(self.update, self.draw)

    def update(self):
        global x, y, enemy_x, enemy_y
        # 自分の移動
        if pyxel.btn(pyxel.KEY_LEFT):
            x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            x += 1
        if pyxel.btn(pyxel.KEY_UP):
            y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            y += 1

        # 相手の位置を補間
        lerp_factor = 0.1  # 補間の速さ（0.0〜1.0）
        enemy_x += (target_enemy_x - enemy_x) * lerp_factor
        enemy_y += (target_enemy_y - enemy_y) * lerp_factor

    def draw(self):
        pyxel.cls(0)
        pyxel.text(5, 5, "You", 7)
        pyxel.text(120, 5, "Enemy", 8)
        pyxel.rect(x, y, 8, 8, 11)      # 自分
        pyxel.rect(int(enemy_x), int(enemy_y), 8, 8, 8)  # 相手

if __name__ == "__main__":
    App()



