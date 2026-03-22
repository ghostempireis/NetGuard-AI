"""
NetGuard AI - AI Engine
Isolation Forest se anomaly detection karta hai
"""

import numpy as np

# Suspicious ports list
SUSPICIOUS_PORTS = {
    22, 23, 25, 445, 1433, 1521, 3306, 3389,
    4444, 5900, 6667, 8080, 8443, 9001, 31337
}

# Known safe port ranges
SAFE_PORTS = {80, 443, 53, 123, 67, 68}


class AIEngine:
    def __init__(self):
        self.model = None
        self.trained = False
        self.training_data = []
        self.min_samples = 20  # Itne samples ke baad train hoga

        # Try sklearn
        try:
            from sklearn.ensemble import IsolationForest
            self.IsolationForest = IsolationForest
            self.sklearn_available = True
        except ImportError:
            self.sklearn_available = False
            print("[AI] scikit-learn nahi mila, rule-based scoring use hoga.")

    def extract_features(self, conn):
        """Connection se numeric features nikalte hain"""
        port = conn.get("remote_port", 0)
        features = [
            float(port),
            1.0 if port in SUSPICIOUS_PORTS else 0.0,
            1.0 if port in SAFE_PORTS else 0.0,
            1.0 if conn.get("status") == "ESTABLISHED" else 0.0,
            float(port > 49151),   # Ephemeral port
            float(port < 1024),    # Well-known port
        ]
        return features

    def train(self, connections):
        """Model ko current connections se train karo"""
        if not self.sklearn_available or len(connections) < self.min_samples:
            return

        try:
            data = [self.extract_features(c) for c in connections]
            self.training_data.extend(data)

            # Last 500 samples rakho
            self.training_data = self.training_data[-500:]

            if len(self.training_data) >= self.min_samples:
                X = np.array(self.training_data)
                self.model = self.IsolationForest(
                    contamination=0.1,
                    random_state=42,
                    n_estimators=50
                )
                self.model.fit(X)
                self.trained = True
        except Exception as e:
            print(f"[AI] Training error: {e}")

    def score(self, conn):
        """
        Connection ka threat score nikalo (0.0 = safe, 1.0 = dangerous)
        """
        base_score = self._rule_based_score(conn)

        if self.trained and self.sklearn_available and self.model:
            try:
                features = np.array([self.extract_features(conn)])
                # IsolationForest: -1 = anomaly, 1 = normal
                raw = self.model.decision_function(features)[0]
                # -0.5 to 0.5 range → 0 to 1 range mein convert
                ai_score = max(0.0, min(1.0, 0.5 - raw))
                # Rule-based aur AI score mix karo
                final = (base_score * 0.4) + (ai_score * 0.6)
                return round(final, 3)
            except:
                pass

        return round(base_score, 3)

    def _rule_based_score(self, conn):
        """Simple rule-based scoring"""
        score = 0.0
        port = conn.get("remote_port", 0)

        if port in SUSPICIOUS_PORTS:
            score += 0.6

        # Very high ports (potential backdoors)
        if port > 60000:
            score += 0.3

        # Non-standard ports
        if port not in SAFE_PORTS and port not in SUSPICIOUS_PORTS:
            if port > 1024:
                score += 0.1

        return min(score, 1.0)

    def level(self, score):
        """Score ko level mein convert karo"""
        if score < 0.3:
            return "safe"
        elif score < 0.6:
            return "warning"
        else:
            return "danger"
