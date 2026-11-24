import pytest
import json
from pathlib import Path

from core.device_manager import DeviceManager
from core.metrics import Metrics
from core.cpu_scheduling import CPUScheduler
from core.memory_management import MemoryManager
from core.disk_scheduling import DiskScheduler
from core.deadlock import DeadlockManager

DATA = Path("datasets")


def test_device_allocation():
    m = DeviceManager()
    m.request_device("D1", "P1")
    assert m.devices["D1"].owners == ["P1"]


def test_device_queue():
    m = DeviceManager()
    m.request_device("D1", "P1")
    m.request_device("D1", "P2")
    assert len(m.devices["D1"].queue) == 1


def test_reallocation():
    m = DeviceManager()
    m.request_device("D1", "P1")
    m.request_device("D1", "P2")
    m.release_device("D1", "P1")
    assert m.devices["D1"].owners == ["P2"]


def test_priority():
    m = DeviceManager()
    m.set_algorithm("PRIORITY")
    m.request_device("D1", "P1")
    m.request_device("D1", "P2", 5)
    m.request_device("D1", "P3", 1)
    m.release_device("D1", "P1")
    assert m.devices["D1"].owners == ["P3"]


def test_shared_device():
    m = DeviceManager()
    for p in ["P1", "P2", "P3"]:
        m.request_device("D3", p)
    assert len(m.devices["D3"].owners) == 3


def test_invalid_device():
    m = DeviceManager()
    with pytest.raises(ValueError):
        m.request_device("D99", "P1")


def test_empty_process():
    m = DeviceManager()
    with pytest.raises(ValueError):
        m.request_device("D1", "")


def test_metrics():
    m = DeviceManager()
    m.request_device("D1", "P1")
    assert Metrics.system_summary(m)["Active Requests"] == 1


def test_logs():
    m = DeviceManager()
    m.request_device("D1", "P1")
    assert len(m.get_logs()) > 0


@pytest.mark.parametrize("algorithm,expected", [
    ("fcfs", 4.33),
    ("sjf", 2.33),
    ("round_robin", 5.0)
])
def test_cpu(algorithm, expected):
    p = [
        {"pid": "P1", "arrival": 0, "burst": 5},
        {"pid": "P2", "arrival": 0, "burst": 3},
        {"pid": "P3", "arrival": 0, "burst": 2}
    ]
    result = getattr(CPUScheduler, algorithm)(p)
    assert result["average_waiting"] == pytest.approx(expected)


@pytest.mark.parametrize("algorithm,faults", [
    ("FIFO", 10),
    ("LRU", 9),
    ("OPTIMAL", 7)
])
def test_memory(algorithm, faults):
    data = json.loads((DATA / "memory_pages.json").read_text())
    result = MemoryManager.simulate(
        data["pages"], data["frames"], algorithm
    )
    assert result["page_faults"] == faults


def test_disk():
    result = DiskScheduler.fcfs(
        [98,183,37,122,14,124,65,67], 53, 200
    )
    assert result["total_movement"] == 640


def test_disk_boundary():
    result = DiskScheduler.fcfs([0,199], 0, 200)
    assert result["total_movement"] == 199


def test_safe_state():
    data = json.loads((DATA / "deadlock_resources.json").read_text())
    result = DeadlockManager.bankers_algorithm(
        data["allocation"],
        data["maximum"],
        data["available"]
    )
    assert result["safe"] is True


def test_unsafe_state():
    result = DeadlockManager.bankers_algorithm(
        [[1],[1]], [[2],[2]], [0]
    )
    assert result["safe"] is False


def test_invalid_allocation():
    with pytest.raises(ValueError):
        DeadlockManager.bankers_algorithm(
            [[5]], [[2]], [1]
        )
