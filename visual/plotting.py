"""
Rota ve yakınsama grafikleri.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st


def show_route_map(lakes, route):
    """
    PyDeck ile göletler ve en iyi rotayı harita üzerinde gösterir.
    
    Args:
        lakes: 'name', 'lat', 'lng' anahtarlarına sahip sözlük listesi
        route: Rotayı temsil eden indeks listesi
    """
    route_order = {node: idx + 1 for idx, node in enumerate(route)}
    
    df_points = pd.DataFrame({
        "name": [lake["name"] for lake in lakes],
        "lat": [lake["lat"] for lake in lakes],
        "lon": [lake["lng"] for lake in lakes],
        "order": [route_order.get(i) for i in range(len(lakes))],
    })
    
    df_points["order_label"] = df_points["order"].apply(
        lambda x: f"{x}. durak" if x else "Bilinmiyor"
    )
    
    # Rota path (lon, lat sırasına dikkat!)
    route_indices = route + [route[0]]
    path_coords = [
        [lakes[i]["lng"], lakes[i]["lat"]] for i in route_indices
    ]
    
    path_data = [{"path": path_coords, "name": "En iyi rota"}]
    
    route_layer = pdk.Layer(
        "PathLayer",
        data=path_data,
        get_path="path",
        get_color=[255, 0, 0],
        width_scale=10,
        width_min_pixels=3,
    )
    
    points_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_points,
        get_position=["lon", "lat"],
        get_radius=2000,
        get_fill_color=[0, 0, 255],
        pickable=True,
    )
    
    view_state = pdk.ViewState(
        latitude=df_points["lat"].mean(),
        longitude=df_points["lon"].mean(),
        zoom=8,
    )
    
    st.pydeck_chart(
        pdk.Deck(
            layers=[route_layer, points_layer],
            initial_view_state=view_state,
            tooltip={"html": "<b>{name}</b><br>Sıra: {order_label}"},
        )
    )


def plot_convergence(hist_best, hist_mean, title="İterasyonlara Göre Tur Uzunluğu (Fitness)"):
    """
    İterasyonlara göre en iyi ve ortalama tur uzunluklarını gösteren yakınsama grafiği çizer.
    
    Args:
        hist_best: İterasyon başına en iyi tur uzunluklarının listesi
        hist_mean: İterasyon başına ortalama tur uzunluklarının listesi
        title: Grafik başlığı
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    iterations = range(len(hist_best))
    ax.plot(iterations, hist_best, label="En iyi tur uzunluğu", linewidth=2)
    ax.plot(iterations, hist_mean, label="Ortalama tur uzunluğu", linewidth=2)
    ax.set_xlabel("İterasyon")
    ax.set_ylabel("Toplam mesafe (km)")
    ax.set_title(title)
    ax.grid(True)
    ax.legend()
    
    return fig


def plot_route(coordinates, path, title="Optimal Route"):
    """
    Basit bir matplotlib haritası üzerinde rotayı çizer (PyDeck alternatifi).
    
    Args:
        coordinates: (lat, lon) tuple'larından oluşan liste
        path: Rotayı temsil eden indeks listesi
        title: Grafik başlığı
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Rota için koordinatları çıkar
    path_coords = [coordinates[i] for i in path]
    path_coords.append(path_coords[0])  # Döngüyü kapat
    
    lats = [coord[0] for coord in path_coords]
    lons = [coord[1] for coord in path_coords]
    
    # Rotayı çiz
    ax.plot(lons, lats, 'b-', linewidth=2, marker='o', markersize=8)
    ax.scatter(lons, lats, c='red', s=100, zorder=5)
    
    # Şehirleri etiketle
    for i, (lat, lon) in enumerate(path_coords[:-1]):
        ax.annotate(f'City {path[i]}', (lon, lat), 
                   xytext=(5, 5), textcoords='offset points')
    
    ax.set_xlabel('Boylam')
    ax.set_ylabel('Enlem')
    ax.set_title(title)
    ax.grid(True)
    
    return fig

