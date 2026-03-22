"""
NetGuard AI - System Tray Module
Windows taskbar mein icon dikhata hai
"""

import webbrowser
import threading


def start_tray(shared_data):
    try:
        import pystray
        from PIL import Image, ImageDraw
    except ImportError:
        print("[Tray] pystray ya pillow nahi mila.")
        print("       Install karo: pip install pystray pillow")
        # Tray ke bina bhi chalata raho
        try:
            import time
            while shared_data["running"]:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 NetGuard AI band ho raha hai...")
            shared_data["running"] = False
        return

    # Shield icon banao (programmatically)
    def create_icon():
        img = Image.new('RGBA', (64, 64), color=(0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Shield shape
        draw.polygon([
            (32, 4), (58, 16), (58, 36),
            (32, 60), (6, 36), (6, 16)
        ], fill=(0, 200, 100, 255))

        # "G" letter andar
        draw.rectangle([24, 24, 40, 40], fill=(0, 0, 0, 200))
        draw.text((26, 25), "NG", fill=(255, 255, 255, 255))

        return img

    # Menu actions
    def open_dashboard(icon, item):
        webbrowser.open("http://localhost:5000")

    def show_status(icon, item):
        conns = len(shared_data.get("connections", []))
        alerts = len(shared_data.get("alerts", []))
        print(f"[Status] Connections: {conns} | Alerts: {alerts}")

    def stop_netguard(icon, item):
        print("\n🛑 NetGuard AI band ho raha hai...")
        shared_data["running"] = False
        icon.stop()

    # Tray menu
    menu = pystray.Menu(
        pystray.MenuItem("📊 Dashboard Kholo", open_dashboard, default=True),
        pystray.MenuItem("📈 Status Dekho", show_status),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("❌ NetGuard Band Karo", stop_netguard),
    )

    icon = pystray.Icon(
        "NetGuard AI",
        create_icon(),
        "NetGuard AI - Chal raha hai 🛡️",
        menu
    )

    print("[Tray] System tray mein icon aa gaya! Right-click karo.")
    icon.run()
