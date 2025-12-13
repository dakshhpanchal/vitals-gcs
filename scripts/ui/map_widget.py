from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
import os

class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setHtml(self._html())

    def update_position(self, lat, lon):
        js = f"updateMarker({lat}, {lon});"
        self.page().runJavaScript(js)

    def _html(self):
        return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<title>Map</title>
<style>
html, body, #map {
    width: 100%;
    height: 100%;
    margin: 0;
}
</style>
<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>
<body>
<div id="map"></div>
<script>
var map = L.map('map').setView([0,0], 16);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

var marker = L.marker([0,0]).addTo(map);

function updateMarker(lat, lon){
    marker.setLatLng([lat, lon]);
    map.setView([lat, lon], map.getZoom());
}
</script>
</body>
</html>
"""
