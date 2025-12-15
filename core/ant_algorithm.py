"""
Ant Colony Optimization (ACO) algorithm implementation for TSP.

Karınca Kolonisi Optimizasyonu (ACO) algoritması, TSP (Traveling Salesman Problem) 
problemlerini çözmek için kullanılan bir meta-sezgisel optimizasyon algoritmasıdır.

Algoritma şu bileşenlerden oluşur:
- Karınca döngüsü: Her karınca bir tur oluşturur
- Feromon (pheromone): Karıncaların bıraktığı izler
- α (alpha): Feromon etkisi katsayısı
- β (beta): Görünürlük (heuristic) etkisi katsayısı
- ρ (rho): Feromon buharlaşma oranı
- Q: Feromon miktarı sabiti
"""
import numpy as np


def tour_length(route, dist_matrix):
    """
    Verilen rota için toplam tur uzunluğunu (km) hesaplar.
    
    Bu fonksiyon, bir karıncanın oluşturduğu rotanın toplam mesafesini hesaplar.
    Rota döngüseldir (son göletten tekrar başlangıca döner).
    
    Args:
        route: Gölet indekslerinden oluşan rota listesi (örn: [0, 3, 1, 2])
        dist_matrix: NxN mesafe matrisi (km cinsinden)
    
    Returns:
        Toplam tur uzunluğu (km)
    """
    total = 0.0
    n = len(route)
    
    # Rotadaki her göletten bir sonrakine olan mesafeyi topla
    for i in range(n):
        a = route[i]  # Mevcut gölet
        b = route[(i + 1) % n]  # Sonraki gölet (son göletten tekrar başlangıca dönüş)
        d = dist_matrix[a, b]
        
        # Ulaşılamayan yol varsa çok büyük bir ceza ver (algoritmanın bu yolu seçmemesi için)
        if np.isinf(d):
            total += 1e6
        else:
            total += d
    
    return total


def construct_tour(start, pheromone, visibility, alpha, beta):
    """
    Bir karıncanın bir tur (permutasyon) oluşturması.
    
    Bu fonksiyon, ACO algoritmasının temel adımıdır. Her karınca, feromon izlerini
    ve görünürlük (heuristic) bilgisini kullanarak bir rota oluşturur.
    
    Seçim olasılığı formülü:
    P(i,j) = [τ(i,j)^α * η(i,j)^β] / Σ[τ(i,k)^α * η(i,k)^β]
    
    Burada:
    - τ(i,j): i'den j'ye olan feromon miktarı
    - η(i,j): i'den j'ye olan görünürlük (1/mesafe)
    - α: Feromon etkisi katsayısı (ne kadar önemli olduğu)
    - β: Görünürlük etkisi katsayısı (ne kadar önemli olduğu)
    
    Args:
        start: Başlangıç gölet indeksi
        pheromone: NxN feromon matrisi (karıncaların bıraktığı izler)
        visibility: NxN görünürlük matrisi (1 / mesafe matrisi)
        alpha: Feromon etkisi katsayısı (α)
        beta: Görünürlük etkisi katsayısı (β)
    
    Returns:
        Gölet indekslerinden oluşan tur listesi
    """
    n = pheromone.shape[0]
    tour = [start]  # Turu başlangıç göleti ile başlat
    unvisited = set(range(n))  # Henüz ziyaret edilmemiş göletler
    unvisited.remove(start)  # Başlangıç göletini ziyaret edilmiş olarak işaretle
    current = start  # Mevcut konum
    
    # Tüm göletler ziyaret edilene kadar devam et
    while unvisited:
        candidates = list(unvisited)  # Ziyaret edilebilecek göletler
        numerators = []  # Olasılık payları
        
        # Her aday gölet için olasılık payını hesapla
        for j in candidates:
            # Feromon etkisi: τ(i,j)^α
            tau = pheromone[current, j] ** alpha
            # Görünürlük etkisi: η(i,j)^β = (1/mesafe)^β
            eta = visibility[current, j] ** beta
            # Toplam etki: τ(i,j)^α * η(i,j)^β
            numerators.append(tau * eta)
        
        numerators = np.array(numerators)
        
        # Eğer tüm paylar 0 ise (feromon yok, görünürlük yok), uniform seçim yap
        if numerators.sum() == 0:
            probs = np.ones_like(numerators) / len(numerators)
        else:
            # Olasılıkları normalize et (toplam 1 olmalı)
            probs = numerators / numerators.sum()
        
        # Olasılıklara göre bir sonraki göleti seç
        chosen = int(np.random.choice(candidates, p=probs))
        tour.append(chosen)  # Seçilen göleti tura ekle
        unvisited.remove(chosen)  # Seçilen göleti ziyaret edilmiş olarak işaretle
        current = chosen  # Mevcut konumu güncelle
    
    return tour


def aco_tsp(
    dist_matrix,
    n_ants=30,
    n_iterations=100,
    alpha=1.0,
    beta=2.0,
    rho=0.32,  # projedeki r = 0.32'ye uygun (buharlaşma oranı)
    Q=100.0,
):
    """
    TSP (Traveling Salesman Problem) için Karınca Kolonisi Optimizasyonu (ACO) algoritması.
    
    Algoritma Adımları:
    1. Başlangıç: Feromon matrisini başlat, görünürlük matrisini hesapla
    2. Her iterasyonda:
       a. Her karınca için bir tur oluştur (construct_tour)
       b. Her turun uzunluğunu hesapla (tour_length)
       c. En iyi turu güncelle
       d. Feromon buharlaşması uygula (pheromone *= (1 - rho))
       e. Her karınca için feromon güncelle (pheromone += Q / tour_length)
    3. En iyi rotayı döndür
    
    Feromon Güncelleme Formülü:
    τ(i,j) = (1 - ρ) * τ(i,j) + Σ(Q / L_k)
    
    Burada:
    - ρ (rho): Buharlaşma oranı (0-1 arası)
    - Q: Feromon miktarı sabiti
    - L_k: k. karıncanın tur uzunluğu
    
    Args:
        dist_matrix: km cinsinden NxN mesafe matrisi
        n_ants: Karınca sayısı (her iterasyonda kaç karınca tur oluşturacak)
        n_iterations: İterasyon sayısı (algoritmanın kaç kez çalışacağı)
        alpha: Feromon etkisi katsayısı (α) - ne kadar yüksekse feromon o kadar önemli
        beta: Görünürlük etkisi katsayısı (β) - ne kadar yüksekse kısa mesafe o kadar önemli
        rho: Buharlaşma oranı (ρ) - feromonun ne kadar hızlı kaybolacağı (0-1 arası)
        Q: Feromon miktarı sabiti - karıncaların bıraktığı feromon miktarı
    
    Returns:
        best_route: En iyi rota (gölet indekslerinden oluşan liste)
        best_length: En iyi rota uzunluğu (km)
        hist_best: İterasyonlara göre en iyi uzunluk geçmişi (yakınsama analizi için)
        hist_mean: İterasyonlara göre ortalama uzunluk geçmişi (yakınsama analizi için)
    """
    n = dist_matrix.shape[0]  # Gölet sayısı
    epsilon = 1e-10  # Sıfıra bölme hatasını önlemek için küçük bir sayı
    
    # Başlangıç feromon matrisi: Tüm kenarlarda eşit feromon miktarı (1.0)
    pheromone = np.ones((n, n), dtype=float)
    
    # Görünürlük matrisi: 1 / mesafe (kısa mesafe = yüksek görünürlük)
    visibility = 1.0 / (dist_matrix + epsilon)
    visibility[dist_matrix == 0] = 0.0  # Diagonal elemanlar (aynı gölet) ve hatalı yerler için 0
    
    # En iyi çözümü takip et
    best_route = None
    best_length = np.inf  # Sonsuz başlat (herhangi bir çözüm daha iyi olacak)
    
    # İterasyon ilerleyişini kaydetmek için tarihçe (yakınsama grafiği için)
    hist_best = []  # Her iterasyondaki en iyi uzunluk
    hist_mean = []  # Her iterasyondaki ortalama uzunluk
    
    # Ana döngü: Her iterasyonda
    for it in range(n_iterations):
        all_routes = []  # Bu iterasyondaki tüm rotalar
        all_lengths = []  # Bu iterasyondaki tüm rota uzunlukları
        
        # Her karınca için bir tur oluştur
        for k in range(n_ants):
            # Rastgele bir başlangıç göleti seç
            start = np.random.randint(0, n)
            # Karınca bir tur oluşturur (feromon ve görünürlüğe göre)
            route = construct_tour(start, pheromone, visibility, alpha, beta)
            # Turun toplam uzunluğunu hesapla
            length = tour_length(route, dist_matrix)
            all_routes.append(route)
            all_lengths.append(length)
            
            # Eğer bu tur şu ana kadarki en iyi turdan daha kısaysa, güncelle
            if length < best_length:
                best_length = length
                best_route = route.copy()  # Kopyasını al (referans değil)
        
        # Bu iterasyonun istatistiklerini kaydet
        all_lengths = np.array(all_lengths, dtype=float)
        hist_best.append(all_lengths.min())  # En iyi uzunluk
        hist_mean.append(all_lengths.mean())  # Ortalama uzunluk
        
        # Feromon buharlaşması: Eski feromonların bir kısmı kaybolur
        # Bu, algoritmanın yeni çözümler keşfetmesine yardımcı olur
        pheromone *= (1.0 - rho)
        
        # Feromon güncellemesi: Her karınca, izlediği yolda feromon bırakır
        # Kısa yollar daha fazla feromon alır (Q / L formülü)
        for route, L in zip(all_routes, all_lengths):
            # Geçersiz rotaları atla (uzunluk 0 veya sonsuz)
            if L == 0 or np.isinf(L):
                continue
            
            # Bu karıncanın bıraktığı feromon miktarı (kısa yol = daha fazla feromon)
            contribution = Q / L
            
            # Rotadaki her kenar için feromon güncelle
            for i in range(n):
                a = route[i]  # Mevcut gölet
                b = route[(i + 1) % n]  # Sonraki gölet
                # Simetrik güncelleme (a->b ve b->a aynı mesafe)
                pheromone[a, b] += contribution
                pheromone[b, a] += contribution
    
    return best_route, best_length, hist_best, hist_mean

