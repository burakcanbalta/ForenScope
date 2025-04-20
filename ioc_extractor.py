import re
import json
from pathlib import Path
from datetime import datetime

def scan_for_iocs(output_dir):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    target_files = sorted(Path(output_dir).glob("incident_*/**/*.*"))
    patterns = {
        "ipv4": r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b",
        "domains": r"\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b",
        "urls": r"https?://[\w\.-]+(?:/[\w\.-]*)*",
        "hashes": r"\b[a-fA-F0-9]{32,64}\b",
        "emails": r"[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}"
    }
    result = {k: [] for k in patterns}
    for file in target_files:
        try:
            text = open(file, "r", errors="ignore").read() 
            for key, pat in patterns.items():
                result[key].extend(re.findall(pat, text))
        except:
            continue
    result = {k: sorted(set(v)) for k, v in result.items() if v}
    out = Path(output_dir) / f"ioc_report_{timestamp}.json"
    with open(out, "w") as f:
        json.dump(result, f, indent=4)
    print(f"[+] IOC scan complete. Saved to {out}")
