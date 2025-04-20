import re
import json
from pathlib import Path
from datetime import datetime

def search_credentials(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    findings = []
    patterns = {
        "email": r"[\w\.-]+@[\w\.-]+\.\w+",
        "token": r"(?i)(token|apikey|bearer)[\s:=']+[A-Za-z0-9\-_\.]+",
        "password": r"(?i)(pass|password|pwd)[\s:=']+[A-Za-z0-9@#$%^&+=!]+"
    }
    for f in Path(output_dir).rglob("*.txt"):
        try:
            text = f.read_text(errors="ignore")
            for key, pat in patterns.items():
                matches = re.findall(pat, text)
                if matches:
                    findings.append({"file": str(f), "type": key, "matches": list(set(matches))})
        except:
            continue
    if findings:
        out = Path(output_dir) / f"credentials_{timestamp}.json"
        out.write_text(json.dumps(findings, indent=4))
        print(f"[+] Credentials report saved to {out}")
    else:
        print("[-] No credentials found.")
