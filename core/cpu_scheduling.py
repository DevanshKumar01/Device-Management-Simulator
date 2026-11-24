from collections import deque


class CPUScheduler:

    @staticmethod
    def validate(processes):
        if not processes:
            raise ValueError("Process list cannot be empty")

        ids = set()

        for p in processes:
            if not p["pid"].strip():
                raise ValueError("Process ID cannot be empty")

            if p["pid"] in ids:
                raise ValueError("Duplicate process ID")

            ids.add(p["pid"])

            if not isinstance(p["arrival"], int) or p["arrival"] < 0:
                raise ValueError("Invalid arrival time")

            if not isinstance(p["burst"], int) or p["burst"] <= 0:
                raise ValueError("Invalid burst time")

    @staticmethod
    def calculate_results(processes, completion, gantt):
        results = []

        for p in processes:
            pid = p["pid"]
            turnaround = completion[pid] - p["arrival"]
            waiting = turnaround - p["burst"]

            results.append({
                "Process": pid,
                "Arrival Time": p["arrival"],
                "Burst Time": p["burst"],
                "Completion Time": completion[pid],
                "Turnaround Time": turnaround,
                "Waiting Time": waiting
            })

        return {
            "results": results,
            "gantt": gantt,
            "average_waiting": round(
                sum(r["Waiting Time"] for r in results)
                / len(results), 2
            ),
            "average_turnaround": round(
                sum(r["Turnaround Time"] for r in results)
                / len(results), 2
            )
        }

    @staticmethod
    def fcfs(processes):
        CPUScheduler.validate(processes)

        ordered = sorted(
            processes,
            key=lambda p: p["arrival"]
        )

        time = 0
        completion = {}
        gantt = []

        for p in ordered:
            time = max(time, p["arrival"])
            start = time
            time += p["burst"]

            completion[p["pid"]] = time

            gantt.append({
                "Process": p["pid"],
                "Start": start,
                "End": time
            })

        return CPUScheduler.calculate_results(
            processes, completion, gantt
        )

    @staticmethod
    def sjf(processes):
        CPUScheduler.validate(processes)

        remaining = processes.copy()
        completion = {}
        gantt = []
        time = 0

        while remaining:
            available = [
                p for p in remaining
                if p["arrival"] <= time
            ]

            if not available:
                time = min(
                    p["arrival"] for p in remaining
                )
                continue

            p = min(
                available,
                key=lambda x: (x["burst"], x["arrival"])
            )

            start = time
            time += p["burst"]

            completion[p["pid"]] = time

            gantt.append({
                "Process": p["pid"],
                "Start": start,
                "End": time
            })

            remaining.remove(p)

        return CPUScheduler.calculate_results(
            processes, completion, gantt
        )

    @staticmethod
    def round_robin(processes, quantum=2):
        CPUScheduler.validate(processes)

        if not isinstance(quantum, int) or quantum <= 0:
            raise ValueError("Time quantum must be a positive integer")

        ordered = sorted(
            processes,
            key=lambda p: p["arrival"]
        )

        remaining = {
            p["pid"]: p["burst"]
            for p in ordered
        }

        queue = deque()
        completion = {}
        gantt = []

        time = 0
        index = 0
        n = len(ordered)

        while index < n or queue:

            if not queue and index < n:
                time = max(
                    time, ordered[index]["arrival"]
                )

            while index < n and ordered[index]["arrival"] <= time:
                queue.append(ordered[index])
                index += 1

            if not queue:
                continue

            p = queue.popleft()
            pid = p["pid"]

            duration = min(
                quantum, remaining[pid]
            )

            start = time
            time += duration
            remaining[pid] -= duration

            gantt.append({
                "Process": pid,
                "Start": start,
                "End": time
            })

            while index < n and ordered[index]["arrival"] <= time:
                queue.append(ordered[index])
                index += 1

            if remaining[pid] > 0:
                queue.append(p)
            else:
                completion[pid] = time

        return CPUScheduler.calculate_results(
            processes, completion, gantt
        )