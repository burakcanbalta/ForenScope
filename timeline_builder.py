import json
from pathlib import Path
from datetime import datetime

def build_timeline(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    entries = []
    for f in Path(output_dir).rglob("*"):
        if f.is_file():
            stat = f.stat()
            entries.append({
                "file": str(f),
                "created": datetime.fromtimestamp(stat.st_ctime).isoformat(),
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "size": stat.st_size
            })
    entries.sort(key=lambda e: e["modified"])
    out = Path(output_dir) / f"timeline_{timestamp}.json"
    out.write_text(json.dumps(entries, indent=4))
    print(f"[+] Timeline generated at {out}")
