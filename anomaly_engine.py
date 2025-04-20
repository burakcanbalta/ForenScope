import numpy as np
from sklearn.ensemble import IsolationForest
from pathlib import Path
from datetime import datetime
import json

def extract_features_from_logs(folder):
    arr = []
    for f in sorted(Path(folder).glob("incident_*/**/*.txt")):
        size = f.stat().st_size
        lines = sum(1 for _ in open(f, 'r', errors='ignore'))
        arr.append([size, lines, size/lines if lines else 0])
    return np.array(arr)

def run_anomaly_detection(output_dir):
    data = extract_features_from_logs(output_dir)
    if data.shape[0] < 5:
        print("[!] Not enough data")
        return
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(data)
    scores = model.decision_function(data)
    labels = model.predict(data)
    out = []
    for idx, p in enumerate(sorted(Path(output_dir).glob("incident_*"))[:len(scores)]):
        out.append({"incident": p.name, "risk_score": float(abs(scores[idx])), "suspicious": labels[idx]==-1})
    path = Path(output_dir) / f"risk_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(path, "w") as f:
        json.dump(out, f, indent=4)
    print(f"[+] Anomaly scoring saved to {path}")

