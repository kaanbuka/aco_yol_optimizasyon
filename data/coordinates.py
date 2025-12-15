"""
City data and Google Geocoding functions.
"""
import requests
import streamlit as st
from config import LAKE_CONFIG


def geocode_place(query: str, api_key: str, language: str = "tr"):
    """
    Verilen adres/sorgu için Google Geocoding API'den koordinat ve formatlanmış adres alır.
    
    Args:
        query: Arama sorgusu (örn: "Mogan Gölü, Gölbaşı, Ankara, Türkiye")
        api_key: Google Maps API anahtarı
        language: Dil kodu (varsayılan: "tr")
    
    Returns:
        {
            "formatted_address": "...",
            "lat": ...,
            "lng": ...
        }
    """
    if not api_key:
        raise ValueError("Geocoding için Google Maps API anahtarı gerekli.")
    
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": query,
        "key": api_key,
        "language": language,
    }
    
    resp = requests.get(url, params=params)
    data = resp.json()
    status = data.get("status")
    
    if status != "OK" or not data.get("results"):
        raise RuntimeError(
            f"Geocode API hatası ({query}): {status} - {data.get('error_message')}"
        )
    
    result = data["results"][0]
    loc = result["geometry"]["location"]
    formatted_address = result.get("formatted_address", query)
    
    return {
        "formatted_address": formatted_address,
        "lat": loc["lat"],
        "lng": loc["lng"],
    }


@st.cache_data(show_spinner=False)
def fetch_lakes_from_google(api_key: str):
    """
    LAKE_CONFIG içindeki tüm göletler için Geocoding API çağrısı yapar,
    name, query, address, lat, lng alanları ile liste döner.
    
    Sonuçlar Streamlit cache'inde saklanır.
    
    Args:
        api_key: Google Maps API anahtarı
    
    Returns:
        List of dictionaries with lake information
    """
    lakes = []
    for item in LAKE_CONFIG:
        info = geocode_place(item["query"], api_key)
        lakes.append({
            "name": item["name"],
            "query": item["query"],
            "address": info["formatted_address"],
            "lat": info["lat"],
            "lng": info["lng"],
        })
    return lakes

