import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
import time

st.set_page_config(
    page_title="Kalite Tahmin Uygulaması",
    page_icon="📹",  # Emoji olarak da koyabilirsin
    layout="wide"
)


st.title("📱 Telefon Kamerasıyla Canlı  Kaynak Kalitesi Tespiti")
st.markdown("""
### ⚙️ Kullanım Talimatı

1. Telefonunuza **IP Webcam** uygulamasını indirin ve açın.
2. **Start server** butonuna basın.
3. Ekranda çıkan IP'yi buraya girin (örnek: `http://192.168.1.35:8080/video`).
4. "▶️ Başlat" butonuna tıklayın.

> ⚠️ Telefon ve bilgisayar aynı Wi-Fi ağına bağlı olmalıdır.
""")


# Oturum durumu başlat
if "run" not in st.session_state:
    st.session_state.run = False

# URL giriş
url = st.text_input("📡 Yayın URL'sini girin:", value="http://192.168.1.35:8080/video")

# Model
model = YOLO("best.pt")  # GPU varsa: model.to("cuda")

# Başlat ve durdur butonları
col1, col2 = st.columns(2)
with col1:
    if st.button("▶️ Başlat"):
        st.session_state.run = True
with col2:
    if st.button("⛔ Durdur"):
        st.session_state.run = False

FRAME_WINDOW = st.image([])

# Eğer 'run' durumu aktifse yayını başlat
if st.session_state.run:
    cap = cv2.VideoCapture(url)
    frame_count = 0

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            st.warning("📛 Kameradan görüntü alınamadı.")
            break

        orig_frame = frame.copy()
        small_frame = cv2.resize(frame, (320, 240))
        small_rgb = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        frame_count += 1
        if frame_count % 2 == 0:
            results = model(small_rgb, verbose=False)
            boxes = results[0].boxes

            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                conf = box.conf[0].item()
                cls = int(box.cls[0].item())
                label = model.names[cls]

                scale_x = orig_frame.shape[1] / 320
                scale_y = orig_frame.shape[0] / 240

                x1 = int(x1 * scale_x)
                y1 = int(y1 * scale_y)
                x2 = int(x2 * scale_x)
                y2 = int(y2 * scale_y)

                cv2.rectangle(orig_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(orig_frame, f"{label} {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            annotated_frame = cv2.cvtColor(orig_frame, cv2.COLOR_BGR2RGB)
            FRAME_WINDOW.image(annotated_frame, channels="RGB")

        # Kısa gecikme ekle → yoksa sistem yorulabilir
        time.sleep(0.03)

    cap.release()
    st.success("📴 Yayın durduruldu.")
