import asyncio
import websockets

clients = set()

async def register(websocket):
    clients.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        clients.remove(websocket)

async def ws_handler(websocket, path):
    await register(websocket)
    async for message in websocket:
        for client in clients:
            if client != websocket:
                await client.send(message)

def start_websocket_server():
    loop = asyncio.get_event_loop()
    server = websockets.serve(ws_handler, "localhost", 8765)
    loop.run_until_complete(server)
    loop.run_forever()
