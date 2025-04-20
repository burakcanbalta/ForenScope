import platform
import shutil
import os
from datetime import datetime
from pathlib import Path

def collect_logs(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logs_dir = Path(output_dir) / f"logs_{timestamp}"
    logs_dir.mkdir(parents=True, exist_ok=True)

    system_platform = platform.system().lower()
    print("[*] Collecting system logs...")

    try:
        if system_platform == "linux":
            for log in ["/var/log/syslog", "/var/log/messages", "/var/log/auth.log"]:
                lp = Path(log)
                if lp.exists():
                    shutil.copy(lp, logs_dir / lp.name)
        elif system_platform == "darwin":
            (logs_dir / "macOS_logs.txt").write_text("Use Console.app or log show")
        elif system_platform == "windows":
            os.system(f"powershell Get-EventLog -LogName Security -Newest 1000 | Out-File -Encoding utf8 {logs_dir / 'security_log.txt'}")
        else:
            (logs_dir / "unknown_os.txt").write_text("[!] Unsupported OS")
        print(f"[+] Logs saved to {logs_dir}")
    except Exception as e:
        (logs_dir / "log_error.txt").write_text(str(e))
