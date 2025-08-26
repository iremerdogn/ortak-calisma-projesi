from pathlib import Path
import csv
import datetime
import getpass
import hashlib

raw_folder = Path("data/raw")
log_file = Path("data/chain_of_custody.csv")

user = getpass.getuser()
timestamp = datetime.datetime.now().isoformat()

with open(log_file, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["filename", "sha256", "user", "timestamp"])
    
    for file_path in raw_folder.iterdir():
        if file_path.is_file():
            # SHA-256 hash hesapla
            h = hashlib.sha256()
            with open(file_path, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            sha256 = h.hexdigest()
            
            writer.writerow([file_path.name, sha256, user, timestamp])
            print(f"{file_path.name} loglandı -> {log_file}")

print(f"Chain-of-custody log dosyası oluşturuldu: {log_file}")
