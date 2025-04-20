import shutil
import subprocess
from pathlib import Path
from datetime import datetime

def secure_archive(incident_dir, password=None):
    base = Path("output")/incident_dir
    zip_name = Path("output")/f"{incident_dir}.zip"
    shutil.make_archive(str(zip_name).replace(".zip",""), 'zip', base)
    if password:
        enc = zip_name.with_name(zip_name.stem+"_encrypted.zip")
        cmd=["7z","a",str(enc),str(zip_name),f"-p{password}","-mhe=on"]
        subprocess.run(cmd,check=True)
        zip_name.unlink()
        print(f"[+] Encrypted archive: {enc}")
    else:
        print(f"[+] Archive created: {zip_name}")
