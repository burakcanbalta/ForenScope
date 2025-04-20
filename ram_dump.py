import platform
import subprocess
from datetime import datetime
from pathlib import Path
import shutil

def dump_ram(output_dir):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(output_dir) / f"ram_dump_{timestamp}.bin"
    system_platform = platform.system().lower()

    print("[*] Dumping RAM memory...")

    try:
        if system_platform == "windows":
            print("[!] RAM dump requires external tool on Windows.")
            output_path.write_text("[ERROR] Windows RAM dump tool not implemented.")
        elif system_platform == "linux":
            if shutil.which("dd"):
                subprocess.run(["sudo", "dd", "if=/dev/mem", f"of={output_path}", "bs=1M", "count=100"], check=False)
            else:
                output_path.write_text("[ERROR] 'dd' not available.")
        elif system_platform == "darwin":
            output_path.write_text("[INFO] macOS does not allow userland RAM dumping.")
        else:
            output_path.write_text("[ERROR] Unsupported OS")
    except Exception as e:
        output_path.write_text(f"[EXCEPTION] RAM dump failed: {e}")

    print(f"[+] RAM dump saved to: {output_path}")
