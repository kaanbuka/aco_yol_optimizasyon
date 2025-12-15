# 🏞️ ACO Ankara Gölleri Optimizasyonu

## 📋 Proje Açıklaması

Bu proje, **Proje 2 – Senaryo 5** kapsamında, Ankara çevresindeki **10 gölet/barajdan su numunesi toplamak** için en kısa rotayı bulmak üzere **Karınca Kolonisi Algoritması (ACO)** kullanır.

### 🎯 Proje Amacı

Ankara'daki göletlerden su numunesi toplamak için en optimal rotayı belirlemek. Bu rota, tüm göletleri ziyaret edip başlangıç noktasına dönen en kısa yolu bulur.

### 🔧 Kullanılan Teknolojiler

- **Google Geocoding API**: Göletlerin koordinatlarını ve adreslerini otomatik olarak almak için
- **Google Distance Matrix API**: Gerçek sürüş mesafelerini hesaplamak için
- **Karınca Kolonisi Algoritması (ACO)**: En kısa rotayı bulmak için optimizasyon algoritması
- **Streamlit**: İnteraktif web arayüzü
- **PyDeck**: Harita görselleştirme
- **Matplotlib**: Yakınsama grafikleri

### 📍 İncelenen Göletler

1. Mogan Gölü
2. Eymir Gölü
3. Çubuk Karagöl
4. Kurtboğazı Barajı
5. Çamlıdere Barajı
6. Kesikköprü Barajı
7. Bayındır Barajı
8. Çubuk-1 Barajı
9. Akyar Barajı
10. Kavşakkaya Barajı

## Kurulum

```bash
pip install -r requirements.txt
```

## Kullanım

```bash
streamlit run main.py
```

## Gereksinimler

- Google Maps API anahtarı (Geocoding ve Distance Matrix API'leri için)
- Python 3.7+

## 🔑 API Anahtarı Ayarlama

API anahtarını üç şekilde ayarlayabilirsiniz (öncelik sırasına göre):

1. **Streamlit secrets.toml dosyası (Önerilen - En Güvenli):**
   `.streamlit/secrets.toml` dosyasını oluşturun ve şunu ekleyin:
   ```toml
   GOOGLE_MAPS_API_KEY = "your_api_key_here"
   ```
   ⚠️ **Önemli:** Bu dosya `.gitignore`'da olduğu için Git'e yüklenmeyecektir.

2. **Çevre değişkeni olarak:**
   ```bash
   export GOOGLE_MAPS_API_KEY="your_api_key_here"
   ```

3. **Streamlit arayüzünden:** Uygulama açıldığında sidebar'dan API anahtarını girebilirsiniz.

### 🔐 API Güvenliği

- API anahtarlarınızı **asla** kod içine yazmayın
- `.env` veya `.streamlit/secrets.toml` dosyalarını `.gitignore`'a eklediğinizden emin olun
- Bu projede `.gitignore` dosyası zaten doğru yapılandırılmıştır

## Proje Yapısı

- `main.py`: Streamlit ana uygulama dosyası
- `config.py`: ACO parametre ayarları ve gölet konfigürasyonu
- `data/coordinates.py`: Google Geocoding fonksiyonları ve gölet verileri
- `core/matrix_utils.py`: Google Distance Matrix API ile mesafe matrisi oluşturma
- `core/ant_algorithm.py`: ACO algoritması implementasyonu
- `visual/plotting.py`: PyDeck harita görselleştirme ve grafik çizimi

## ✨ Özellikler

### 🗺️ Veri Yönetimi
- ✅ Google Geocoding API ile otomatik koordinat alma
- ✅ Google Distance Matrix API ile gerçek sürüş mesafeleri
- ✅ 10 Ankara göleti/barajı için otomatik veri çekme

### 🐜 ACO Algoritması
- ✅ Tam implementasyon: Karınca döngüsü, feromon, α, β, buharlaşma oranı
- ✅ Dinamik parametre ayarlama (Streamlit arayüzünden)
- ✅ Her çalıştırmada mantıklı ve geçerli sonuçlar
- ✅ Detaylı Türkçe kod yorumları ve dokümantasyon

### 📊 Görselleştirme
- ✅ PyDeck ile interaktif harita görselleştirme
- ✅ İterasyonlara göre yakınsama grafikleri (en iyi ve ortalama)
- ✅ Rota detayları tablosu
- ✅ Gölet listesi ve koordinat bilgileri

### 🎛️ Kullanıcı Arayüzü
- ✅ Ayarlanabilir ACO parametreleri (karınca sayısı, iterasyon, α, β, ρ, Q)
- ✅ API anahtarı yönetimi (secrets.toml, çevre değişkeni veya manuel giriş)
- ✅ Sade, estetik ve işlevsel arayüz

## 📚 ACO Algoritması Hakkında

Karınca Kolonisi Optimizasyonu (ACO), doğadaki karıncaların yiyecek arama davranışından esinlenen bir meta-sezgisel optimizasyon algoritmasıdır.

### Algoritma Bileşenleri

- **α (Alpha)**: Feromon etkisi katsayısı - Karıncaların bıraktığı izlerin ne kadar önemli olduğu
- **β (Beta)**: Görünürlük etkisi katsayısı - Kısa mesafelerin ne kadar önemli olduğu
- **ρ (Rho)**: Buharlaşma oranı - Eski feromon izlerinin ne kadar hızlı kaybolacağı (0-1 arası)
- **Q**: Feromon miktarı sabiti - Karıncaların bıraktığı feromon miktarı
- **Karınca Sayısı**: Her iterasyonda kaç karınca tur oluşturacak
- **İterasyon Sayısı**: Algoritmanın kaç kez çalışacağı

### Algoritma Adımları

1. **Başlangıç**: Feromon matrisini başlat, görünürlük matrisini hesapla
2. **Her iterasyonda**:
   - Her karınca için bir tur oluştur (feromon ve görünürlüğe göre)
   - Her turun uzunluğunu hesapla
   - En iyi turu güncelle
   - Feromon buharlaşması uygula
   - Her karınca için feromon güncelle (kısa yollar daha fazla feromon alır)
3. **Sonuç**: En iyi rotayı döndür

