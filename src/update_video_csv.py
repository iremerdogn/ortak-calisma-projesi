import pandas as pd
import numpy as np

# Örnek ENF verisi (simülasyon)
enf_array = np.random.normal(50, 0.01, 11)  # Ortalama 50 Hz, çok küçük varyans
time_array = np.arange(len(enf_array))  # 1 Hz örnekleme → zaman dizisi

# DataFrame oluştur
df = pd.DataFrame({
    'time_s': time_array,
    'enf_hz': enf_array  # Kolon adı kesinlikle 'enf_hz'
})

# Kaydet
df.to_csv("docs/video1_enf_1hz.csv", index=False)
print("CSV güncellendi: docs/video1_enf_1hz.csv")
