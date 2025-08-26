import pandas as pd
import numpy as np
from scipy.signal import medfilt
from pathlib import Path
import matplotlib.pyplot as plt

# --- Klasör ---
docs_folder = Path("docs")

# --- Video dosyaları ---
video_files = [
    "video1.mp4"
]

def load_baseline_csv(video_file):
    base_csv = docs_folder / (Path(video_file).stem + "_enf_1hz.csv")
    if base_csv.exists():
        return pd.read_csv(base_csv)
    else:
        return None

def improve_enf(enf_array):
    # Median filtre ile outlier bastırma
    enf_med = medfilt(enf_array, kernel_size=3)
    # Kısa eksik değerleri lineer interpolasyonla doldur
    idx = np.arange(len(enf_med))
    mask = ~np.isnan(enf_med)
    enf_interp = np.interp(idx, idx[mask], enf_med[mask])
    return enf_interp

for video_file in video_files:
    print(f"\n=== {video_file} ===")
    base_df = load_baseline_csv(video_file)

    if base_df is None or 'enf_hz' not in base_df.columns:
        print("Baseline CSV veya 'enf_hz' kolonu bulunamadı, 50 Hz dizisi kullanılacak.")
        baseline_enf = None
        time = np.arange(11)
    else:
        baseline_enf = base_df['enf_hz'].values
        time = base_df['time_s'].values

    if baseline_enf is None:
        enf_array = np.full(11, 50.0)
    else:
        enf_array = baseline_enf

    # ENF iyileştirme
    enf_improved = improve_enf(enf_array)

    # CSV kaydet
    out_csv = docs_folder / (Path(video_file).stem + "_enf_1hz_improved.csv")
    pd.DataFrame({'time_s': time, 'enf_hz': enf_improved}).to_csv(out_csv, index=False)

    # Karşılaştırmalı grafik
    plt.figure(figsize=(8,4))
    if baseline_enf is not None:
        plt.plot(time, baseline_enf, label="Baseline")
    plt.plot(time, enf_improved, label="Improved", linestyle='--')
    plt.title(f"{video_file} | Video ENF İyileştirme")
    plt.xlabel("Zaman (s)")
    plt.ylabel("ENF (Hz)")
    plt.legend()
    out_png = docs_folder / (Path(video_file).stem + "_compare.png")
    plt.savefig(out_png)
    plt.close()
    print(f"Simüle edilmiş ENF CSV kaydedildi: {out_csv}")
    print(f"Grafik kaydedildi: {out_png}")
