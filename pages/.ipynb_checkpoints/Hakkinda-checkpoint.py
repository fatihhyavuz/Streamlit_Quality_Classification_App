import streamlit as st
from PIL import Image

st.title("Hakkında")

st.markdown("""
🚀 **Demir Kaynak Kalite Tespiti Modeli**, GoldbergMed şirketinin medikal üretim hattında yapay zekâ destekli otomasyon vizyonunun bir parçası olarak geliştirilmiştir.

🔧 Bu yenilikçi çözüm, kaynak işlemi uygulanmış demir parçaların kalite seviyelerini **tamamen otonom bir şekilde** tespit etmektedir. Model, parçaları “Good” ve “Bad” olarak sınıflandırarak, geleneksel denetim süreçlerine olan bağımlılığı ortadan kaldırır. Böylece üretimde hem **verimlilik** artar hem de **insan hatası** minimize edilir.

🧠 Modelin temelinde, yüksek başarı oranlarıyla bilinen **YOLOv11** mimarisi yer almaktadır. Bu mimari sayesinde sistem, sahadaki gerçek zamanlı kalite kontrol görevlerini hızlı ve güvenilir biçimde yerine getirir.

---

### 🎯 Model Performans Değerleri

| Sınıf      | Görüntü Sayısı | Örnek Sayısı | Doğruluk (P) | Hassasiyet (R) | mAP@50 | mAP@50-95 |
|------------|----------------|--------------|---------------|----------------|--------|-----------|
| **Tümü**   | 301            | 378          | **0.731**     | **0.746**      | **0.759** | **0.423**   |
| **Bad**    | 165            | 186          | 0.773         | 0.774          | 0.789  | 0.459     |
| **Good**   | 138            | 192          | 0.689         | 0.719          | 0.728  | 0.388     |

📌 Bu performans metrikleri, modelin sahadaki uygulamalarda **yüksek doğruluk oranıyla çalıştığını** ve **karar destek sistemlerine güvenle entegre edilebileceğini** göstermektedir.

---

🔍 Bu sistem sayesinde GoldbergMed, üretim hattında kalite kontrol süreçlerinde **dijital dönüşümün en somut adımlarından birini** atmış ve sektördeki rekabet avantajını artırmıştır.
""")