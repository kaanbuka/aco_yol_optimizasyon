"""
Haversine mesafe hesaplama modülü.

Haversine formülü, küresel bir yüzey üzerinde (Dünya) iki nokta arasındaki
en kısa mesafeyi (kuş uçuşu) hesaplamak için kullanılır.
"""
import math


def haversine_km(lat1, lon1, lat2, lon2):
    """
    İki nokta arasındaki kuş uçuşu mesafeyi (km) hesaplar.
    
    Haversine formülü, Dünya'nın küresel şeklini dikkate alarak iki koordinat
    arasındaki en kısa mesafeyi hesaplar. Bu mesafe, yeryüzü üzerindeki
    gerçek mesafedir (kuş uçuşu), sürüş mesafesi değildir.
    
    Args:
        lat1: İlk noktanın enlemi (latitude) - derece cinsinden
        lon1: İlk noktanın boylamı (longitude) - derece cinsinden
        lat2: İkinci noktanın enlemi (latitude) - derece cinsinden
        lon2: İkinci noktanın boylamı (longitude) - derece cinsinden
    
    Returns:
        İki nokta arasındaki mesafe (kilometre cinsinden)
    
    Örnek:
        >>> haversine_km(39.9334, 32.8597, 39.7833, 32.7833)
        18.5  # Ankara'dan Mogan Gölü'ne yaklaşık mesafe
    """
    R = 6371.0  # Dünya yarıçapı (kilometre cinsinden)
    
    # Derece cinsinden koordinatları radyan cinsine çevir
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)  # Enlem farkı (radyan)
    dlambda = math.radians(lon2 - lon1)  # Boylam farkı (radyan)
    
    # Haversine formülü: a = sin²(Δφ/2) + cos(φ1) * cos(φ2) * sin²(Δλ/2)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    
    # Merkez açıyı hesapla: c = 2 * atan2(√a, √(1−a))
    # Burada asin kullanıyoruz (atan2 yerine)
    c = 2 * math.asin(math.sqrt(a))
    
    # Mesafeyi hesapla: d = R * c
    return R * c

# Alias for backward compatibility
haversine_distance = haversine_km

