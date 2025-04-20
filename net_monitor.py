import psutil
import json
from datetime import datetime
from pathlib import Path

def collect_network_info(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_dir) / f"network_{timestamp}.json"
    result = []

    for conn in psutil.net_connections():
        try:
            laddr = f"{conn.laddr.ip}:{conn.laddr.port}" if conn.laddr else ""
            raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else ""
            result.append({
                "pid": conn.pid,
                "status": conn.status,
                "type": str(conn.type),
                "local_address": laddr,
                "remote_address": raddr
            })
        except:
            continue

    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)

    print(f"[+] Network connections saved to {output_file}")
