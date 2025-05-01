
import time
from collections import deque
from datetime import datetime

LOG_FILE = "monitor_log.txt"
THRESHOLD_COUNT = 5        # number of file changes
THRESHOLD_SECONDS = 10     # within this time window

def parse_log_line(line):
    try:
        timestamp_str, event = line.strip().split("] ", 1)
        timestamp_str = timestamp_str.strip("[").strip()
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
        return timestamp, event
    except:
        return None, None

def detect_ransomware():
    print("Starting ransomware detection...")
    recent_events = deque()

    try:
        with open(LOG_FILE, "r") as f:
            f.seek(0, 2)  # Move to the end of the file

            while True:
                line = f.readline()
                if not line:
                    time.sleep(1)
                    continue

                timestamp, event = parse_log_line(line)
                if timestamp is None:
                    continue

                recent_events.append(timestamp)

                # Remove old events outside the time window
                while recent_events and (timestamp - recent_events[0]).total_seconds() > THRESHOLD_SECONDS:
                    recent_events.popleft()

                if len(recent_events) >= THRESHOLD_COUNT:
                    print(f"[ALERT] Ransomware-like activity detected!")
                    print(f"Modified {len(recent_events)} files within {THRESHOLD_SECONDS} seconds.")
                   
                    recent_events.clear()  # Reset after alert
    except KeyboardInterrupt:
        print("Detection stopped.")

if __name__ == "__main__":
    detect_ransomware()
