"""
NetGuard AI - Main Entry Point
Chalane ke liye: python netguard.py
"""

import threading
import time
import webbrowser
import sys
import os

# Windows check
if sys.platform != 'win32':
    print("Warning: Yeh tool Windows ke liye optimized hai.")

from monitor import NetworkMonitor
from alerts import AlertSystem
from ai_engine import AIEngine
from server import start_server

def main():
    print("=" * 55)
    print("   🛡️  NetGuard AI - Starting...")
    print("=" * 55)

    # Components initialize karo
    monitor = NetworkMonitor()
    alert_system = AlertSystem()
    ai_engine = AIEngine()

    # Shared state
    shared_data = {
        "connections": [],
        "alerts": [],
        "stats": {},
        "running": True
    }

    # --- Thread 1: Network Monitor ---
    def monitor_loop():
        print("[Monitor] Network monitoring shuru hua...")
        while shared_data["running"]:
            connections = monitor.get_connections()
            new_ips = monitor.check_new_ips(connections)
            shared_data["connections"] = connections
            shared_data["stats"] = monitor.get_stats()

            # AI se check karao
            for conn in connections:
                score = ai_engine.score(conn)
                conn["threat_score"] = score
                conn["threat_level"] = ai_engine.level(score)

            # Naaye IPs pe alert
            for ip_info in new_ips:
                alert = {
                    "type": "new_ip",
                    "ip": ip_info["ip"],
                    "process": ip_info["process"],
                    "time": ip_info["time"],
                    "message": f"Naaya IP detected: {ip_info['ip']} ({ip_info['process']})"
                }
                shared_data["alerts"].insert(0, alert)
                shared_data["alerts"] = shared_data["alerts"][:50]  # Last 50 raho
                alert_system.notify(alert["message"], alert["type"])

            # High threat connections pe alert
            for conn in connections:
                if conn.get("threat_score", 0) > 0.75:
                    alert = {
                        "type": "threat",
                        "ip": conn["remote_ip"],
                        "process": conn["process"],
                        "time": conn.get("time", ""),
                        "message": f"⚠️ Suspicious activity: {conn['remote_ip']} (Score: {conn['threat_score']:.2f})"
                    }
                    if not any(a["ip"] == conn["remote_ip"] and a["type"] == "threat"
                               for a in shared_data["alerts"][:5]):
                        shared_data["alerts"].insert(0, alert)
                        shared_data["alerts"] = shared_data["alerts"][:50]
                        alert_system.notify(alert["message"], "threat")

            time.sleep(8)

    # --- Thread 2: AI Training ---
    def ai_loop():
        print("[AI] Anomaly detection engine ready...")
        while shared_data["running"]:
            if shared_data["connections"]:
                ai_engine.train(shared_data["connections"])
            time.sleep(30)

    # --- Thread 3: Flask Server ---
    def server_loop():
        start_server(shared_data)

    # Sab threads shuru karo
    t1 = threading.Thread(target=monitor_loop, daemon=True)
    t2 = threading.Thread(target=ai_loop, daemon=True)
    t3 = threading.Thread(target=server_loop, daemon=True)

    t1.start()
    t2.start()
    t3.start()

    # Dashboard open karo
    time.sleep(2)
    print("[Dashboard] Browser mein khul raha hai...")
    webbrowser.open("http://localhost:5000")

    print("\n✅ NetGuard AI chal raha hai!")
    print("   Dashboard: http://localhost:5000")
    print("   Band karne ke liye: Ctrl+C dabao\n")

    # System tray try karo (agar available ho)
    try:
        from tray import start_tray
        start_tray(shared_data)
    except ImportError:
        print("[Tray] pystray install nahi hai, tray icon nahi chalega.")
        print("       Install karo: pip install pystray pillow")
        try:
            while shared_data["running"]:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 NetGuard AI band ho raha hai...")
            shared_data["running"] = False

if __name__ == "__main__":
    main()
