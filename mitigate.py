import pyinotify
import os
import shutil
import datetime
import psutil
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
MONITOR_DIR = os.path.expanduser("~/critical")  # Directory to monitor
BACKUP_DIR = os.path.expanduser("~/backups")    # Backup directory
SENDER_EMAIL = "stupiduser7969@gmail.com"      # Your Gmail address
RECEIVER_EMAIL = "adversary112@gmail.com"      # Admin email for alerts
EMAIL_PASSWORD = "fdwy bmzp aeui fgoy"         # Your Gmail App Password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

def ensure_backup_directory():
    """Ensure the backup directory exists."""
    try:
        if not os.path.exists(BACKUP_DIR):
            os.makedirs(BACKUP_DIR)
            logger.info(f"Created backup directory: {BACKUP_DIR}")
    except Exception as e:
        logger.error(f"Failed to create backup directory: {e}")

def backup_file(filepath):
    """Backup a single file to the backup directory with a timestamp."""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        relative_path = os.path.relpath(filepath, os.path.expanduser("~"))
        backup_path = os.path.join(BACKUP_DIR, f"{timestamp}_{relative_path.replace('/', '_')}")
        backup_dir = os.path.dirname(backup_path)
        
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        shutil.copy2(filepath, backup_path)
        logger.info(f"Backed up: {filepath} to {backup_path}")
    except Exception as e:
        logger.error(f"Failed to backup {filepath}: {e}")

def backup_directory():
    """Backup all files in the monitored directory."""
    ensure_backup_directory()
    try:
        for root, _, files in os.walk(MONITOR_DIR):
            for file in files:
                filepath = os.path.join(root, file)
                backup_file(filepath)
        logger.info("Initial backup completed.")
    except Exception as e:
        logger.error(f"Failed to backup directory: {e}")

def send_alert_email(filename, process_name, pid):
    """Send an email alert to the admin about suspicious activity."""
    subject = "Ransomware Alert: Suspicious File Modification Detected"
    body = (f"Suspicious activity detected!\n\n"
            f"File modified: {filename}\n"
            f"Process: {process_name} (PID: {pid})\n"
            f"Action: Process terminated and file backed up.\n"
            f"Please investigate immediately.")

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        logger.info("Alert email sent to admin.")
    except Exception as e:
        logger.error(f"Failed to send alert email: {e}")

def kill_suspicious_process(filename):
    """Identify and kill the process modifying the file."""
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            if not proc.is_running():
                continue
            open_files = proc.open_files() or []
            for file in open_files:
                if file.path == filename:
                    logger.warning(f"Suspicious process detected: {proc.name()} (PID: {proc.pid}) modifying {filename}")
                    backup_file(filename)  # Backup before termination
                    send_alert_email(filename, proc.name(), proc.pid)
                    proc.terminate()  # Try graceful termination first
                    try:
                        proc.wait(timeout=3)  # Wait for termination
                    except psutil.TimeoutExpired:
                        proc.kill()  # Force kill if it doesn't terminate
                    logger.info(f"Terminated process: {proc.name()} (PID: {proc.pid})")
                    return
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue

class FileChangeHandler(pyinotify.ProcessEvent):
    """Handle file modification events."""
    def process_IN_MODIFY(self, event):
        filepath = event.pathname
        logger.info(f"Modification detected: {filepath}")
        kill_suspicious_process(filepath)

def monitor_directory():
    """Monitor the directory for file modifications using pyinotify."""
    try:
        wm = pyinotify.WatchManager()
        handler = FileChangeHandler()
        notifier = pyinotify.Notifier(wm, handler)
        wm.add_watch(MONITOR_DIR, pyinotify.IN_MODIFY, rec=True)
        logger.info(f"Starting monitoring of {MONITOR_DIR}...")
        
        # Perform initial backup
        backup_directory()
        
        notifier.loop()
    except Exception as e:
        logger.error(f"Monitoring failed: {e}")
    finally:
        logger.info("Monitoring stopped.")

if __name__ == "__main__":
    monitor_directory()
