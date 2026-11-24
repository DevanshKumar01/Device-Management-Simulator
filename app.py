import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path

from core.device_manager import DeviceManager
from core.metrics import Metrics
from core.cpu_scheduling import CPUScheduler
from core.memory_management import MemoryManager
from core.disk_scheduling import DiskScheduler
from core.deadlock import DeadlockManager


st.set_page_config(
    page_title="Device Management Simulator",
    page_icon="💻",
    layout="wide"
)

st.markdown("""
<style>
    [data-testid="stMetric"] {
        background-color: rgba(128,128,128,0.08);
        border: 1px solid rgba(128,128,128,0.2);
        padding: 20px;
        border-radius: 12px;
    }
    .block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)


if "manager" not in st.session_state:
    st.session_state.manager = DeviceManager()

manager = st.session_state.manager


# SIDEBAR

st.sidebar.title("💻 OS Simulator")
st.sidebar.caption("Operating System | ENCS351")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Overview",
        "🖨️ Device Management",
        "⚙️ CPU Scheduling",
        "🧠 Memory Management",
        "💽 Disk Scheduling",
        "🔒 Deadlock Management",
        "📊 Performance Analysis",
        "📋 Activity Logs",
        "💻 System Information"
    ]
)

st.sidebar.divider()
st.sidebar.info("Python + Bash Integrated Capstone Project")


# OVERVIEW

if page == "🏠 Overview":

    st.title("Device Management Simulator")
    st.caption("Integrated Operating System Resource Management")

    summary = Metrics.system_summary(manager)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Devices", summary["Total Devices"])
    c2.metric("Active Requests", summary["Active Requests"])
    c3.metric("Waiting Requests", summary["Waiting Requests"])
    c4.metric("Completed", summary["Completed Requests"])

    st.subheader("Device Status")

    st.dataframe(
        pd.DataFrame(manager.get_all_devices()),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Device Utilization")

    df = pd.DataFrame(Metrics.get_all_metrics(manager))

    fig = px.bar(
        df,
        x="Device",
        y="Utilization (%)",
        color="Device",
        text_auto=True
    )

    fig.update_yaxes(range=[0, 100])

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Integrated OS Modules")

    c1, c2, c3 = st.columns(3)

    c1.info("🖨️ Device Management\n\nAllocation, buffering and spooling")
    c2.info("⚙️ CPU Scheduling\n\nFCFS, SJF and Round Robin")
    c3.info("🧠 Memory Management\n\nFIFO, LRU and Optimal")

    c1, c2 = st.columns(2)

    c1.info("💽 Disk Scheduling\n\nFCFS, SSTF, SCAN and C-SCAN")
    c2.info("🔒 Deadlock Management\n\nBanker's Algorithm")


# DEVICE MANAGEMENT

elif page == "🖨️ Device Management":

    st.title("🖨️ Device Management")

    algorithm = st.selectbox(
        "Request Scheduling Algorithm",
        ["FCFS", "PRIORITY"],
        index=0 if manager.algorithm == "FCFS" else 1
    )

    if algorithm != manager.algorithm:
        manager.set_algorithm(algorithm)

    device_id = st.selectbox(
        "Select Device",
        list(manager.devices.keys()),
        format_func=lambda x: manager.devices[x].name
    )

    device = manager.devices[device_id]

    c1, c2, c3 = st.columns(3)

    c1.metric("Status", device.status)
    c2.metric("Waiting Requests", len(device.queue))
    c3.metric("Buffer Items", len(device.buffer))

    tab1, tab2, tab3, tab4 = st.tabs([
        "Allocate",
        "Release",
        "Buffer",
        "Print Spooling"
    ])

    with tab1:

        process_id = st.text_input(
            "Process ID",
            placeholder="P1"
        )

        priority = st.number_input(
            "Priority (1 = Highest)",
            min_value=1,
            max_value=5,
            value=3
        )

        if st.button("Request Device"):

            try:
                result = manager.request_device(
                    device_id,
                    process_id,
                    int(priority)
                )

                st.info(result)

            except ValueError as e:
                st.error(str(e))

    with tab2:

        if device.owners:

            owner = st.selectbox(
                "Select Process",
                device.owners
            )

            if st.button("Release Device"):

                try:
                    st.success(
                        manager.release_device(device_id, owner)
                    )

                except ValueError as e:
                    st.error(str(e))

        else:
            st.info("No active owners")

    with tab3:

        data = st.text_input("Buffer Data")

        if st.button("Add to Buffer"):

            try:
                st.info(manager.add_to_buffer(device_id, data))

            except ValueError as e:
                st.error(str(e))

        if st.button("Process Buffer"):
            st.info(manager.process_buffer(device_id))

        st.write("Buffer Contents:", list(device.buffer))

    with tab4:

        document = st.text_input("Document Name")

        if st.button("Add Print Job"):

            try:
                st.info(manager.spool_print_job(document))

            except ValueError as e:
                st.error(str(e))

        if st.button("Print Next Document"):
            st.info(manager.process_buffer("D1"))

        st.write(
            "Print Spool:",
            list(manager.devices["D1"].buffer)
        )

    st.subheader("All Devices")

    st.dataframe(
        pd.DataFrame(manager.get_all_devices()),
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Waiting Queue")

    if device.queue:
        st.dataframe(
            pd.DataFrame(list(device.queue)),
            use_container_width=True
        )
    else:
        st.info("Waiting queue is empty")

    if st.button("Reset Device Simulator"):
        manager.reset()
        st.rerun()


# CPU SCHEDULING

elif page == "⚙️ CPU Scheduling":

    st.title("⚙️ CPU Scheduling Simulator")

    default = pd.DataFrame({
        "pid": ["P1", "P2", "P3"],
        "arrival": [0, 0, 0],
        "burst": [5, 3, 2]
    })

    edited = st.data_editor(
        default,
        num_rows="dynamic",
        use_container_width=True
    )

    quantum = st.number_input(
        "Round Robin Time Quantum",
        min_value=1,
        max_value=100,
        value=2
    )

    if st.button("Run CPU Simulation"):

        try:

            processes = []

            for row in edited.to_dict("records"):

                if pd.isna(row["pid"]):
                    raise ValueError("Process ID is required")

                for key in ["arrival", "burst"]:
                    value = row[key]

                    if pd.isna(value) or int(value) != value:
                        raise ValueError("Times must be integers")

                processes.append({
                    "pid": str(row["pid"]).strip(),
                    "arrival": int(row["arrival"]),
                    "burst": int(row["burst"])
                })

            results = {
                "FCFS": CPUScheduler.fcfs(processes),
                "SJF": CPUScheduler.sjf(processes),
                "Round Robin": CPUScheduler.round_robin(
                    processes, int(quantum)
                )
            }

            comparison = []

            for name, result in results.items():

                st.subheader(name)

                st.dataframe(
                    pd.DataFrame(result["results"]),
                    use_container_width=True
                )

                fig = go.Figure()

                for segment in result["gantt"]:

                    fig.add_trace(go.Bar(
                        x=[segment["End"] - segment["Start"]],
                        y=["CPU"],
                        base=[segment["Start"]],
                        orientation="h",
                        name=segment["Process"],
                        text=segment["Process"],
                        textposition="inside"
                    ))

                fig.update_layout(
                    barmode="overlay",
                    xaxis_title="Time Units",
                    height=220
                )

                st.plotly_chart(fig, use_container_width=True)

                comparison.append({
                    "Algorithm": name,
                    "Average Waiting": result["average_waiting"],
                    "Average Turnaround": result["average_turnaround"]
                })

            df = pd.DataFrame(comparison)

            st.subheader("Algorithm Comparison")

            st.dataframe(df, use_container_width=True)

            st.plotly_chart(
                px.bar(
                    df,
                    x="Algorithm",
                    y=["Average Waiting", "Average Turnaround"],
                    barmode="group"
                ),
                use_container_width=True
            )

        except (ValueError, TypeError, OverflowError) as e:
            st.error(str(e))


# MEMORY MANAGEMENT

elif page == "🧠 Memory Management":

    st.title("🧠 Memory Management Simulator")

    reference = st.text_input(
        "Page Reference String",
        "7 0 1 2 0 3 0 4 2 3 0 3 2"
    )

    frames = st.number_input(
        "Number of Frames",
        min_value=1,
        max_value=20,
        value=3
    )

    if st.button("Run Memory Simulation"):

        try:

            pages = [
                int(x)
                for x in reference.replace(",", " ").split()
            ]

            comparison = MemoryManager.compare(
                pages, int(frames)
            )

            df = pd.DataFrame(comparison)

            st.dataframe(df, use_container_width=True)

            st.plotly_chart(
                px.bar(
                    df,
                    x="Algorithm",
                    y=["Page Hits", "Page Faults"],
                    barmode="group"
                ),
                use_container_width=True
            )

            for algorithm in ["FIFO", "LRU", "OPTIMAL"]:

                with st.expander(f"{algorithm} Execution Trace"):

                    result = MemoryManager.simulate(
                        pages,
                        int(frames),
                        algorithm
                    )

                    st.dataframe(
                        pd.DataFrame(result["history"]),
                        use_container_width=True
                    )

        except ValueError as e:
            st.error(str(e))


# DISK SCHEDULING

elif page == "💽 Disk Scheduling":

    st.title("💽 Disk Scheduling Simulator")

    requests_input = st.text_input(
        "Disk Requests",
        "98,183,37,122,14,124,65,67"
    )

    disk_size = st.number_input(
        "Disk Size",
        min_value=1,
        value=200
    )

    head = st.number_input(
        "Initial Head Position",
        min_value=0,
        value=53
    )

    if st.button("Run Disk Simulation"):

        try:

            requests = [
                int(x)
                for x in requests_input.replace(",", " ").split()
            ]

            comparison = DiskScheduler.compare(
                requests,
                int(head),
                int(disk_size)
            )

            df = pd.DataFrame(comparison)

            st.dataframe(df, use_container_width=True)

            st.plotly_chart(
                px.bar(
                    df,
                    x="Algorithm",
                    y="Total Head Movement",
                    color="Algorithm"
                ),
                use_container_width=True
            )

            algorithms = {
                "FCFS": DiskScheduler.fcfs,
                "SSTF": DiskScheduler.sstf,
                "SCAN": DiskScheduler.scan,
                "C-SCAN": DiskScheduler.cscan
            }

            for name, function in algorithms.items():

                result = function(
                    requests,
                    int(head),
                    int(disk_size)
                )

                st.subheader(name)

                path = result["path"]

                fig = px.line(
                    x=list(range(len(path))),
                    y=path,
                    markers=True,
                    labels={
                        "x": "Movement Step",
                        "y": "Cylinder Position"
                    }
                )

                st.plotly_chart(fig, use_container_width=True)

        except ValueError as e:
            st.error(str(e))


# DEADLOCK MANAGEMENT

elif page == "🔒 Deadlock Management":

    st.title("🔒 Deadlock Management")
    st.caption("Banker's Algorithm Safety Check")

    allocation_input = st.text_area(
        "Allocation Matrix",
        "[[0,1,0],[2,0,0],[3,0,2],[2,1,1],[0,0,2]]"
    )

    maximum_input = st.text_area(
        "Maximum Matrix",
        "[[7,5,3],[3,2,2],[9,0,2],[2,2,2],[4,3,3]]"
    )

    available_input = st.text_input(
        "Available Resources",
        "[3,3,2]"
    )

    if st.button("Check System Safety"):

        try:

            allocation = json.loads(allocation_input)
            maximum = json.loads(maximum_input)
            available = json.loads(available_input)

            if not all(isinstance(x, list) for x in [
                allocation, maximum, available
            ]):
                raise ValueError("Inputs must be lists")

            if not all(
                isinstance(row, list)
                for row in allocation + maximum
            ):
                raise ValueError("Matrices must contain rows")

            result = DeadlockManager.bankers_algorithm(
                allocation,
                maximum,
                available
            )

            if result["safe"]:

                st.success("System is in a Safe State")

                st.write(
                    "Safe Sequence:",
                    " → ".join(result["safe_sequence"])
                )

            else:

                st.error("System is in an Unsafe State")

                st.write(
                    "Unfinished Processes:",
                    result["unfinished_processes"]
                )

            st.subheader("Need Matrix")

            st.dataframe(
                pd.DataFrame(result["need"]),
                use_container_width=True
            )

            st.subheader("Execution Trace")

            st.dataframe(
                pd.DataFrame(result["history"]),
                use_container_width=True
            )

        except (ValueError, TypeError) as e:
            st.error(str(e))


# PERFORMANCE ANALYSIS

elif page == "📊 Performance Analysis":

    st.title("📊 Performance Analysis")

    summary = Metrics.system_summary(manager)

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Requests", summary["Total Requests"])

    c2.metric(
        "System Utilization",
        f'{summary["System Utilization (%)"]}%'
    )

    c3.metric(
        "Completion Rate",
        f'{summary["Completion Rate (%)"]}%'
    )

    df = pd.DataFrame(Metrics.get_all_metrics(manager))

    st.dataframe(df, use_container_width=True)

    st.plotly_chart(
        px.bar(
            df,
            x="Device",
            y=[
                "Active Requests",
                "Waiting Requests",
                "Completed Requests"
            ],
            barmode="group"
        ),
        use_container_width=True
    )

    st.plotly_chart(
        px.bar(
            df,
            x="Device",
            y=["Utilization (%)", "Buffer Usage (%)"],
            barmode="group"
        ),
        use_container_width=True
    )

    st.download_button(
        "Download Performance Report",
        df.to_csv(index=False),
        "performance_report.csv",
        "text/csv"
    )


# ACTIVITY LOGS

elif page == "📋 Activity Logs":

    st.title("📋 Activity Logs")

    logs = manager.get_logs()

    if logs:

        df = pd.DataFrame(logs)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Activity Logs",
            df.to_csv(index=False),
            "activity_logs.csv",
            "text/csv"
        )

    else:
        st.info("No activity recorded yet")


# SYSTEM INFORMATION

elif page == "💻 System Information":

    st.title("💻 System Information")

    st.caption("System report generated using Bash")

    report = Path("outputs/system_info.txt")

    if report.exists():

        content = report.read_text(
            encoding="utf-8",
            errors="replace"
        )

        st.code(content, language="text")

        st.download_button(
            "Download System Report",
            content,
            "system_info.txt",
            "text/plain"
        )

    else:

        st.warning("System report not found")

        st.code(
            "bash scripts/system_info.sh",
            language="bash"
        )


st.divider()

st.caption(
    "Device Management Simulator | "
    "Operating System Capstone Project | ENCS351"
)