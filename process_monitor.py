import psutil
import json
from datetime import datetime
from pathlib import Path

def collect_process_info(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_dir) / f"processes_{timestamp}.json"
    process_list = []

    for proc in psutil.process_iter(['pid', 'ppid', 'name', 'username', 'cmdline']):
        try:
            info = proc.info
            process_list.append({
                "pid": info.get("pid"),
                "ppid": info.get("ppid"),
                "name": info.get("name"),
                "user": info.get("username"),
                "cmdline": " ".join(info.get("cmdline", []))
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    with open(output_file, "w") as f:
        json.dump(process_list, f, indent=4)

    print(f"[+] Process info saved to {output_file}")
