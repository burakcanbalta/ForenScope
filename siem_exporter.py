import socket
import json
from pathlib import Path
from datetime import datetime

SIEM_HOST="127.0.0.1"; SIEM_PORT=514

def send_syslog(msg):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(msg.encode(), (SIEM_HOST, SIEM_PORT))
    sock.close()

def export_latest_incident(output_dir):
    files = sorted(Path(output_dir).rglob("*.json"))[-5:]
    for f in files:
        data = json.loads(f.read_text())
        message = json.dumps({"file": str(f), "data": data})
        send_syslog(message)
        print(f"[+] Sent to SIEM: {f.name}")
