import subprocess
import datetime

def monitor_directory(directory, log_file):
    print(f"Monitoring directory: {directory} for changes...")
    try:
        # Start inotifywait subprocess
        process = subprocess.Popen(
            ["inotifywait", "-m", "-r", "-e", "modify", directory],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        with open(log_file, "a") as log:
            for line in process.stdout:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_entry = f"[{timestamp}] {line.strip()}\n"
                print(log_entry.strip())
                log.write(log_entry)
                log.flush()

    except FileNotFoundError:
        print("inotifywait not found. Please install inotify-tools.")
    except KeyboardInterrupt:
        print("Monitoring stopped.")

if __name__ == "__main__":
    monitor_directory("/home/sec-lab/hack", "monitor_log.txt")
