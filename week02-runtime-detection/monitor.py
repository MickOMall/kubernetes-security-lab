import psutil
import os
import time

#config
WATCHED_DIR = "/tmp"      # directory being watched
SLEEP_INTERVAL = 2        # seconds between checks

# track knwon processes 
known_pids = set(p.info['pid'] for p in psutil.process_iter(['pid', 'name']))

# track known files
known_files = set(os.listdir(WATCHED_DIR))

print("[INFO] Runtime monitoring started...")
print(f"[INFO] Watching processes and new files in {WATCHED_DIR}")

while True:
    #process
    current_pids = set(p.info['pid'] for p in psutil.process_iter(['pid', 'name']))
    new_pids = current_pids - known_pids
    if new_pids:
        for p in psutil.process_iter(['pid', 'name']):
            if p.info['pid'] in new_pids:
                print(f"[ALERT] New process detected: PID={p.info['pid']} NAME={p.info['name']}")
    known_pids = current_pids

    #file
    current_files = set(os.listdir(WATCHED_DIR))
    new_files = current_files - known_files
    if new_files:
        for f in new_files:
            print(f"[ALERT] New file detected in {WATCHED_DIR}: {f}")
    known_files = current_files

    time.sleep(SLEEP_INTERVAL)


