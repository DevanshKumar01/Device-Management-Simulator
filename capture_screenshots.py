from playwright.sync_api import sync_playwright
from pathlib import Path

folder = Path("screenshots")
folder.mkdir(exist_ok=True)

pages = [
    ("Overview", "01_overview.png"),
    ("Device Management", "02_device_management.png"),
    ("CPU Scheduling", "03_cpu_scheduling.png"),
    ("Memory Management", "04_memory_management.png"),
    ("Disk Scheduling", "05_disk_scheduling.png"),
    ("Deadlock Management", "06_deadlock.png"),
    ("Performance Analysis", "07_performance.png"),
    ("Activity Logs", "08_activity_logs.png"),
    ("System Information", "09_system_info.png"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
        color_scheme="dark"
    )

    page.goto("http://localhost:8501", timeout=60000)
    sidebar = page.locator('[data-testid="stSidebar"]')
    sidebar.wait_for(timeout=60000)

    for name, filename in pages:
        try:
            sidebar.get_by_text(name, exact=False).first.click(timeout=10000)
            page.wait_for_timeout(3000)

            page.evaluate("window.scrollTo(0, 0)")

            page.screenshot(
                path=str(folder / filename),
                full_page=True
            )

            print(f"SUCCESS: {filename}")

        except Exception as e:
            print(f"FAILED: {name} - {e}")

    browser.close()

print("Screenshot capture finished.")
