import pandas as pd
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pathlib import Path

out = Path("outputs")
charts = out / "charts"
charts.mkdir(exist_ok=True)

plt.style.use("ggplot")

# CPU Scheduling Comparison
df = pd.read_csv(out / "cpu_comparison.csv")

ax = df.set_index("Algorithm").plot(
    kind="bar",
    figsize=(10, 6),
    color=["#2563eb", "#f97316"]
)

ax.set_title("CPU Scheduling Algorithm Comparison")
ax.set_ylabel("Time Units")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(charts / "cpu_comparison.png", dpi=300)
plt.close()

# Memory Management Comparison
df = pd.read_csv(out / "memory_comparison.csv")

ax = df.set_index("Algorithm")[["Page Hits", "Page Faults"]].plot(
    kind="bar",
    figsize=(10, 6),
    color=["#16a34a", "#dc2626"]
)

ax.set_title("Page Replacement Algorithm Comparison")
ax.set_ylabel("Number of Pages")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(charts / "memory_comparison.png", dpi=300)
plt.close()

# Disk Scheduling Comparison
df = pd.read_csv(out / "disk_comparison.csv")

ax = df.set_index("Algorithm")["Total Head Movement"].plot(
    kind="bar",
    figsize=(10, 6),
    color="#7c3aed"
)

ax.set_title("Disk Scheduling Algorithm Comparison")
ax.set_ylabel("Head Movement (Cylinders)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(charts / "disk_comparison.png", dpi=300)
plt.close()

print("All performance charts generated successfully!")
