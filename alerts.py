"""
NetGuard AI - Alert System
Desktop notifications aur sound alerts
"""

import threading
import time


class AlertSystem:
    def __init__(self):
        self.last_alert_time = {}
        self.cooldown = 30  # Same IP pe 30 sec baad hi dobara alert

        # Check available notification libraries
        self.notifier = self._init_notifier()
        self.sound_available = self._init_sound()

    def _init_notifier(self):
        # plyer try karo
        try:
            from plyer import notification
            print("[Alert] plyer notification ready.")
            return "plyer"
        except ImportError:
            pass

        # win10toast try karo
        try:
            from win10toast import ToastNotifier
            print("[Alert] win10toast notification ready.")
            return "win10toast"
        except ImportError:
            pass

        # Windows native (ctypes)
        try:
            import ctypes
            print("[Alert] Windows native notification ready.")
            return "native"
        except:
            pass

        print("[Alert] Koi notification library nahi mili. pip install plyer")
        return None

    def _init_sound(self):
        try:
            import winsound
            print("[Alert] Windows sound ready.")
            return "winsound"
        except ImportError:
            pass

        try:
            import pygame
            pygame.mixer.init()
            print("[Alert] pygame sound ready.")
            return "pygame"
        except ImportError:
            pass

        print("[Alert] Sound library nahi mili.")
        return None

    def notify(self, message, alert_type="info"):
        """Alert bhejo — cooldown check ke saath"""
        now = time.time()
        key = message[:30]  # Key for cooldown

        if key in self.last_alert_time:
            if now - self.last_alert_time[key] < self.cooldown:
                return  # Cooldown mein hai, skip karo

        self.last_alert_time[key] = now

        # Thread mein chalao taaki main loop block na ho
        t = threading.Thread(
            target=self._send_alert,
            args=(message, alert_type),
            daemon=True
        )
        t.start()

    def _send_alert(self, message, alert_type):
        title = "🛡️ NetGuard AI"
        if alert_type == "threat":
            title = "⚠️ NetGuard - THREAT DETECTED"
        elif alert_type == "new_ip":
            title = "🔍 NetGuard - New IP"

        # Notification bhejo
        self._send_notification(title, message)

        # Sound bajao
        self._play_sound(alert_type)

    def _send_notification(self, title, message):
        try:
            if self.notifier == "plyer":
                from plyer import notification
                notification.notify(
                    title=title,
                    message=message,
                    app_name="NetGuard AI",
                    timeout=5
                )

            elif self.notifier == "win10toast":
                from win10toast import ToastNotifier
                toaster = ToastNotifier()
                toaster.show_toast(title, message, duration=5, threaded=True)

            elif self.notifier == "native":
                import ctypes
                ctypes.windll.user32.MessageBoxW(0, message, title, 0x40)

        except Exception as e:
            print(f"[Alert] Notification error: {e}")
            print(f"  → {title}: {message}")

    def _play_sound(self, alert_type):
        try:
            if self.sound_available == "winsound":
                import winsound
                if alert_type == "threat":
                    # Urgent beep
                    for _ in range(3):
                        winsound.Beep(1000, 300)
                        time.sleep(0.1)
                else:
                    winsound.Beep(700, 400)

            elif self.sound_available == "pygame":
                import pygame
                # Simple tone generate karo
                import numpy as np
                freq = 1000 if alert_type == "threat" else 700
                duration = 0.4
                sample_rate = 44100
                t = np.linspace(0, duration, int(sample_rate * duration))
                wave = (np.sin(2 * np.pi * freq * t) * 32767).astype(np.int16)
                sound = pygame.sndarray.make_sound(np.column_stack([wave, wave]))
                sound.play()
                time.sleep(duration)

        except Exception as e:
            print(f"[Alert] Sound error: {e}")
