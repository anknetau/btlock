#!/usr/bin/env python3
import subprocess, time, os
 
DEVICE   = "AA:BB:CC:DD:EE:FF" # device address
INTERVAL = 3 # seconds between pings
MISSES   = 2 # consecutive misses before locking
DEBUG = False

def is_locked():
    session_id = os.environ.get("XDG_SESSION_ID", "")
    result = subprocess.run(
        ["loginctl", "show-session", session_id, "--property=LockedHint", "--value"],
        capture_output=True, text=True)
    return result.stdout.strip() == "yes"
 
misses = 0
 
while True:
    time.sleep(INTERVAL)
    result = subprocess.run(["sudo", "l2ping", DEVICE, "-t", "1", "-c", "1"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    found = result.returncode == 0
    locked = is_locked()
    if DEBUG:
        print("locked=" + str(locked) + " misses=" + str(misses) + " found=" + str(found))
    if found:
        if locked:
            if DEBUG:
                print("unlocking")
            os.system("loginctl unlock-session")
        misses = 0
    else:
        misses += 1
        if misses >= MISSES and not locked:
            if DEBUG:
                print("locking")
            os.system("loginctl lock-session")
            misses = 0
