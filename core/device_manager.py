from datetime import datetime
from core.device import Device
from core.scheduler import Scheduler


class DeviceManager:

    def __init__(self):
        self.devices = {
            "D1": Device("D1", "Printer", "Virtual", 1, 10),
            "D2": Device("D2", "Scanner", "Dedicated", 1, 5),
            "D3": Device("D3", "Disk", "Shared", 3, 10),
            "D4": Device("D4", "Network", "Shared", 4, 15)
        }

        self.logs = []
        self.algorithm = "FCFS"

    def log(self, message):
        self.logs.append({
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Activity": message
        })

    def set_algorithm(self, algorithm):
        algorithm = algorithm.strip().upper()

        if algorithm not in ["FCFS", "PRIORITY"]:
            raise ValueError("Invalid scheduling algorithm")

        self.algorithm = algorithm
        self.log(f"Scheduling changed to {algorithm}")

    def get_device(self, device_id):
        if device_id not in self.devices:
            raise ValueError("Invalid device ID")

        return self.devices[device_id]

    def request_device(self, device_id, process_id, priority=3):
        device = self.get_device(device_id)
        process_id = process_id.strip()

        if not process_id:
            raise ValueError("Process ID cannot be empty")

        if not isinstance(priority, int) or not 1 <= priority <= 5:
            raise ValueError("Priority must be between 1 and 5")

        if process_id in device.owners:
            return "Process already owns this device"

        if any(r["process_id"] == process_id for r in device.queue):
            return "Process is already in the waiting queue"

        request = {
            "process_id": process_id,
            "priority": priority,
            "arrival_time": datetime.now()
        }

        device.total_requests += 1

        if device.is_available():
            device.owners.append(process_id)
            self.log(f"{device.name} allocated to {process_id}")

            return f"{device.name} allocated to {process_id}"

        device.queue.append(request)

        self.log(f"{process_id} added to {device.name} queue")

        return f"{device.name} is busy. {process_id} added to queue"

    def release_device(self, device_id, process_id):
        device = self.get_device(device_id)

        if process_id not in device.owners:
            raise ValueError("Process does not own this device")

        device.owners.remove(process_id)
        device.completed_requests += 1

        self.log(f"{process_id} released {device.name}")

        while device.queue and device.is_available():
            request = Scheduler.get_next_request(
                device.queue,
                self.algorithm
            )

            next_process = request["process_id"]
            device.owners.append(next_process)

            self.log(
                f"{device.name} automatically allocated to {next_process}"
            )

        return f"{device.name} released successfully"

    def add_to_buffer(self, device_id, data):
        device = self.get_device(device_id)

        if not isinstance(data, str) or not data.strip():
            raise ValueError("Buffer data cannot be empty")

        if len(device.buffer) >= device.buffer_capacity:
            self.log(f"Buffer overflow prevented on {device.name}")
            return "Buffer is full"

        device.buffer.append(data)

        self.log(f"Data added to {device.name} buffer")

        return "Data added successfully"

    def process_buffer(self, device_id):
        device = self.get_device(device_id)

        if not device.buffer:
            return "Buffer is empty"

        data = device.buffer.popleft()

        self.log(f"{device.name} processed data: {data}")

        return f"Processed: {data}"

    def spool_print_job(self, document_name):
        if not document_name.strip():
            raise ValueError("Document name cannot be empty")

        result = self.add_to_buffer("D1", document_name)

        if result == "Data added successfully":
            self.log(f"Print job spooled: {document_name}")
            return "Print job added to spool"

        return result

    def get_all_devices(self):
        return [
            device.to_dict()
            for device in self.devices.values()
        ]

    def get_logs(self):
        return self.logs

    def reset(self):
        self.__init__()
        return "Simulator reset successfully"