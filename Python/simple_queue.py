import uasyncio as asyncio

class SimpleQueue:
    def __init__(self):
        self.items = []

    async def put(self, item):
        self.items.append(item)

    async def get(self):
        while not self.items:
            await asyncio.sleep(0)   # yield CPU
        return self.items.pop(0)
