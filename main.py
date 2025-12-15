"""
Streamlit main application file.
Proje 2 – Senaryo 5: Ankara'daki göletlerden su numunesi toplama problemi
Karınca Kolonisi Algoritması (ACO) + Google Maps (Geocoding + Distance Matrix) + Streamlit
"""
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from data.coordinates import fetch_lakes_from_google
from core.matrix_utils import build_distance_matrix_google
from core.ant_algorithm import aco_tsp
from visual.plotting import show_route_map, plot_convergence


def main():
    st.set_page_config(
        page_title="Proje 2 – Senaryo 5 (Ankara Göletleri – ACO)",
        layout="wide"
    )
    
    st.title("Proje 2 – Senaryo 5: Ankara Göletlerinde Su Numunesi Toplama")
    
    # Kullanıcıya kısa açıklama
    st.markdown(
        """
        ### Proje Hakkında
        
        Bu uygulama, Ankara çevresindeki **10 gölet/barajdan su numunesi toplamak** için
        en kısa rotayı bulmak üzere **Karınca Kolonisi Algoritması (ACO)** kullanır.
        
        **Kullanılan Teknolojiler:**
        - **Google Geocoding API**: Göletlerin koordinatlarını ve adreslerini almak için
        - **Google Distance Matrix API**: Gerçek sürüş mesafelerini hesaplamak için
        - **ACO Algoritması**: En kısa rotayı bulmak için optimizasyon algoritması
        - **Streamlit**: İnteraktif web arayüzü
        """
    )
    
    # ============ Sidebar: Parametreler ============
    with st.sidebar:
        st.header("ACO Parametreleri")
        
        # ACO algoritması için ayarlanabilir hiperparametreler
        n_ants = st.slider("Karınca sayısı", 5, 80, 30, step=1)
        n_iter = st.slider("İterasyon sayısı", 10, 300, 100, step=10)
        alpha = st.slider("α (feromon etkisi)", 0.1, 5.0, 1.0, step=0.1)
        beta = st.slider("β (görüş etkisi)", 0.1, 5.0, 2.0, step=0.1)
        rho = st.slider("ρ (buharlaşma oranı)", 0.05, 0.95, 0.32, step=0.01)
        Q = st.slider("Q (feromon miktarı)", 10.0, 500.0, 100.0, step=10.0)
        
        st.markdown("---")
        st.header("Google Maps Ayarları")
        
        # API anahtarını önce secrets.toml'dan, sonra çevre değişkeninden, son olarak kullanıcıdan al
        # Streamlit secrets.toml'dan okuma (API güvenliği için önemli)
        try:
            default_key = st.secrets.get("GOOGLE_MAPS_API_KEY", "")
        except (FileNotFoundError, AttributeError, KeyError):
            default_key = ""
        
        # Çevre değişkeninden okuma (fallback)
        if not default_key:
            default_key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
        
        api_key = st.text_input(
            "Google Maps API anahtarı (Geocoding + Distance Matrix)",
            value=default_key,
            type="password",
            help="API anahtarınızı .streamlit/secrets.toml dosyasına ekleyebilirsiniz veya buraya yazabilirsiniz. Aynı anahtar hem Geocoding hem Distance Matrix için kullanılacaktır.",
        )
    
    # ============ Koordinat & adresleri API'den çek ============
    lakes = None
    if api_key:
        try:
            lakes = fetch_lakes_from_google(api_key)
            
            # API'den gelen gölet bilgilerini tablo olarak göster
            st.subheader("Gölet / Baraj Listesi (Senaryo 5 – Ankara)")
            df_lakes = pd.DataFrame(lakes)
            st.dataframe(df_lakes[["name", "address", "lat", "lng"]])
            
        except Exception as e:
            st.error(f"Google Geocoding ile koordinatlar alınırken hata oluştu: {e}")
    else:
        st.info(
            "Lütfen Google Maps API anahtarını girin; "
            "gölet koordinatları ve adresleri Geocoding API ile çekilecektir."
        )
    
    # ============ Hesapla butonu ============
    if st.button("En Kısa Rotayı Bul"):
        if lakes is None:
            st.error(
                "Önce geçerli bir API anahtarı girip "
                "koordinatların başarıyla alındığından emin olun."
            )
            st.stop()
        
        with st.spinner("Mesafeler hesaplanıyor ve ACO çalıştırılıyor..."):
            # Mesafe matrisi - Google Distance Matrix API ile gerçek sürüş mesafeleri
            try:
                dist_matrix = build_distance_matrix_google(lakes, api_key)
                st.success("Google Distance Matrix API ile sürüş mesafeleri hesaplandı.")
            except Exception as e:
                st.error(f"Mesafe matrisi hesaplanırken hata oluştu: {e}")
                st.stop()
            
            # ACO çalıştır
            best_route, best_length, hist_best, hist_mean = aco_tsp(
                dist_matrix,
                n_ants=n_ants,
                n_iterations=n_iter,
                alpha=alpha,
                beta=beta,
                rho=rho,
                Q=Q,
            )
        
        # Sonuçlar
        st.subheader("Sonuçlar")
        
        # En iyi rota uzunluğu
        col1, col2 = st.columns(2)
        with col1:
            st.metric("En İyi Rota Uzunluğu", f"{best_length:.2f} km")
        with col2:
            st.metric("Ziyaret Edilen Gölet Sayısı", len(best_route))
        
        # Rota sırası
        st.markdown("### Önerilen Rota Sırası")
        route_indices = best_route + [best_route[0]]
        route_names = [lakes[i]["name"] for i in route_indices]
        
        # Rota sırasını numaralı liste olarak göster
        route_text = ""
        for idx, name in enumerate(route_names, 1):
            if idx == len(route_names):
                route_text += f"**{idx}. {name}** (Başlangıç noktasına dönüş)"
            else:
                route_text += f"**{idx}. {name}** → "
        
        st.markdown(route_text)
        
        # Rota detayları tablosu
        st.markdown("### Rota Detayları")
        route_details = []
        for i in range(len(route_indices) - 1):
            from_idx = route_indices[i]
            to_idx = route_indices[i + 1]
            distance = dist_matrix[from_idx, to_idx]
            route_details.append({
                "Adım": i + 1,
                "Başlangıç": lakes[from_idx]["name"],
                "Hedef": lakes[to_idx]["name"],
                "Mesafe (km)": f"{distance:.2f}"
            })
        
        df_route = pd.DataFrame(route_details)
        st.dataframe(df_route, use_container_width=True, hide_index=True)
        
        # Fitness grafiği (iterasyonlara göre)
        st.subheader("İterasyonlara Göre Tur Uzunluğu (Fitness)")
        fig = plot_convergence(hist_best, hist_mean)
        st.pyplot(fig)
        
        # Harita
        st.subheader("Ankara Göletleri Üzerinde En İyi Rota")
        show_route_map(lakes, best_route)


if __name__ == "__main__":
    main()

