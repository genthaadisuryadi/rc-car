# 🚗 RC Car Controller — Web Dashboard

Dashboard web untuk mengontrol RC Car via MQTT menggunakan 4 metode kontrol berbeda.

---

## Struktur Proyek

```
rc-car-controller/
├── app.py                          ← Flask backend
├── requirements.txt
├── Procfile                        ← Start command untuk hosting (gunicorn)
├── runtime.txt                     ← Versi Python untuk hosting
├── .env.example                    ← Salin ke .env dan isi konfigurasi
├── README.md
│
├── templates/
│   ├── base.html                   ← Template dasar (font, CSS)
│   ├── index.html                  ← Halaman pilihan kontroler
│   └── controllers/
│       ├── button.html             ← web_kontrolv2.html  → Kontrol tombol
│       ├── voice.html              ← kontrol.py          → Kontrol suara
│       ├── voice_copy.html         ← kontrol-copy.py     → Suara Plus (durasi otomatis)
│       └── finger.html             ← kontrol-jari.py     → Kontrol jari (MediaPipe)
│
└── static/
    └── css/
        └── style.css               ← Tema dark racing
```

---

## Cara Menjalankan (Lokal)

### 1. Install dependensi

```bash
pip install -r requirements.txt
```

### 2. Buat file konfigurasi

```bash
cp .env.example .env
```

Edit `.env`:
```
MQTT_TOPIC=
MQTT_BROKER_WSS=
PORT=5000
DEBUG=false
```

### 3. Jalankan server (dev)

```bash
python app.py
```

Buka di browser: `http://localhost:5000`

---

## Cara Deploy ke Hosting (Production)

1. *Jangan* upload folder `venv/` — hosting akan install dependency sendiri dari `requirements.txt`.
2. Set environment variables di dashboard hosting (Railway/Render/dll): `MQTT_TOPIC`, `MQTT_BROKER_WSS`, `DEBUG=false`. Jangan set `PORT` manual, platform hosting biasanya inject otomatis.
3. Start command sudah disiapkan di `Procfile`:
   ```
   web: gunicorn -w 2 -b 0.0.0.0:$PORT app:app
   ```
4. Pastikan platform hosting menyediakan **HTTPS otomatis** — wajib untuk fitur kamera (`Kontrol Jari`) dan mikrofon (`Kontrol Suara`), karena browser modern memblokir `getUserMedia`/Web Speech API di halaman non-HTTPS (kecuali `localhost`).

---

## Ringkasan 4 Kontroler

| File Asli | Route | Metode | Kebutuhan |
|---|---|---|---|
| `web_kontrolv2.html` | `/controller/button` | Tombol tekan-tahan | MQTT |
| `kontrol.py` | `/controller/voice` | Suara + regex | Mikrofon, Chrome |
| `kontrol-copy.py` | `/controller/voice_copy` | Suara + durasi otomatis belok | Mikrofon, Chrome |
| `kontrol-jari.py` | `/controller/finger` | Tracking jari MediaPipe | Kamera, Chrome |

---

## Catatan

- **Web Speech API** hanya berfungsi di **Google Chrome** atau **Microsoft Edge** (tidak di Firefox/Safari).
- **Kamera** memerlukan izin browser. HTTPS diperlukan jika deploy ke server publik.
- Semua kontroler mengirim perintah `S` (Stop) otomatis saat tab/window tidak aktif untuk keamanan.
- Broker MQTT publik (mis. `broker.hivemq.com`) tidak punya autentikasi — topic yang terlalu mudah ditebak berisiko dikirimi perintah dari luar. Untuk pemakaian serius, pertimbangkan broker private dengan username/password.

---

> **Penting:** Kamera dan mikrofon browser hanya berfungsi di HTTPS.
> Gunakan nginx + certbot, atau layanan seperti Railway / Render yang menyediakan HTTPS otomatis.
