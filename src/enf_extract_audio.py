import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfiltfilt, stft
from scipy.ndimage import median_filter
import matplotlib.pyplot as plt
from pathlib import Path
import os

# ------------------ Yardımcılar ------------------
def read_wav_mono(path):
    sr, data = wavfile.read(path)
    if data.ndim > 1:
        data = data[:, 0]
    # int -> float dönüştür
    if np.issubdtype(data.dtype, np.integer):
        maxv = np.iinfo(data.dtype).max
        data = data.astype(np.float64) / maxv
    else:
        data = data.astype(np.float64)
    return sr, data

def bandpass_filter(x, sr, low=45, high=55, order=4):
    nyq = 0.5 * sr
    sos = butter(order, [low/nyq, high/nyq], btype="bandpass", output="sos")
    return sosfiltfilt(sos, x)

def stft_peak_track_near(x, sr, target=50.0, band=(45,55), near_band=2.0,
                         nperseg=8192, noverlap=None):
    if noverlap is None:
        noverlap = nperseg // 2
    f, t, Z = stft(x, fs=sr, nperseg=nperseg, noverlap=noverlap, boundary=None)
    # Önce geniş bant (45–55)
    mask_wide = (f >= band[0]) & (f <= band[1])
    f_band = f[mask_wide]
    Z_band = Z[mask_wide, :]
    mag = np.abs(Z_band)

    # 50±near_band’e yakın tepe (örn 48–52)
    mask_near = (f_band >= (target - near_band)) & (f_band <= (target + near_band))
    if np.any(mask_near):
        f_near = f_band[mask_near]
        mag_near = mag[mask_near, :]
        idx = np.argmax(mag_near, axis=0)
        enf_curve = f_near[idx]
    else:
        # Fall-back: geniş bant içinde mutlak tepe
        idx = np.argmax(mag, axis=0)
        enf_curve = f_band[idx]
    return t, enf_curve

def resample_to_1hz(times, values, total_seconds):
    # 0..T aralığında 1 Hz zaman ekseni
    new_t = np.arange(0, int(np.floor(total_seconds)) + 1)
    # Kenar durum: tek nokta ise tekrar et
    if len(times) < 2:
        vals = np.ones_like(new_t, dtype=float) * (values[0] if len(values) else np.nan)
        return new_t, vals
    vals = np.interp(new_t, times, values)
    return new_t, vals

def smooth_curve(x, med_size=5, ma_win=7):
    x_med = median_filter(x, size=max(1, med_size))
    if ma_win <= 1:
        return x_med
    kernel = np.ones(ma_win) / ma_win
    x_smooth = np.convolve(x_med, kernel, mode='same')
    return x_smooth

def make_plots_and_save(new_t, enf_raw, enf_smooth, out_png, title):
    plt.figure(figsize=(12, 4))
    plt.plot(new_t, enf_raw, alpha=0.5, label='ENF (1 Hz)')
    plt.plot(new_t, enf_smooth, linewidth=2, label='ENF (düzgünleştirilmiş)')
    plt.axhline(50.0, linestyle='--', linewidth=1, label='50 Hz referans')
    plt.xlabel('Zaman (s)')
    plt.ylabel('Frekans (Hz)')
    plt.title(title)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.show()

# ------------------ Ana akış ------------------
if __name__ == "__main__":
    # İstersen buraya tek dosya yaz: INPUTS = ["src/office_phone1_20250817_001_original.wav.wav"]
    # Aksi halde src içindeki tüm .wav dosyalarını gezelim:
    INPUTS = sorted(str(p) for p in Path("src").glob("*.wav*"))  # *.wav ve *.wav.wav

    os.makedirs("docs", exist_ok=True)

    for wav_path in INPUTS:
        print(f"\n=== İşleniyor: {wav_path} ===")
        sr, data = read_wav_mono(wav_path)
        dur = len(data) / sr
        print(f"Örnekleme hızı: {sr} Hz, Süre: {dur:.1f} sn, Örnek sayısı: {len(data)}")

        # 1) 45–55 Hz band-pass
        x_filt = bandpass_filter(data, sr, low=45, high=55, order=4)
        print("Band-pass filtre uygulandı (45–55 Hz).")

        # 2) STFT tepe takibi (50±2 Hz öncelikli)
        t_stft, enf = stft_peak_track_near(x_filt, sr, target=50.0, band=(45,55),
                                           near_band=2.0, nperseg=8192)
        print("STFT ile 50 Hz’e yakın tepe takibi tamamlandı.")

        # 3) 1 Hz’e yeniden örnekleme
        new_t, enf_1hz = resample_to_1hz(t_stft, enf, dur)
        # 4) Düzgünleştirme
        enf_smooth = smooth_curve(enf_1hz, med_size=5, ma_win=7)

        print(f"1 Hz uzunluğu: {len(enf_1hz)} sn | Ortalama: {np.nanmean(enf_smooth):.4f} Hz | Std: {np.nanstd(enf_smooth):.4f} Hz")

        stem = Path(wav_path).stem
        out_png = f"docs/{stem}_enf.png"
        out_csv = f"docs/{stem}_enf_1hz.csv"

        # 5) Grafik ve CSV kaydet
        make_plots_and_save(new_t, enf_1hz, enf_smooth, out_png, f"ENF Eğrisi (1 Hz) — {Path(wav_path).name}")
        np.savetxt(out_csv, np.column_stack([new_t, enf_smooth]), delimiter=",", header="time_s,enf_hz", comments="")
        print(f"Kaydedildi: {out_png} | {out_csv}")

    print("\nTamamlandı. docs/ klasöründe grafikleri ve CSV’leri bulabilirsin.")

