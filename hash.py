import hashlib
from pathlib import Path
import csv

raw_folder = Path("data/raw")
csv_path = Path("data/checksums.csv")

# CSV başlığı
with open(csv_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "sha256"])

# Dosyaları oku ve hashle
for file_path in raw_folder.iterdir():
    if file_path.is_file():
        h = hashlib.sha256()
        with open(file_path, "rb") as file:
            while chunk := file.read(8192):
                h.update(chunk)
        hash_value = h.hexdigest()

        with open(csv_path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([file_path.name, hash_value])
        
        print(f"{file_path.name} hashlendi -> {hash_value}")

print(f"SHA-256 hashleri kaydedildi: {csv_path}")
