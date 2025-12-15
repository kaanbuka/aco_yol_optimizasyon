"""
Veri modülleri.

Bu paket, veri ile ilgili fonksiyonları içerir:
- coordinates: Gölet koordinatlarını almak için Google Geocoding API entegrasyonu
"""

from .coordinates import geocode_place, fetch_lakes_from_google

__all__ = [
    'geocode_place',
    'fetch_lakes_from_google',
]

