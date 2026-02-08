#!/usr/bin/env python3
"""Collect system information and output as JSON."""

import json
import os
import platform
import socket
import subprocess


def run_cmd(cmd):
    """Run a shell command and return stripped output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception:
        return "N/A"


def get_memory_info():
    """Parse /proc/meminfo for memory stats."""
    mem = {}
    try:
        with open("/proc/meminfo", "r") as f:
            for line in f:
                parts = line.split(":")
                if len(parts) == 2:
                    key = parts[0].strip()
                    val = parts[1].strip().split()[0]  # value in kB
                    if key in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
                        mem[key] = int(val)
    except FileNotFoundError:
        return {"error": "Cannot read /proc/meminfo"}

    total = mem.get("MemTotal", 0)
    available = mem.get("MemAvailable", 0)
    return {
        "total_mb": round(total / 1024, 1),
        "available_mb": round(available / 1024, 1),
        "used_percent": round((1 - available / total) * 100, 1) if total else 0,
        "swap_total_mb": round(mem.get("SwapTotal", 0) / 1024, 1),
        "swap_free_mb": round(mem.get("SwapFree", 0) / 1024, 1),
    }


def get_cpu_info():
    """Get CPU model and core count."""
    model = "Unknown"
    try:
        with open("/proc/cpuinfo", "r") as f:
            for line in f:
                if line.startswith("model name"):
                    model = line.split(":")[1].strip()
                    break
    except FileNotFoundError:
        pass

    return {
        "model": model,
        "cores": os.cpu_count() or 0,
        "load_avg": list(os.getloadavg()),
    }


def get_network_interfaces():
    """Get IP addresses for network interfaces."""
    interfaces = []
    output = run_cmd("ip -4 -o addr show | awk '{print $2, $4}'")
    if output and output != "N/A":
        for line in output.splitlines():
            parts = line.split()
            if len(parts) == 2:
                interfaces.append({"name": parts[0], "address": parts[1]})
    return interfaces


def main():
    info = {
        "hostname": socket.gethostname(),
        "fqdn": socket.getfqdn(),
        "os": {
            "system": platform.system(),
            "release": platform.release(),
            "version": run_cmd("cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'\"' -f2") or platform.version(),
            "arch": platform.machine(),
        },
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "uptime": run_cmd("uptime -p"),
        "network": get_network_interfaces(),
        "kernel": platform.release(),
    }

    print(json.dumps(info, indent=2))


if __name__ == "__main__":
    main()
