import json
import pandas as pd
from pathlib import Path

from core.cpu_scheduling import CPUScheduler
from core.memory_management import MemoryManager
from core.disk_scheduling import DiskScheduler
from core.deadlock import DeadlockManager

data = Path("datasets")
out = Path("outputs")
out.mkdir(exist_ok=True)

# CPU Scheduling
processes = pd.read_csv(data / "cpu_processes.csv").to_dict("records")

cpu_results = {
    "FCFS": CPUScheduler.fcfs(processes),
    "SJF": CPUScheduler.sjf(processes),
    "Round Robin": CPUScheduler.round_robin(processes, 2)
}

cpu_comparison = [
    {
        "Algorithm": name,
        "Average Waiting Time": result["average_waiting"],
        "Average Turnaround Time": result["average_turnaround"]
    }
    for name, result in cpu_results.items()
]

pd.DataFrame(cpu_comparison).to_csv(
    out / "cpu_comparison.csv", index=False
)

# Memory Management
memory = json.loads((data / "memory_pages.json").read_text())

memory_results = MemoryManager.compare(
    memory["pages"], memory["frames"]
)

pd.DataFrame(memory_results).to_csv(
    out / "memory_comparison.csv", index=False
)

# Disk Scheduling
disk = json.loads((data / "disk_requests.json").read_text())

disk_results = DiskScheduler.compare(
    disk["requests"], disk["head"], disk["disk_size"]
)

pd.DataFrame(disk_results).to_csv(
    out / "disk_comparison.csv", index=False
)

# Deadlock Management
resources = json.loads(
    (data / "deadlock_resources.json").read_text()
)

deadlock = DeadlockManager.bankers_algorithm(
    resources["allocation"],
    resources["maximum"],
    resources["available"]
)

# Save complete execution results
results = {
    "CPU Scheduling": cpu_results,
    "Memory Management": memory_results,
    "Disk Scheduling": disk_results,
    "Deadlock Management": deadlock
}

(out / "simulation_results.json").write_text(
    json.dumps(results, indent=4, default=str)
)

print("All analysis reports generated successfully!")
