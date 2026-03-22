<div align="center">
🛡️ NetGuard AI
AI-Powered Network Intrusion Detection System
Show Image
Show Image
Show Image
Show Image
Show Image
A real-time AI-powered network monitoring tool that silently runs in the background, detects anomalies using Machine Learning, and instantly alerts you when suspicious activity is found on your system.
Features • Architecture • Installation • Usage • Tech Stack
</div>

🔍 What is NetGuard AI?
Traditional firewalls rely on static rules — if a pattern matches, block it. But modern network threats don't always follow known patterns.
NetGuard AI goes a step further by using Isolation Forest (unsupervised Machine Learning) to learn what normal traffic looks like on your system — and automatically flags anything that deviates from that baseline.

Built by a cybersecurity researcher who wanted a smarter, always-on threat detection layer for Windows.


✨ Features

🤖 AI Anomaly Detection — Isolation Forest ML model learns your network's normal behavior and detects outliers
🔍 Real-Time Monitoring — Scans all active connections every 8 seconds (IP, port, process, status)
🚨 Instant Alerts — Windows desktop notification + sound alert on threat detection
📊 Live Dashboard — Cyberpunk-themed real-time dashboard with threat scoring
🖥️ System Tray Integration — Runs silently in background, right-click to open dashboard or stop
🎯 Threat Scoring — Every connection scored 0.0 → 1.0 with SAFE / WARNING / DANGER levels
🆕 New IP Detection — Flags and logs every new IP that connects to your system
🔄 Multi-threaded — 4 parallel threads ensure monitoring never blocks the UI


🏗️ Architecture
┌─────────────────────────────────────────────┐
│              NetGuard AI Core               │
│                                             │
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │   Monitor   │───▶│     AI Engine       │ │
│  │   Thread    │    │  (Isolation Forest) │ │
│  └─────────────┘    └─────────────────────┘ │
│         │                     │             │
│         ▼                     ▼             │
│  ┌─────────────┐    ┌─────────────────────┐ │
│  │    Alert    │    │    Flask Server     │ │
│  │   Thread    │    │  (Dashboard API)    │ │
│  └─────────────┘    └─────────────────────┘ │
│         │                     │             │
│         ▼                     ▼             │
│  Desktop Notification    Browser Dashboard  │
│  + Sound Alert           localhost:5000     │
└─────────────────────────────────────────────┘
Threat Scoring System
ScoreLevelAction0.0 – 0.3🟢 SAFENo action0.3 – 0.6🟡 WARNINGLogged0.6 – 1.0🔴 DANGERAlert fired immediately
Score = (Rule-based score × 0.4) + (AI anomaly score × 0.6)

📁 Project Structure
NetGuard-AI/
├── netguard.py       # Main entry point — run this
├── monitor.py        # Network scanner (psutil)
├── ai_engine.py      # Isolation Forest anomaly detection
├── alerts.py         # Desktop notifications + sound
├── server.py         # Flask API server
├── tray.py           # Windows system tray icon
├── dashboard.html    # Real-time cyberpunk dashboard
└── requirements.txt  # Python dependencies

⚙️ Installation
Prerequisites

Windows OS
Python 3.8 or higher

Step 1 — Clone the Repository
bashgit clone https://github.com/ghostempireis/NetGuard-AI.git
cd NetGuard-AI
Step 2 — Install Dependencies
bashpip install -r requirements.txt
Step 3 — Run NetGuard AI
bashpython netguard.py
Dashboard will automatically open at http://localhost:5000 🚀

🚀 Usage
bashpython netguard.py
Once running:

📊 Dashboard opens automatically in your browser
🖥️ System tray icon appears in taskbar corner
🔔 Alerts fire automatically when threats are detected

Stopping NetGuard

Option 1: Right-click system tray icon → "NetGuard Band Karo"
Option 2: Press Ctrl + C in Command Prompt


🛠️ Tech Stack
ComponentTechnologyNetwork MonitoringpsutilAI / ML Enginescikit-learn — Isolation ForestNumerical ComputingnumpyWeb DashboardFlask + Flask-CORSDesktop NotificationsplyerSound Alertswinsound (built-in Windows)System Traypystray + PillowFrontendHTML5, CSS3, Vanilla JS

🤖 How the AI Works
NetGuard uses Isolation Forest — an unsupervised anomaly detection algorithm that:

Learns normal network behavior from your system (baseline phase)
Scores every new connection based on how "isolated" it is from normal patterns
Flags statistical outliers as potential threats — no labeled attack data needed

This approach is ideal for network security because attack patterns are unpredictable and constantly evolving.

🗺️ Roadmap

 Real-time network monitoring
 AI anomaly detection (Isolation Forest)
 Desktop notifications + sound alerts
 System tray background service
 Live cyberpunk dashboard
 AbuseIPDB API integration (malicious IP reputation check)
 Email alert support
 IP whitelisting via dashboard
 Packet-level deep inspection (Scapy)
 Cross-platform support (Linux/Mac)


⚠️ Disclaimer
NetGuard AI is built for educational and personal security research purposes. Use responsibly and only on systems you own or have permission to monitor.

👤 Author
Ghost Empire — Cybersecurity Researcher
Show Image

<div align="center">
⭐ Agar helpful laga toh star dena! ⭐
</div>
