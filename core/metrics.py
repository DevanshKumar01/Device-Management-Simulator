class Metrics:

    @staticmethod
    def device_metrics(device):
        utilization = (
            len(device.owners) / device.capacity
        ) * 100

        buffer_utilization = (
            len(device.buffer) / device.buffer_capacity
        ) * 100

        completion_rate = (
            device.completed_requests / device.total_requests * 100
            if device.total_requests > 0 else 0
        )

        return {
            "Device": device.name,
            "Total Requests": device.total_requests,
            "Completed Requests": device.completed_requests,
            "Active Requests": len(device.owners),
            "Waiting Requests": len(device.queue),
            "Utilization (%)": round(utilization, 2),
            "Buffer Usage (%)": round(buffer_utilization, 2),
            "Completion Rate (%)": round(completion_rate, 2)
        }

    @staticmethod
    def get_all_metrics(manager):
        return [
            Metrics.device_metrics(device)
            for device in manager.devices.values()
        ]

    @staticmethod
    def system_summary(manager):
        devices = list(manager.devices.values())

        total_requests = sum(
            d.total_requests for d in devices
        )

        completed_requests = sum(
            d.completed_requests for d in devices
        )

        active_requests = sum(
            len(d.owners) for d in devices
        )

        waiting_requests = sum(
            len(d.queue) for d in devices
        )

        total_capacity = sum(
            d.capacity for d in devices
        )

        utilization = (
            active_requests / total_capacity * 100
            if total_capacity > 0 else 0
        )

        return {
            "Total Devices": len(devices),
            "Total Requests": total_requests,
            "Completed Requests": completed_requests,
            "Active Requests": active_requests,
            "Waiting Requests": waiting_requests,
            "Available Devices": sum(
                d.is_available() for d in devices
            ),
            "Busy Devices": sum(
                not d.is_available() for d in devices
            ),
            "System Utilization (%)": round(utilization, 2),
            "Completion Rate (%)": round(
                completed_requests / total_requests * 100
                if total_requests > 0 else 0, 2
            )
        }