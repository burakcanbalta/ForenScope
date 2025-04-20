import platform
import subprocess
from datetime import datetime
from pathlib import Path

def collect_session_info(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = Path(output_dir) / f"sessions_{timestamp}.txt"

    system_platform = platform.system().lower()
    try:
        if system_platform in ["linux", "darwin"]:
            cmd = ["who"]
        elif system_platform == "windows":
            cmd = ["query", "user"]
        else:
            output_file.write_text("[!] Unsupported OS")
            return

        result = subprocess.check_output(cmd, universal_newlines=True)
        output_file.write_text(result)
        print(f"[+] Session info saved to {output_file}")
    except Exception as e:
        output_file.write_text(f"[!] Session info error: {e}")
