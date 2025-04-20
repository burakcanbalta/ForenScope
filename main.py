import argparse
import subprocess
from datetime import datetime
from pathlib import Path
import traceback
import sqlite3
import sys

from modules.ram_dump import dump_ram
from modules.process_monitor import collect_process_info
from modules.net_monitor import collect_network_info
from modules.session_info import collect_session_info
from modules.log_collector import collect_logs
from modules.ioc_extractor import scan_for_iocs
from modules.anomaly_engine import run_anomaly_detection
from modules.user_behavior_summary import analyze_behavior
from modules.timeline_builder import build_timeline
from modules.credential_finder import search_credentials
from modules.geolocation_mapper import map_geolocation
from modules.siem_exporter import export_latest_incident
from scripts.secure_archiver import secure_archive

DB_PATH = "incident_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_name TEXT,
            timestamp TEXT,
            modules TEXT,
            secure INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def insert_incident_record(name, timestamp, modules, secure=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO incidents (incident_name, timestamp, modules, secure) VALUES (?, ?, ?, ?)",
              (name, timestamp, ",".join(modules), secure))
    conn.commit()
    conn.close()

def get_incident_folder(base="output"):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    incident_path = Path(base) / f"incident_{timestamp}"
    incident_path.mkdir(parents=True, exist_ok=True)
    return str(incident_path), timestamp

def log_message(msg):
    print(f"[ForenScope] {msg}")
    sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description="ForenScope Modular Incident Response")
    parser.add_argument("--modules", type=str, default="all",
                        help="Comma-separated modules: ram,process,net,session,logs,iocs,archive,ai,behavior,timeline,creds,geo,siem,secure")
    parser.add_argument("--password", type=str, help="Optional password for secure archive")
    args = parser.parse_args()

    modules = args.modules.split(",") if args.modules != "all" else [
        "ram", "process", "net", "session", "logs", "iocs", "archive", "ai",
        "behavior", "timeline", "creds", "geo", "siem", "secure"
    ]

    init_db()
    incident_dir, timestamp = get_incident_folder()

    try:
        if "ram" in modules:
            dump_ram(incident_dir)
        if "process" in modules:
            collect_process_info(incident_dir)
        if "net" in modules:
            collect_network_info(incident_dir)
        if "session" in modules:
            collect_session_info(incident_dir)
        if "logs" in modules:
            collect_logs(incident_dir)
        if "iocs" in modules:
            scan_for_iocs("output")
        if "ai" in modules:
            run_anomaly_detection("output")
        if "behavior" in modules:
            analyze_behavior("output")
        if "timeline" in modules:
            build_timeline("output")
        if "creds" in modules:
            search_credentials("output")
        if "geo" in modules:
            map_geolocation("output")
        if "siem" in modules:
            export_latest_incident("output")
        if "archive" in modules:
            archive_incident("output")
        secure_flag = 0
        if "secure" in modules and args.password:
            secure_archive(Path(incident_dir).name, password=args.password)
            secure_flag = 1

        insert_incident_record(Path(incident_dir).name, timestamp, modules, secure_flag)
        log_message("Incident collection complete. ✅")

    except Exception:
        log_message("[!] Error:\n" + traceback.format_exc())

if __name__ == "__main__":
    main()
