import json
import requests
import time
from pathlib import Path
from datetime import datetime

def map_geolocation(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    ioc_file = sorted(Path(output_dir).glob("ioc_report_*.json"))[-1]
    data = json.loads(ioc_file.read_text())
    ips = data.get("ipv4", [])
    results = []
    for ip in ips:
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            if r.ok and r.json().get("status")=="success":
                info = r.json()
                results.append({
                    "ip": ip,
                    "country": info["country"],
                    "region": info["regionName"],
                    "city": info["city"],
                    "isp": info["isp"]
                })
            time.sleep(1)
        except:
            results.append({"ip": ip, "error": "lookup failed"})
    out = Path(output_dir) / f"geo_report_{timestamp}.json"
    out.write_text(json.dumps(results, indent=4))
    print(f"[+] Geolocation report saved to {out}")
