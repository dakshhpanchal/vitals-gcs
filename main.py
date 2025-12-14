import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QTimer
import signal
from scripts.ui.dashboard import Dashboard
from scripts.controller.gamepad import ControllerReader
from scripts.mavlink.mav_client import MAVClient

def main():
    app = QApplication(sys.argv)
    def handle_sigint(*args):
        QApplication.quit()
    signal.signal(signal.SIGINT, handle_sigint)
    
    sig_timer = QTimer()
    sig_timer.start(100)
    sig_timer.timeout.connect(lambda: None)
    ui = Dashboard()
    ui.resize(1600, 900)
    ui.show()

    mav = MAVClient()
    mav.request_stream()

    controller = ControllerReader()
    app.aboutToQuit.connect(controller.stop)
    controller.updated.connect(
        lambda lx, ly, rx, ry: (
            ui.left_joy.update_stick(lx, ly),
            ui.right_joy.update_stick(rx, ry)
        )
    )

    gps = {"lat": None, "lon": None, "sats": None}
    vfr = {"alt": None, "speed": None}

    def poll_mav():
        while True:
            msg = mav.read()
            if not msg:
                break

            mtype = msg.get_type()

            if mtype == "GPS_RAW_INT":
                gps["lat"] = msg.lat / 1e7
                gps["lon"] = msg.lon / 1e7
                gps["sats"] = msg.satellites_visible

            elif mtype == "VFR_HUD":
                vfr["alt"] = msg.alt
                vfr["speed"] = msg.groundspeed

            elif mtype == "STATUSTEXT":
                text = msg.text
                if isinstance(text, bytes):
                    text = text.decode(errors='ignore').rstrip('\x00')
                else:
                    text = str(text).rstrip('\x00')

                ui.add_log(text)

        text = ""
        if gps["lat"] is not None:
            text += (
                "GPS:\n"
                f"  Lat: {gps['lat']:.6f}\n"
                f"  Lon: {gps['lon']:.6f}\n"
                f"  Satellites: {gps['sats']}\n\n"
            )
            ui.map.update_position(gps["lat"], gps["lon"])
        
        if vfr["alt"] is not None:
            text += f"Altitude: {vfr['alt']:.2f} cm\n"
            text += f"Speed: {vfr['speed']:.2f} m/s\n"

        if text:
            ui.update_telem(text)
        
    mav_timer = QTimer()
    mav_timer.timeout.connect(poll_mav)
    mav_timer.start(50)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()