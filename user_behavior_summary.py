import re
import json
from pathlib import Path
from datetime import datetime

def analyze_behavior(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    findings = []
    patterns = ["eval", "exec", "base64", "curl", "wget", "powershell", "Invoke-Expression", "cmd.exe", "/bin/bash", "token", "key"]
    for f in Path(output_dir).rglob("*.txt"):
        try:
            lines = f.read_text(errors="ignore").splitlines()
            for i, line in enumerate(lines):
                for kw in patterns:
                    if kw in line:
                        findings.append({"file": str(f), "line": i+1, "keyword": kw, "content": line.strip()})
        except:
            continue
    out = Path(output_dir) / f"behavior_summary_{timestamp}.json"
    out.write_text(json.dumps(findings, indent=4))
    print(f"[+] Behavior summary saved to {out}")
