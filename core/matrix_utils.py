"""
Mesafe matrisi ve feromon matrisi yardımcı fonksiyonları.

Bu modül, göletler arası mesafe matrislerini oluşturmak için kullanılır.
Google Distance Matrix API ile gerçek sürüş mesafeleri hesaplanır.
"""
import numpy as np
import requests


def build_distance_matrix_google(lakes, api_key, mode="driving"):
    """
    Google Distance Matrix API kullanarak tüm göletler arası sürüş mesafe matrisi oluşturur.
    
    Bu fonksiyon, Google Distance Matrix API'yi kullanarak gerçek sürüş mesafelerini
    hesaplar. Tek bir API çağrısı ile tüm gölet çiftleri için mesafeler alınır.
    
    Avantajları:
    - Gerçek sürüş mesafeleri (yol ağını dikkate alır)
    - Trafik, yol durumu gibi faktörler dikkate alınabilir
    - Çok doğru sonuçlar
    
    Dezavantajları:
    - API anahtarı gerekir (ücretli olabilir)
    - API çağrısı yapılması gerekir (internet bağlantısı)
    
    Args:
        lakes: Gölet bilgilerini içeren liste. Her eleman 'lat' ve 'lng' anahtarlarına sahip olmalı.
        api_key: Google Maps API anahtarı (Distance Matrix API erişimi olmalı)
        mode: Seyahat modu. Seçenekler: "driving" (sürüş), "walking" (yürüyüş),
              "bicycling" (bisiklet), "transit" (toplu taşıma). Varsayılan: "driving"
    
    Returns:
        NxN mesafe matrisi (kilometre cinsinden). dist[i][j] = i. ve j. gölet arası sürüş mesafesi.
        Ulaşılamayan yollar için np.inf değeri kullanılır.
    
    Raises:
        ValueError: API anahtarı boşsa
        RuntimeError: API çağrısı başarısız olursa
    """
    if not api_key:
        raise ValueError("Distance Matrix için Google Maps API anahtarı boş olamaz.")
    
    # Koordinatları API formatına çevir: "lat,lng" formatında
    coords = [f"{lake['lat']},{lake['lng']}" for lake in lakes]
    origins = "|".join(coords)  # Tüm başlangıç noktaları (pipe ile ayrılmış)
    destinations = origins  # Tüm hedef noktalar (aynı göletler)
    
    # Google Distance Matrix API endpoint
    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": origins,        # Başlangıç noktaları
        "destinations": destinations,  # Hedef noktalar
        "mode": mode,              # Seyahat modu
        "units": "metric",         # Metrik birimler (km, metre)
        "key": api_key,            # API anahtarı
    }
    
    # API çağrısı yap
    resp = requests.get(url, params=params)
    data = resp.json()
    
    # API yanıtını kontrol et
    if data.get("status") != "OK":
        raise RuntimeError(
            f"Distance Matrix API hatası: {data.get('status')} - {data.get('error_message')}"
        )
    
    n = len(lakes)
    dist = np.zeros((n, n), dtype=float)
    
    # API yanıtından mesafe matrisini oluştur
    for i, row in enumerate(data["rows"]):
        for j, elem in enumerate(row["elements"]):
            status = elem.get("status")
            if status == "OK":
                # Mesafe değeri metre cinsinden gelir, kilometreye çevir
                dist[i, j] = elem["distance"]["value"] / 1000.0
            else:
                # Ulaşılamayan yol varsa çok büyük bir ceza ver (algoritmanın bu yolu seçmemesi için)
                dist[i, j] = np.inf
    
    # Diagonal elemanları 0 yap (aynı gölet)
    np.fill_diagonal(dist, 0.0)
    return dist


def initialize_pheromone_matrix(n, initial_value=1.0):
    """
    Initialize pheromone matrix.
    """
    return np.ones((n, n), dtype=float) * initial_value

