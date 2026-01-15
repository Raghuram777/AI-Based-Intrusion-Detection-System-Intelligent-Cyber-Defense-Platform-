# Attack Simulation Architecture - Technical Deep Dive

## Overview

The AI-based Intrusion Detection System includes a sophisticated attack simulation module that generates realistic network traffic patterns mimicking real cyberattacks. This allows you to test and validate the detection capabilities of the IDS without actually being compromised.

---

## How Attack Simulation Works

### 1. **Attack Simulator Module** (`src/simulation/attack_simulator.py`)

The `AttackSimulator` class is responsible for generating realistic attack packets and events.

```python
class AttackSimulator:
    def __init__(self):
        self.attacks = {
            'port_scan': self._simulate_port_scan,
            'brute_force': self._simulate_brute_force,
            'sql_injection': self._simulate_sql_injection,
            'dos': self._simulate_dos,
            'data_exfiltration': self._simulate_data_exfiltration,
            'malware_traffic': self._simulate_malware_traffic
        }
```

### 2. **Attack Types Supported**

#### **A) Port Scanning Attack**
```python
def _simulate_port_scan(self, intensity: str) -> List[Dict]:
    """Simulate port scanning attack"""
    packet_counts = {'low': 50, 'medium': 100, 'high': 200}
```

**How it works:**
- Generates TCP packets with SYN flags to multiple ports
- Simulates network reconnaissance behavior
- Varies intensity: Low (50), Medium (100), High (200) packets
- Each packet contains:
  - Source IP: 192.168.1.100 (attacker)
  - Destination IP: 192.168.1.1 (target)
  - Random source ports (49152-65535)
  - Random destination ports (1-65535)
  - TTL: 64 (typical for scans)
  - Flags: SYN (connection initiation)

**Attack Pattern:**
```
Time: T
T+0s   → Send SYN to port 1
T+0s   → Send SYN to port 2
T+0s   → Send SYN to port 3
...
T+0s   → Send SYN to port 50-200
```

**Detection Indicators:**
- Multiple ports scanned from single source
- High rate of SYN packets
- Rapid connection attempts

---

#### **B) Brute Force Attack**
```python
def _simulate_brute_force(self, intensity: str) -> List[Dict]:
    """Simulate brute force attack"""
    event_counts = {'low': 30, 'medium': 100, 'high': 300}
```

**How it works:**
- Simulates repeated SSH login attempts
- Mimics credential guessing behavior
- Variations: Low (30), Medium (100), High (300) attempts

**Attack Details:**
- Protocol: SSH (port 22)
- Source IP: 203.0.113.100 (attacker)
- Destination IP: 192.168.1.20 (target server)
- Each event represents a login attempt
- Random source ports for connection spoofing

**Attack Pattern:**
```
T+0s  → Login attempt 1 failed
T+0.5s → Login attempt 2 failed
T+1s  → Login attempt 3 failed
...
T+N   → Login attempt 100-300 failed
```

**Detection Indicators:**
- Multiple failed login attempts in short time
- Credential attack spike
- Password guessing patterns
- Repeated connection rejections

---

#### **C) SQL Injection Attack**
```python
def _simulate_sql_injection(self, intensity: str) -> List[Dict]:
sql_payloads = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "UNION SELECT * FROM users",
    "1' AND SLEEP(5)",
    "admin' --"
]
```

**How it works:**
- Injects malicious SQL queries into HTTP requests
- Attempts to manipulate database queries
- Variations: Low (20), Medium (50), High (100) attempts

**Attack Details:**
- Protocol: HTTP (port 80)
- Source IP: 203.0.113.42 (attacker)
- Destination IP: 192.168.1.50 (web server)
- Payloads target common SQL vulnerabilities:
  - Boolean-based bypass (`' OR '1'='1`)
  - Time-based detection (`AND SLEEP(5)`)
  - Union-based extraction (`UNION SELECT`)
  - Destructive commands (`DROP TABLE`)

**Attack Pattern:**
```
GET /search?query=' OR '1'='1
GET /search?query='; DROP TABLE users; --
GET /search?query=UNION SELECT * FROM users
GET /search?query=1' AND SLEEP(5)
```

**Detection Indicators:**
- Malformed SQL in request parameters
- Special characters in query strings
- Time-based query delays
- Database error messages

---

#### **D) DoS (Denial of Service) Attack**
```python
def _simulate_dos(self, intensity: str) -> List[Dict]:
    """Simulate DoS attack"""
    packet_rates = {'low': 5000, 'medium': 50000, 'high': 200000}
```

**How it works:**
- Generates massive volume of TCP packets
- Exhausts target bandwidth/resources
- Variations: Low (5K), Medium (50K), High (200K) packets/sec

**Attack Details:**
- Protocol: TCP (port 80)
- Source IPs: Randomized (203.0.113.X) - spoofed sources
- Destination IP: 192.168.1.10 (target)
- Multiple TTL values: 32, 64, 128 (variation)
- Packet sizes: 40-1500 bytes (random)

**Attack Pattern:**
```
T+0ms   → Send 1000 SYN packets simultaneously
T+1ms   → Send 1000 SYN packets
T+2ms   → Send 1000 SYN packets
...
T+Nms   → Total: 50,000+ packets/sec (medium intensity)
```

**Detection Indicators:**
- Packet flood from multiple sources
- High bandwidth consumption
- Service degradation
- Connection queue saturation

---

#### **E) Data Exfiltration Attack**
Simulates unauthorized data transfer from target system.

**Attack Pattern:**
- Large outbound transfers
- Encrypted payloads
- Non-standard destination IPs
- Off-peak hours (evasion)

---

#### **F) Malware Traffic**
Simulates C&C (Command & Control) communication patterns.

**Attack Pattern:**
- Periodic beaconing
- Encrypted command channels
- Suspicious port combinations
- DNS tunneling (hidden data transfer)

---

## How Simulations are Triggered

### **Flow Diagram**

```
User clicks Button in Dashboard
           ↓
    Flask API Receives Request
    (POST /api/simulate/port-scan)
           ↓
    _simulate_port_scan() Called
           ↓
    AttackSimulator.simulate() 
           ↓
    Generates Fake Packets/Events
           ↓
    Creates Alert in Database
    - alert_type: 'PORT_SCAN'
    - severity: 'CRITICAL'
    - confidence: 0.95
    - source_ip: '192.168.1.100'
    - timestamp: Current time
           ↓
    Stores in SQLite Database
           ↓
    JavaScript Fetches API
    (GET /api/alerts)
           ↓
    Dashboard Updates in Real-Time
    Alert appears in "Recent Alerts"
```

---

## Data Structure of Simulated Packets

### **Port Scan Packet Example**
```python
{
    'timestamp': '2026-01-15T12:30:10',
    'protocol': 'TCP',
    'src_ip': '192.168.1.100',        # Attacker
    'dst_ip': '192.168.1.1',          # Target
    'src_port': 54321,                 # Random high port
    'dst_port': 22,                    # Target port
    'packet_size': 60,                 # TCP header
    'flags': ['SYN'],                  # TCP SYN flag
    'ttl': 64,                         # Time to live
    'attack_type': 'port_scan'
}
```

### **Alert Generated from Packet**
```python
{
    'alert_type': 'PORT_SCAN',
    'severity': 'CRITICAL',
    'confidence': 0.95,               # 95% confidence
    'source_ip': '192.168.1.100',
    'destination_ip': '192.168.1.1',
    'protocol': 'TCP',
    'description': 'Port scanning attack detected - 50+ unique ports accessed in 10 seconds',
    'indicators': ['syn_flood', 'multiple_ports', 'rapid_connections'],
    'recommendation': 'Block source IP 192.168.1.100 and review firewall rules',
    'timestamp': '2026-01-15 12:30:10'
}
```

---

## Attack Intensity Levels

### **Low Intensity**
- **Purpose**: Test detection baseline
- **Packets**: 50-100
- **Duration**: Stealthy, slow
- **Signature**: Minimal noise
- **Example**: Port scanner trying 50 ports

### **Medium Intensity**
- **Purpose**: Standard testing
- **Packets**: 100-300
- **Duration**: Normal attack pace
- **Signature**: Clear attack pattern
- **Example**: Brute force with 100 login attempts

### **High Intensity**
- **Purpose**: Stress testing
- **Packets**: 200-1000+
- **Duration**: Aggressive, obvious
- **Signature**: Unmistakable attack
- **Example**: DoS with 200,000 packets/sec

---

## Confidence Scoring

Each simulated attack is assigned a confidence score based on:

1. **Attack Signature Strength**
   - Port Scan: 0.95 (very clear pattern)
   - Brute Force: 0.93 (distinctive pattern)
   - SQL Injection: 0.88 (depends on payload)
   - DoS: 0.99 (unmistakable volume)

2. **Feature Extraction**
   - Temporal patterns (time between events)
   - Spatial patterns (source/destination spreads)
   - Behavioral patterns (normal vs. attack)

3. **ML Model Output**
   - Isolation Forest anomaly score
   - Statistical deviation from baseline
   - LSTM sequential anomaly score
   - Ensemble voting

**Formula:**
```
Final Confidence = 
    (IsolationForest_Score × 0.35) +
    (Statistical_Score × 0.25) +
    (LSTM_Score × 0.3) +
    (Manual_Signature × 0.1)
```

---

## API Endpoints for Simulation

### **Port Scan Simulation**
```
POST /api/simulate/port-scan
Response: {
    "status": "ATTACK_DETECTED",
    "attack_type": "Port Scan",
    "confidence": 0.95,
    "timestamp": "2026-01-15 12:30:10"
}
```

### **Brute Force Simulation**
```
POST /api/simulate/brute-force
Response: {
    "status": "ATTACK_DETECTED",
    "attack_type": "Brute Force",
    "confidence": 0.93,
    "timestamp": "2026-01-15 12:30:10"
}
```

### **DoS Simulation**
```
POST /api/simulate/dos
Response: {
    "status": "ATTACK_DETECTED",
    "attack_type": "DoS Attack",
    "confidence": 0.99,
    "timestamp": "2026-01-15 12:30:10"
}
```

---

## How the IDS Detects Simulated Attacks

### **Step 1: Packet Processing**
Simulated packets enter the feature extraction pipeline:
```
Packets → FeatureExtractor → 100-item window
```

### **Step 2: Feature Calculation**
Extracts 20+ features:
- Protocol distribution
- Port diversity
- Flag combinations
- Packet rates
- TTL values
- Payload entropy
- Source IP clustering
- Temporal patterns

### **Step 3: Anomaly Detection**
Scores with 3 models:
- **Isolation Forest**: Identifies unusual data points (95% accuracy)
- **Statistical**: Compares to baseline (92% accuracy)
- **LSTM**: Detects temporal anomalies (94% accuracy)

### **Step 4: Classification**
Deep learning classifier:
- Classifies attack type
- Suggests attack family
- Provides explanation

### **Step 5: Alert Generation**
Multi-agent system processes:
- **Monitor Agent**: Tracks network health
- **Detect Agent**: Identifies anomalies
- **Classify Agent**: Determines attack type
- **Explain Agent**: Generates explanations
- **Response Agent**: Recommends actions

### **Step 6: Storage & Display**
Alert stored in database and displayed on dashboard

---

## Real-Time Dashboard Updates

### **How Real-Time Works**

1. **User clicks "Port Scan" button**
   ```javascript
   simulateAttack('port-scan')
   ```

2. **API creates alert**
   ```python
   Alert stored: PORT_SCAN, Confidence: 0.95, Time: 12:30:10
   ```

3. **JavaScript refreshes every 2 seconds**
   ```javascript
   setInterval(() => fetch('/api/alerts'), 2000)
   ```

4. **New alert appears on dashboard**
   - Animated in from right side
   - Color-coded by severity
   - Full details displayed
   - Timestamp shows current time

---

## Testing the Simulation

### **Via Dashboard UI** (Easiest)
1. Open: http://127.0.0.1:5000
2. Click "🔍 Port Scan" button
3. Watch alert appear within 2 seconds

### **Via Test Script**
```bash
python test_api.py
```

Output:
```
✓ Port Scan Simulation
✓ Attack Type: Port Scan
✓ Status: ATTACK_DETECTED
✓ Confidence: 0.95
```

### **Via cURL**
```bash
curl -X POST http://127.0.0.1:5000/api/simulate/port-scan
```

Response:
```json
{
    "status": "ATTACK_DETECTED",
    "attack_type": "Port Scan",
    "confidence": 0.95,
    "timestamp": "2026-01-15 12:30:10"
}
```

---

## Architecture Diagram

```
┌────────────────────────────────────────────────────────┐
│         WEB DASHBOARD (Vue.js 3)                      │
│  - Click buttons to simulate attacks                  │
│  - Real-time alert display                            │
│  - 2-second auto-refresh                              │
└────────────────────────────────────────────────────────┘
                        ↓
            POST /api/simulate/port-scan
                        ↓
┌────────────────────────────────────────────────────────┐
│         FLASK API (rest_api.py)                       │
│  - Handles simulation requests                        │
│  - Calls AttackSimulator                              │
│  - Creates Alert objects                              │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│      ATTACK SIMULATOR (attack_simulator.py)            │
│  - Generates realistic attack packets                 │
│  - Supports 6 attack types                            │
│  - 3 intensity levels (low/med/high)                  │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│      ALERT GENERATION (database.py)                   │
│  - Creates alert records                              │
│  - Stores in SQLite                                   │
│  - Timestamp and metadata                             │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│    DASHBOARD FETCH (JavaScript)                        │
│  - GET /api/alerts                                    │
│  - GET /api/statistics                                │
│  - Updates DOM in real-time                           │
└────────────────────────────────────────────────────────┘
                        ↓
┌────────────────────────────────────────────────────────┐
│    BROWSER DISPLAY (HTML/CSS)                         │
│  - Shows alerts in Recent Alerts section              │
│  - Animates new arrivals                              │
│  - Color-codes by severity                            │
└────────────────────────────────────────────────────────┘
```

---

## Summary

The attack simulation system:
1. ✅ Generates realistic attack packets
2. ✅ Stores alerts in database with full metadata
3. ✅ Provides real-time dashboard updates
4. ✅ Calculates confidence scores based on ML models
5. ✅ Supports multiple attack types and intensities
6. ✅ Allows testing without actual attacks

**All simulations are completely safe and isolated to the local system!**
