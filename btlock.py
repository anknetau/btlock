#!/usr/bin/env python3
import subprocess, time, os
 
DEVICE   = "AA:BB:CC:DD:EE:FF" # your device MAC address
INTERVAL = 3 # seconds between pings
MISSES   = 2 # consecutive misses before locking

def is_locked():
    result = subprocess.run(["loginctl", "show-session", "self", "--property=LockedHint"],
                            capture_output=True, text=True)
    return "LockedHint=yes" in result.stdout
 
misses = 0
 
while True:
    time.sleep(INTERVAL)
    result = subprocess.run(["sudo", "l2ping", DEVICE, "-t", "1", "-c", "1"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    locked = is_locked()
    if result.returncode == 0:
        if locked:
            os.system("loginctl unlock-session")
        misses = 0
    else:
        misses += 1
        if misses >= MISSES and not locked:
            os.system("loginctl lock-session")
            misses = 0
