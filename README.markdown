# Ransomware Simulation Project

This project simulates a ransomware attack and its mitigation in a controlled lab environment. It covers five stages: Action (Encryption), Infection (Phishing Email), Monitoring, Detection, and Mitigation. The project is implemented using Python scripts and Linux commands, tested in a virtual machine to ensure safety.

## Prerequisites

- **Operating System**: Linux (e.g., Ubuntu, Kali)
- **Python**: Version 3.6 or higher
- **Virtual Machine**: Recommended for isolation (e.g., VirtualBox, VMware)
- **Gmail Account**: For sending phishing and alert emails (requires App Password)

## Setup Instructions

1. **Install Required Libraries**:
   - Install Python libraries using pip:
     - `pycryptodome`: For AES encryption
     - `secure-smtplib`: For sending emails
     - `pyinotify`: For real-time file monitoring
     - `psutil`: For process management
   - Command: `pip3 install pycryptodome secure-smtplib pyinotify psutil`
   - Links:
     - [pycryptodome](https://pypi.org/project/pycryptodome/)
     - [secure-smtplib](https://pypi.org/project/secure-smtplib/)
     - [pyinotify](https://pypi.org/project/pyinotify/)
     - [psutil](https://pypi.org/project/psutil/)

2. **Install Third-Party Tools**:
   - Install `inotify-tools` for file change monitoring:
     - Command: `sudo apt-get install inotify-tools`
     - Link: [inotify-tools](https://github.com/inotify-tools/inotify-tools)

3. **Create Gmail App Password**:
   - Generate an App Password for Gmail to use in email scripts.
   - Instructions: Google Account > Security > 2-Step Verification > App Passwords
   - Link: [Google App Passwords](https://myaccount.google.com/security)

## Project Files

- **encrypt.py**: Encrypts files in the `~/critical` directory using AES.
- **decrypt.py**: Decrypts files using the provided key.
- **send_email.py**: Sends a phishing email with `encrypt.py` as an attachment.
- **monitor.py**: Monitors file changes in `~/critical` using `pyinotify`.
- **detect.py**: Detects ransomware patterns by analyzing file modifications.
- **mitigate.py**: Backs up files, terminates suspicious processes, and sends alerts.

## Usage Instructions

1. **Create Directory Structure**:
   - Run the following commands to create the `~/critical` folder with subfolders (`lab1`, `lab2`, `lab3`) and text files (`lab1.txt`, `lab2.txt`, `lab3.txt`):
     ```
     mkdir -p ~/critical/lab1 ~/critical/lab2 ~/critical/lab3
     echo "Lab 1 Content" > ~/critical/lab1/lab1.txt
     echo "Lab 2 Content" > ~/critical/lab2/lab2.txt
     echo "Lab 3 Content" > ~/critical/lab3/lab3.txt
     ```

2. **Action - Encryption**:
   - Run `encrypt.py` to encrypt files in `~/critical`:
     ```
     python3 encrypt.py
     ```
   - To decrypt, run `decrypt.py` with the correct key:
     ```
     python3 decrypt.py
     ```

3. **Infection - Phishing Email**:
   - Update `send_email.py` with your Gmail credentials (email and App Password).
   - Run the script to send a phishing email:
     ```
     python3 send_email.py
     ```
   - Note: Use test email accounts and run in a VM.

4. **Monitoring**:
   - Run `monitor.py` to watch for file changes in `~/critical` in real-time:
     ```
     python3 monitor.py
     ```
   - The script logs file modifications for further analysis.

5. **Detection**:
   - Run `detect.py` to identify ransomware patterns (e.g., rapid file changes):
     ```
     python3 detect.py
     ```
   - The script analyzes file hashes to detect unauthorized modifications.

6. **Mitigation**:
   - Run the script to monitor `~/critical`, back up files to `~/backups`, terminate suspicious processes.
     ```
     python3 mitigate.py
     ```

## Testing the Project

1. **Setup**: Create the directory structure and ensure all scripts are in place.
2. **Simulate Attack**:
   - Run `send_email.py` to simulate phishing.
   - Run `encrypt.py` to encrypt files.
3. **Monitor, Detect, and Mitigate**:
   - Run `monitor.py` to track file changes.
   - Run `detect.py` to identify ransomware activity.
   - Run `mitigate.py` to back up files, kill the `encrypt.py` process.
4. **Recover**:
   - Use `decrypt.py` to restore files (simulating ransom payment).
5. **Reset**:
   - Delete `~/critical` to start over:
     rm -rf ~/critical
   - Recreate the structure using the commands above.

## Notes

- **Safety**: Run all scripts in a virtual machine to avoid accidental damage.
- **Email**: Use Gmail App Passwords, not regular passwords. Test with disposable or test email accounts (e.g., `stupiduser7969@gmail.com`, `adversary112@gmail.com`).
- **Permissions**: Ensure read/write access to `~/critical` and `~/backups`. Use `sudo` for `mitigate.py` if process termination fails.
- **Educational Use**: This project is for learning purposes only. Do not use it to harm systems or networks.

## Troubleshooting

- **Permission Denied**: Check folder permissions (`chmod -R u+w ~/critical`) or run scripts with `sudo`.
- **Email Errors**: Verify Gmail App Password and SMTP settings. Test email sending with a standalone script.
- **Monitoring Issues**: Ensure `inotify-tools` is installed and test with `inotifywait -m ~/critical -e modify`.
- **Detection Failures**: Check `detect.py` logs for hash mismatches or adjust polling intervals.

## Future Enhancements

- Add a process whitelist to `mitigate.py` to avoid false positives.
- Implement cloud backups (e.g., AWS S3, Google Drive).
- Create a recovery script to restore files from `~/backups`.
- Enhance `detect.py` with machine learning for better ransomware detection.

## License
This project is for educational purposes only and is not licensed for malicious use. (University of North Texas)
