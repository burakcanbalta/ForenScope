import platform
import subprocess
from datetime import datetime

def setup_scheduler():
    os_type=platform.system().lower()
    if os_type=="linux":
        cron=f"0 9 * * * python3 $(pwd)/main.py\n"
        with open("/etc/cron.d/forenscope","w") as f: f.write(cron)
        subprocess.run(["chmod","+x","/etc/cron.d/forenscope"])
        print("[+] Cron job set for 09:00 daily")
    elif os_type=="windows":
        subprocess.run([
            "schtasks","/Create","/SC","DAILY","/TN","ForenScope_Daily",
            "/TR",f"python %cd%\\\\main.py","/ST","09:00"
        ],check=True)
        print("[+] Scheduled Task created")
    else:
        print("[!] Unsupported OS")

if __name__=="__main__":
    setup_scheduler()
