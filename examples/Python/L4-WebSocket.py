import asyncio
from solana.rpc.websocket_api import connect


async def main():
    async with connect("wss://api.devnet.solana.com/") as websocket:
        print("Подключено к WebSocket RPC")
        await websocket.slot_subscribe()

        for _ in range(5):
            message = await websocket.recv()
            print("Новое событие:", message)

asyncio.run(main())
