import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import welch

def analyze_enf(wav_file, target_freq=50, band=5):
    sr, data = wavfile.read(wav_file)

    if len(data.shape) > 1:
        data = data[:, 0]

    freqs, psd = welch(data, sr, nperseg=4096)
    mask = (freqs >= target_freq - band) & (freqs <= target_freq + band)

    if not np.any(mask):
        print(f"[!] Hedef frekans aralığında veri yok.")
        return

    plt.figure(figsize=(8, 4))
    plt.plot(freqs[mask], psd[mask])
    plt.title(f"ENF Analizi ({target_freq} Hz civarı)")
    plt.xlabel("Frekans (Hz)")
    plt.ylabel("Güç Yoğunluğu")
    plt.grid(True)
    plt.show()

    dominant_freq = freqs[mask][np.argmax(psd[mask])]
    print(f"[+] Tespit edilen ENF frekansı: {dominant_freq:.4f} Hz")

if __name__ == "__main__":
    # --- Dosya listesi ---
    files = [
        "src/office_phone1_20250817_001_noisy.wav.wav",
        "src/office_phone1_20250817_001_original.wav.wav",
        "src/quiet_phone1_20250817_002_original.wav.wav"
    ]

    for f in files:
        print(f"\n=== Analiz: {f} ===")
        analyze_enf(f, band=5)
