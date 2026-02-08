#!/usr/bin/env python3
"""Check disk space usage on all mounted filesystems."""

import os
import json
import shutil

WARNING_THRESHOLD = 80
CRITICAL_THRESHOLD = 95


def get_mount_points():
    """Get list of mount points from /proc/mounts (Linux)."""
    mount_points = []
    try:
        with open("/proc/mounts", "r") as f:
            for line in f:
                parts = line.split()
                if len(parts) >= 2:
                    device, mount = parts[0], parts[1]
                    # Skip virtual filesystems
                    if device.startswith("/dev/"):
                        mount_points.append(mount)
    except FileNotFoundError:
        # Fallback: just check root
        mount_points = ["/"]
    return mount_points


def check_disk_usage():
    """Check disk usage for all mount points."""
    results = []
    mount_points = get_mount_points()

    for mount in mount_points:
        try:
            usage = shutil.disk_usage(mount)
            percent_used = (usage.used / usage.total) * 100

            status = "ok"
            if percent_used >= CRITICAL_THRESHOLD:
                status = "critical"
            elif percent_used >= WARNING_THRESHOLD:
                status = "warning"

            results.append({
                "mount": mount,
                "total_gb": round(usage.total / (1024**3), 2),
                "used_gb": round(usage.used / (1024**3), 2),
                "free_gb": round(usage.free / (1024**3), 2),
                "percent_used": round(percent_used, 1),
                "status": status,
            })
        except PermissionError:
            results.append({
                "mount": mount,
                "error": "Permission denied",
                "status": "unknown",
            })

    return results


def main():
    results = check_disk_usage()

    has_warnings = any(r.get("status") in ("warning", "critical") for r in results)

    print(json.dumps({"filesystems": results}, indent=2))

    if has_warnings:
        print("\n--- ALERTS ---")
        for r in results:
            if r.get("status") == "critical":
                print(f"CRITICAL: {r['mount']} is {r['percent_used']}% full!")
            elif r.get("status") == "warning":
                print(f"WARNING: {r['mount']} is {r['percent_used']}% full")


if __name__ == "__main__":
    main()
