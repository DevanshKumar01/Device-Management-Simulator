from dataclasses import dataclass, field
from collections import deque


@dataclass
class Device:
    device_id: str
    name: str
    device_type: str
    capacity: int = 1
    buffer_capacity: int = 5

    owners: list = field(default_factory=list)
    queue: deque = field(default_factory=deque)
    buffer: deque = field(default_factory=deque)

    total_requests: int = 0
    completed_requests: int = 0

    @property
    def status(self):
        if len(self.owners) >= self.capacity:
            return "Busy"
        elif self.owners:
            return "Partially Busy"
        return "Available"

    def is_available(self):
        return len(self.owners) < self.capacity

    def to_dict(self):
        return {
            "Device ID": self.device_id,
            "Device": self.name,
            "Type": self.device_type,
            "Status": self.status,
            "Owner": ", ".join(self.owners) or "None",
            "Queue": len(self.queue),
            "Buffer": len(self.buffer),
            "Capacity": self.capacity,
            "Completed Requests": self.completed_requests
        }