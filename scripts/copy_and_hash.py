from pathlib import Path
import shutil

src_folder = Path("src")
raw_folder = Path("data/raw")
raw_folder.mkdir(parents=True, exist_ok=True)

for file_path in src_folder.iterdir():
    if file_path.is_file():
        shutil.copy(file_path, raw_folder)
        print(f"{file_path.name} kopyalandı -> {raw_folder}")
