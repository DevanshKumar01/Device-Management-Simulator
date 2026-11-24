#!/usr/bin/env bash

set -e

cd "$(dirname "$0")/.."

mkdir -p outputs

{
    echo "===================================="
    echo "       SYSTEM RESOURCE REPORT"
    echo "===================================="

    echo "Generated: $(date)"

    echo ""
    echo "Operating System:"
    uname -a

    echo ""
    echo "Disk Usage:"
    df -h

    echo ""
    echo "Memory Information:"

    if command -v free >/dev/null 2>&1; then
        free -h
    elif command -v powershell.exe >/dev/null 2>&1; then
        powershell.exe -NoProfile -Command \
        'Get-CimInstance Win32_OperatingSystem | Select-Object TotalVisibleMemorySize,FreePhysicalMemory'
    else
        echo "Memory information unavailable"
    fi

    echo ""
    echo "Running Processes:"
    ps -e

    echo ""
    echo "Report generated successfully."

} | tee outputs/system_info.txt