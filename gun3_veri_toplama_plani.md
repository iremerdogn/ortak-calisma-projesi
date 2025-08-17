# Gün 3 — Veri Toplama Planı ve "Ground Truth" Stratejisi

## Amaç
Test veri seti tasarımı ve ground truth doğrulama stratejisinin hazırlanması.

## Yapılacaklar
- **Ses kayıtları:**  
  - 3 farklı ortamda (sessiz, ofis, dış mekân) 10’ar dakikalık kayıt.  
- **Video kayıtları:**  
  - LED aydınlatma altında 5–10 dk, hem 30 fps hem 60 fps kayıt.  
- **Fotoğraf (opsiyonel):**  
  - LED altında seri çekim.  
- **Çapraz doğrulama:**  
  - İki cihazla eşzamanlı kayıt senaryosu.

## Dosya Adlandırma Standardı
- Ses: `ses_<ortam>_<dakika>.wav`  
  - Örn: `ses_ofis_10dk.wav`  
- Video: `video_LED_<fps>_<dakika>.mp4`  
  - Örn: `video_LED_60fps_5dk.mp4`  
- Fotoğraf: `foto_LED_seri_<id>.jpg`  
  - Örn: `foto_LED_seri_01.jpg`

## Çıktı / Kanıt
- Veri toplama protokolü dokümanı hazırlandı.  
- Dosya adlandırma standardı belirlendi.  

## Kabul
- Protokol onaylandı.  
- Çekim takvimi belirlendi.  
