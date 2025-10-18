import folium
import webbrowser

mapa = folium.Map(location=[10.99, -74.79], zoom_start=12)
folium.Marker(
    location=[10.99, -74.79],
    popup="Barranquilla",
    tooltip="Haz clic para más info"
).add_to(mapa)

mapa.save("Mapa.html")
webbrowser.open("barranquilla.html")