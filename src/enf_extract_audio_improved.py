import numpy as np
import pandas as pd
from scipy.signal import medfilt
from pathlib import Path
import matplotlib.pyplot as plt

# --- Klasörler ---
docs_folder = Path("docs")
baseline_folder = docs_folder
improved_folder = docs_folder

# --- Dosyalar ---
wav_files = [
    "src/office_phone1_20250817_001_noisy.wav.wav",
    "src/office_phone1_20250817_001_original.wav.wav",
    "src/quiet_phone1_20250817_002_original.wav.wav"
]

def load_baseline_csv(wav_file):
    base_csv = docs_folder / (Path(wav_file).stem + "_enf_1hz.csv")
    if base_csv.exists():
        return pd.read_csv(base_csv)
    else:
        return None

def improve_enf(enf_array):
    # Median filtre (window=3) ile outlier bastırma
    enf_med = medfilt(enf_array, kernel_size=3)
    # Kısa eksik değerleri lineer interpolasyonla doldur
    idx = np.arange(len(enf_med))
    mask = ~np.isnan(enf_med)
    enf_interp = np.interp(idx, idx[mask], enf_med[mask])
    return enf_interp

def snr_r2(baseline, improved):
    if baseline is None:
        return -np.inf, -1.0
    # SNR
    noise = baseline - improved
    num = np.mean(baseline**2)
    den = np.mean(noise**2)
    snr_db = 10.0 * np.log10(num / den) if den != 0 else np.inf
    # R^2
    ss_res = np.sum((baseline - improved)**2)
    ss_tot = np.sum((baseline - np.mean(baseline))**2)
    r2 = 1 - ss_res/ss_tot if ss_tot != 0 else 0.0
    return snr_db, r2

for wav_file in wav_files:
    print(f"\n=== {Path(wav_file).name} ===")
    # ENF 1 Hz CSV oku
    base_df = load_baseline_csv(wav_file)
    if base_df is None:
        print("Baseline CSV bulunamadı!")
        baseline_enf = None
        time = np.arange(11)  # varsayılan 11 örnek
    else:
        baseline_enf = base_df['enf_hz'].values
        time = base_df['time_s'].values

    # Baseline yerine rastgele örnek (örn. 50 Hz) kullanabiliriz
    if baseline_enf is None:
        enf_array = np.full(11, 50.0)
    else:
        enf_array = baseline_enf

    # ENF iyileştirme
    enf_improved = improve_enf(enf_array)

    # SNR ve R^2
    snr_val, r2_val = snr_r2(baseline_enf, enf_improved)

    # Kaydet CSV
    out_csv = improved_folder / (Path(wav_file).name + "_enf_1hz_improved.csv")
    pd.DataFrame({'ENF': enf_improved}).to_csv(out_csv, index=False)

    # Karşılaştırmalı grafik
    plt.figure(figsize=(8,4))
    x = time
    if baseline_enf is not None:
        plt.plot(x, baseline_enf, label="Baseline")
    plt.plot(x, enf_improved, label="Improved", linestyle='--')
    plt.title(f"{Path(wav_file).name} | SNR: {snr_val:.2f} dB | R²: {r2_val:.2f}")
    plt.xlabel("Zaman (s)")
    plt.ylabel("ENF (Hz)")
    plt.legend()
    out_png = improved_folder / (Path(wav_file).name + "_compare.png")
    plt.savefig(out_png)
    plt.close()
    print(f"Kaydedildi: {out_csv} | {out_png}")
