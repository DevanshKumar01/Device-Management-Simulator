class DiskScheduler:

    @staticmethod
    def validate(requests, head, disk_size):
        if not isinstance(disk_size, int) or disk_size <= 0:
            raise ValueError("Invalid disk size")

        if not requests:
            raise ValueError("Request queue cannot be empty")

        if not isinstance(head, int) or not 0 <= head < disk_size:
            raise ValueError("Invalid head position")

        for request in requests:
            if not isinstance(request, int) or not 0 <= request < disk_size:
                raise ValueError("Invalid disk request")

    @staticmethod
    def calculate(sequence, head, request_count):
        path = [head] + sequence

        movement = sum(
            abs(path[i] - path[i - 1])
            for i in range(1, len(path))
        )

        return {
            "sequence": sequence,
            "path": path,
            "total_movement": movement,
            "average_movement": round(
                movement / request_count, 2
            )
        }

    @staticmethod
    def fcfs(requests, head, disk_size=200):
        DiskScheduler.validate(requests, head, disk_size)

        return DiskScheduler.calculate(
            requests.copy(), head, len(requests)
        )

    @staticmethod
    def sstf(requests, head, disk_size=200):
        DiskScheduler.validate(requests, head, disk_size)

        remaining = requests.copy()
        sequence = []
        current = head

        while remaining:
            nearest = min(
                remaining,
                key=lambda r: abs(r - current)
            )

            sequence.append(nearest)
            remaining.remove(nearest)
            current = nearest

        return DiskScheduler.calculate(
            sequence, head, len(requests)
        )

    @staticmethod
    def scan(requests, head, disk_size=200):
        DiskScheduler.validate(requests, head, disk_size)

        left = sorted(
            [r for r in requests if r < head],
            reverse=True
        )

        right = sorted(
            [r for r in requests if r >= head]
        )

        sequence = right.copy()

        if left:
            if not sequence or sequence[-1] != disk_size - 1:
                sequence.append(disk_size - 1)

            sequence.extend(left)

        return DiskScheduler.calculate(
            sequence, head, len(requests)
        )

    @staticmethod
    def cscan(requests, head, disk_size=200):
        DiskScheduler.validate(requests, head, disk_size)

        left = sorted(
            [r for r in requests if r < head]
        )

        right = sorted(
            [r for r in requests if r >= head]
        )

        sequence = right.copy()

        if left:
            if not sequence or sequence[-1] != disk_size - 1:
                sequence.append(disk_size - 1)

            if left[0] != 0:
                sequence.append(0)

            sequence.extend(left)

        return DiskScheduler.calculate(
            sequence, head, len(requests)
        )

    @staticmethod
    def compare(requests, head, disk_size=200):
        algorithms = {
            "FCFS": DiskScheduler.fcfs,
            "SSTF": DiskScheduler.sstf,
            "SCAN": DiskScheduler.scan,
            "C-SCAN": DiskScheduler.cscan
        }

        results = []

        for name, algorithm in algorithms.items():
            result = algorithm(requests, head, disk_size)

            results.append({
                "Algorithm": name,
                "Total Head Movement": result["total_movement"],
                "Average Head Movement": result["average_movement"]
            })

        return results