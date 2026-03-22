==============================================
  🛡️  NetGuard AI — Setup Guide
==============================================

STEP 1: Libraries Install Karo
-------------------------------
Command Prompt kholo aur yeh command chalao:

  pip install -r requirements.txt


STEP 2: NetGuard Chalao
------------------------
Usi Command Prompt mein:

  python netguard.py

Bas! Dashboard automatically browser mein khul jaayega.


STEP 3: Kya dikhega?
---------------------
✅ Browser mein dashboard khulega → http://localhost:5000
✅ System tray mein shield icon aayega (taskbar corner)
✅ Har 8 second mein connections refresh honge
✅ Koi naaya ya suspicious IP aaya → notification + sound

STEP 4: Band Karna
-------------------
- System tray icon pe right-click karo
- "NetGuard Band Karo" pe click karo
- YA: Command Prompt mein Ctrl+C dabao


FEATURES:
---------
🔍 Live network connections monitor
🤖 AI anomaly detection (Isolation Forest)
🚨 Desktop notifications
🔊 Sound alerts
📊 Real-time dashboard
🛡️ System tray background service


FILES:
------
netguard.py    → Main file (yahi chalao)
monitor.py     → Network scanner
ai_engine.py   → AI detection
alerts.py      → Notifications & sound
server.py      → Dashboard server
tray.py        → System tray icon
dashboard.html → Visual dashboard


TROUBLESHOOTING:
----------------
Q: "Module not found" error aa raha hai?
A: pip install -r requirements.txt dobara chalao

Q: Dashboard nahi khul raha?
A: Browser mein manually kholo: http://localhost:5000

Q: System tray icon nahi aa raha?
A: pip install pystray pillow

==============================================
