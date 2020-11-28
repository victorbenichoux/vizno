import os
from typing import List

import fastapi
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse
from starlette.websockets import WebSocket, WebSocketDisconnect

app = fastapi.FastAPI()

app.mount("/static", StaticFiles(directory=os.environ["SERVER_DIR"]))


class UpdateNotifier:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def notify(self):
        connections = []
        while len(self.connections) > 0:
            websocket = self.connections.pop()
            await websocket.send_text("update")
            connections.append(websocket)
        self.connections = connections


notifier = UpdateNotifier()


@app.get("/")
def redirect_to_index():
    return RedirectResponse(url="/static/index.html")


@app.post("/update")
async def has_updated():
    await notifier.notify()
    return "ok"


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)
