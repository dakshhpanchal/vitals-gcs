from PySide6.QtWebEngineWidgets import QWebEngineView

class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self._ready = False
        self.loadFinished.connect(self._on_load)
        self.setHtml(self._html())

    def _on_load(self, ok):
        if ok:
            self._ready = True

    def update_position(self, lat, lon):
        if not self._ready:
            return   # <-- CRITICAL
        self.page().runJavaScript(
            f"updatePosition({lat}, {lon});"
        )

    def _html(self):
        return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8" />
<style>
html, body, #map { width:100%; height:100%; margin:0; }
</style>
<link rel="stylesheet"
 href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
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

function updatePosition(lat, lon){
    marker.setLatLng([lat, lon]);
    map.setView([lat, lon], map.getZoom());
}
</script>
</body>
</html>
"""
