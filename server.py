"""
NetGuard AI - Flask Server
Dashboard ke liye API endpoints serve karta hai
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os


def start_server(shared_data):
    app = Flask(__name__)
    CORS(app)

    base_dir = os.path.dirname(os.path.abspath(__file__))

    @app.route('/')
    def index():
        return send_from_directory(base_dir, 'dashboard.html')

    @app.route('/api/connections')
    def connections():
        return jsonify(shared_data.get("connections", []))

    @app.route('/api/alerts')
    def alerts():
        return jsonify(shared_data.get("alerts", []))

    @app.route('/api/stats')
    def stats():
        conns = shared_data.get("connections", [])
        net_stats = shared_data.get("stats", {})
        threat_count = sum(1 for c in conns if c.get("threat_level") == "danger")
        warning_count = sum(1 for c in conns if c.get("threat_level") == "warning")

        return jsonify({
            "total_connections": len(conns),
            "unique_ips": len(set(c["remote_ip"] for c in conns)),
            "threat_count": threat_count,
            "warning_count": warning_count,
            "alert_count": len(shared_data.get("alerts", [])),
            "mb_sent": net_stats.get("mb_sent", 0),
            "mb_recv": net_stats.get("mb_recv", 0),
            "status": "running" if shared_data.get("running") else "stopped"
        })

    @app.route('/api/summary')
    def summary():
        return jsonify({
            "running": shared_data.get("running", False),
            "total_alerts": len(shared_data.get("alerts", [])),
        })

    print("[Server] Dashboard server shuru: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
