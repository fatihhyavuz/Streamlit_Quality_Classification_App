import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import glob
import tempfile
import shutil
import zipfile
from PIL import Image

import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Kalite Tahmin Uygulaması",
    page_icon="📹",  # Emoji olarak da koyabilirsin
    layout="wide"
)

# Logo üstte
logo = Image.open("logo2.png")
st.image(logo, width=300)

# Başlık altta
st.title("📸 Kaynak Kalite Kontrol Uygulaması")

st.markdown(
    """
    **Bir görsel veya klasör yükleyin, model kaynak kalitesini tespit etsin ve sonucu sağ tarafta görün!**  
    - Desteklenen formatlar: JPG, JPEG, PNG  
    - Model: YOLOv11 (best.pt)
    """
)

model = YOLO("best.pt")

tab1, tab2 = st.tabs(["🔍 Tekli Görsel", "📁 Klasörle Toplu Tahmin"])

# --- TABS: Tekli Yükleme ---
with tab1:
    uploaded_file = st.file_uploader("📂 Görsel Yükle", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

        col1, col2 = st.columns(2)

        with col1:
            st.header("Orijinal Görsel")
            st.image(image, use_container_width=True)

        temp_path = uploaded_file.name
        image.save(temp_path)

        results = model(temp_path, save=True)

        output_dirs = sorted(glob.glob("runs/detect/predict*"), key=os.path.getmtime, reverse=True)
        if output_dirs:
            latest_output_dir = output_dirs[0]
            predicted_img_path = os.path.join(latest_output_dir, os.path.basename(temp_path))

            with col2:
                st.header("Tahmin Sonucu")
                if os.path.exists(predicted_img_path):
                    pred_img = Image.open(predicted_img_path)
                    st.image(pred_img, use_container_width=True)
                    st.success("✅ Tahmin tamamlandı!")
                else:
                    st.error("Tahmin sonucu bulunamadı.")
        else:
            with col2:
                st.error("Tahmin klasörü bulunamadı.")
    else:
        st.info("Lütfen bir görsel yükleyin.")

# --- TABS: Klasörle Toplu Tahmin ---
with tab2:
    uploaded_files = st.file_uploader("📁 Birden fazla görsel yükle", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        temp_dir = tempfile.mkdtemp()

        for file in uploaded_files:
            img = Image.open(file).convert("RGB")
            img.save(os.path.join(temp_dir, file.name))

        with st.spinner("Görseller işleniyor..."):
            results = model(source=temp_dir, save=True)

        output_dirs = sorted(glob.glob("runs/detect/predict*"), key=os.path.getmtime, reverse=True)
        if output_dirs:
            latest_output_dir = output_dirs[0]
            st.header("📊 Toplu Tahmin Sonuçları")
            import zipfile
            import io
            pred_images = glob.glob(os.path.join(latest_output_dir, "*"))
            # --- ZIP dosyasını oluştur ---
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for img_path in pred_images:
                    zip_file.write(img_path, arcname=os.path.basename(img_path))
            zip_buffer.seek(0)
            
            # --- ZIP indirme butonu (görsellerin üstünde gösterilecek) ---
            st.download_button(
                label="📦 Tahmin Sonuçlarını ZIP Olarak İndir",
                data=zip_buffer,
                file_name="tahmin_sonuclari.zip",
                mime="application/zip"
            )
            
            cols = st.columns(2)

            for i, img_path in enumerate(pred_images):
                 with cols[i % 2]:
                     st.image(img_path, caption=os.path.basename(img_path), width=600)

            # # Klasörü zip yap
            # zip_path = shutil.make_archive(latest_output_dir, 'zip', latest_output_dir)

            # # İndirme butonu
            # with open(zip_path, "rb") as f:
            #     st.download_button(
            #         label="📥 Tahmin Sonuçlarını İndir (ZIP)",
            #         data=f,
            #         file_name=os.path.basename(zip_path),
            #         mime="application/zip"
            #     )
        else:
            st.error("Tahmin sonuçları klasörü bulunamadı.")

        # Geçici klasörü silmek istersen:
        # shutil.rmtree(temp_dir)
    else:
        st.info("Lütfen birden fazla görsel yükleyin.")
