"""
ACO parameter settings.
"""

# Ankara Göletleri Konfigürasyonu
# Koordinatlar ELLE yazılmıyor.
# Her gölet/baraj için Google Geocoding API'ye gönderilecek sorgu metni tanımlıyoruz.
LAKE_CONFIG = [
    {"name": "Mogan Gölü",        "query": "Mogan Gölü, Gölbaşı, Ankara, Türkiye"},
    {"name": "Eymir Gölü",        "query": "Eymir Gölü, Oran, Ankara, Türkiye"},
    {"name": "Çubuk Karagöl",     "query": "Karagöl, Çubuk, Ankara, Türkiye"},
    {"name": "Kurtboğazı Barajı", "query": "Kurtboğazı Barajı, Ankara, Türkiye"},
    {"name": "Çamlıdere Barajı",  "query": "Çamlıdere Barajı, Ankara, Türkiye"},
    {"name": "Kesikköprü Barajı", "query": "Kesikköprü Barajı, Ankara, Türkiye"},
    {"name": "Bayındır Barajı",   "query": "Bayındır Barajı, Ankara, Türkiye"},
    {"name": "Çubuk-1 Barajı",    "query": "Çubuk 1 Barajı, Ankara, Türkiye"},
    {"name": "Akyar Barajı",      "query": "Akyar Barajı, Ankara, Türkiye"},
    {"name": "Kavşakkaya Barajı", "query": "Kavşakkaya Barajı, Ankara, Türkiye"},
]

N_LAKES = len(LAKE_CONFIG)

# ACO Parameters (Default values)
ALPHA = 1.0  # Pheromone importance
BETA = 2.0   # Heuristic importance
RHO = 0.32   # Evaporation rate (buharlaşma oranı)
Q = 100.0    # Pheromone deposit constant
NUM_ANTS = 30
NUM_ITERATIONS = 100

