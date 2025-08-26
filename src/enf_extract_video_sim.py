import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Parametreler ---
duration_sec = 10       # Video süresi (saniye)
fps = 30                # Frame per second
frames = duration_sec * fps

# --- Simüle edilen LED flicker sinyali ---
# 50 Hz sinyal, 100 Hz örnekleme yerine fps ile örneklenmiş
t = np.arange(frames) / fps
led_signal = 0.5 * (1 + np.sin(2 * np.pi * 50 * t))  # 0-1 arası parlaklık

# --- Gürültü ekleyelim (opsiyonel) ---
noise = np.random.normal(0, 0.05, size=frames)
led_signal_noisy = led_signal + noise

# --- STFT benzeri basit tepe tespiti (frame başına max) ---
enf_raw = led_signal_noisy  # burada gerçek algoritma STFT kullanır

# --- 1 Hz’e indirgeme (medyan + downsample) ---
from scipy.signal import medfilt, resample
enf_med = medfilt(enf_raw, kernel_size=3)
enf_1hz = resample(enf_med, duration_sec)  # 10 sn -> 1 Hz örnekleme

# --- Zaman dizisi ---
time_1hz = np.arange(len(enf_1hz))

# --- CSV kaydet ---
df = pd.DataFrame({'Time (s)': time_1hz, 'ENF (Hz)': enf_1hz})
df.to_csv("docs/video1_enf_1hz.csv", index=False)
print("Simüle edilmiş ENF CSV kaydedildi: docs/video1_enf_1hz.csv")

# --- Grafik ---
plt.figure(figsize=(8,4))
plt.plot(time_1hz, enf_1hz, label="Simüle ENF")
plt.title("Video1 Simüle ENF (1 Hz)")
plt.xlabel("Zaman (s)")
plt.ylabel("ENF (Hz)")
plt.legend()
plt.savefig("docs/video1_enf_example.png")
plt.show()
print("Grafik kaydedildi: docs/video1_enf_example.png")
