"""
NetGuard AI - Network Monitor Module
Saari active connections track karta hai
"""

import psutil
import socket
import datetime


class NetworkMonitor:
    def __init__(self):
        self.seen_ips = set()
        self.new_ips_log = []

    def get_hostname(self, ip):
        try:
            return socket.gethostbyaddr(ip)[0]
        except:
            return "Unknown"

    def get_connections(self):
        connections = []
        try:
            for conn in psutil.net_connections(kind='inet'):
                if conn.raddr and conn.raddr.ip:
                    remote_ip = conn.raddr.ip
                    remote_port = conn.raddr.port
                    local_port = conn.laddr.port if conn.laddr else 0
                    status = conn.status

                    # Private/loopback IPs skip karo
                    if remote_ip.startswith("127.") or remote_ip.startswith("::1"):
                        continue

                    # Process name
                    process_name = "Unknown"
                    pid = conn.pid
                    try:
                        if pid:
                            proc = psutil.Process(pid)
                            process_name = proc.name()
                    except:
                        pass

                    connections.append({
                        "remote_ip": remote_ip,
                        "remote_port": remote_port,
                        "local_port": local_port,
                        "status": status,
                        "process": process_name,
                        "pid": pid,
                        "is_new": remote_ip not in self.seen_ips,
                        "time": datetime.datetime.now().strftime("%H:%M:%S"),
                        "threat_score": 0.0,
                        "threat_level": "safe"
                    })
        except Exception as e:
            print(f"[Monitor] Error: {e}")

        # Duplicates remove
        seen = set()
        unique = []
        for c in connections:
            key = f"{c['remote_ip']}:{c['remote_port']}:{c['process']}"
            if key not in seen:
                seen.add(key)
                unique.append(c)

        return unique

    def check_new_ips(self, connections):
        new_found = []
        for conn in connections:
            ip = conn["remote_ip"]
            if ip not in self.seen_ips:
                self.seen_ips.add(ip)
                info = {
                    "ip": ip,
                    "process": conn["process"],
                    "time": conn["time"]
                }
                self.new_ips_log.append(info)
                new_found.append(info)
        return new_found

    def get_stats(self):
        try:
            stats = psutil.net_io_counters()
            return {
                "mb_sent": round(stats.bytes_sent / (1024 * 1024), 2),
                "mb_recv": round(stats.bytes_recv / (1024 * 1024), 2),
                "packets_sent": stats.packets_sent,
                "packets_recv": stats.packets_recv,
            }
        except:
            return {"mb_sent": 0, "mb_recv": 0, "packets_sent": 0, "packets_recv": 0}

    def get_new_ips_log(self):
        return self.new_ips_log[-30:]
