from botbuilder.core import MemoryStorage
from botbuilder.schema import Activity


class ActivityLog:
    def __init__(self, storage: MemoryStorage):
        self._storage = storage

    async def append(self, activity_id: str, activity: Activity):
        if not activity_id:
            raise TypeError("activity_id is required for ActivityLog.append")

        if not activity:
            raise TypeError("activity is required for ActivityLog.append")

        obj = {}
        obj[activity_id] = activity

        await self._storage.write(obj)
        return

    async def find(self, activity_id: str) -> Activity:
        if not activity_id:
            raise TypeError("activity_id is required for ActivityLog.find")

        items = await self._storage.read([activity_id])
        return items[activity_id] if len(items) >= 1 else None
