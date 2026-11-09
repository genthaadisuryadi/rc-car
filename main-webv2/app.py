"""
RC Car Controller - Flask Backend
==================================
Menyajikan 4 jenis kontroler RC Car via web browser.
"""

import os
import httpx
from flask import Flask, render_template, request, jsonify, redirect, url_for

from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── Konfigurasi (dari .env) ──────────────────────────────────────────────
MQTT_TOPIC = os.getenv("MQTT_TOPIC")
MQTT_BROKER_WSS = os.getenv("MQTT_BROKER_WSS")

if not MQTT_TOPIC or not MQTT_BROKER_WSS:
    raise ValueError("Konfigurasi MQTT di file .env belum lengkap")
    

MQTT_TOPIC = os.getenv("MQTT_TOPIC", "muhayara/rc/rc-car-controller/car")
MQTT_BROKER_WSS = os.getenv("MQTT_BROKER_WSS", "wss://broker.rakitai.id/mqtt")


# ── Data Kontroler ─────────────────────────────────────────────────────────
CONTROLLERS = [
    {
        "id":    "button",
        "name":  "Tombol",
        "desc":  "Tekan dan tahan tombol arah untuk menggerakkan RC Car.",
        "tech":  ["MQTT", "Touch & Mouse"],
        "color": "#0057ff",
        "on_color": "#ffffff",
    },
    {
        "id":    "finger",
        "name":  "Kontrol Jari",
        "desc":  "Arahkan jari telunjuk ke zona layar. Kamera mendeteksi gerakan secara real-time.",
        "tech":  ["MediaPipe", "Kamera", "MQTT"],
        "color": "#ffd400",
        "on_color": "#0a1f44",
    },
    {
        "id":    "voice",
        "name":  "Kontrol Suara",
        "desc":  "Ucapkan perintah seperti \"maju 2\" atau \"kiri\" untuk menggerakkan mobil selama N detik.",
        "tech":  ["Web Speech API", "MQTT"],
        "color": "#0057ff",
        "on_color": "#ffffff",
    },
    {
        "id":    "voice_copy",
        "name":  "Kontrol Suara Plus",
        "desc":  "Versi suara yang ditingkatkan. belok otomatis 0.6 detik jika tidak ada angka.",
        "tech":  ["Web Speech API", "MQTT"],
        "color": "#ffd400",
        "on_color": "#0a1f44",
    },
]


# ── Routes ─────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    """Halaman utama — pilihan kontroler."""
    return render_template("index.html", controllers=CONTROLLERS)


@app.route("/controller/<controller_id>")
def controller(controller_id):
    """Halaman kontroler yang dipilih."""
    ctrl = next((c for c in CONTROLLERS if c["id"] == controller_id), None)
    if not ctrl:
        return redirect(url_for("index"))

    template = f"controllers/{controller_id}.html"
    return render_template(
        template,
        ctrl=ctrl,
        mqtt_topic=MQTT_TOPIC,
        mqtt_broker=MQTT_BROKER_WSS,
    )


# ── Entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port  = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    print(f"\n🚗  RC Car Controller berjalan di http://localhost:{port}\n")
    app.run(debug=debug, host="0.0.0.0", port=port)
