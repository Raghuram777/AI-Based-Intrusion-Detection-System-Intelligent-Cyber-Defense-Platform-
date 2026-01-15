# Deployment & Usage Guide

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installation](#installation)
3. [Running the System](#running-the-system)
4. [Web Dashboard Access](#web-dashboard-access)
5. [API Usage](#api-usage)
6. [Attack Simulation](#attack-simulation)
7. [Troubleshooting](#troubleshooting)
8. [Configuration](#configuration)

---

## System Requirements

### Minimum Requirements
- **OS**: Windows 10+, Linux (Ubuntu 20.04+), macOS 11+
- **Python**: 3.10 or higher (tested on 3.12)
- **RAM**: 2GB minimum, 4GB recommended
- **Disk Space**: 500MB for installation + database
- **Network**: For real packet capture (admin/root privileges required)

### Recommended Setup
- **CPU**: Multi-core processor (4+ cores)
- **RAM**: 8GB
- **Network**: Gigabit Ethernet for real-time capture
- **OS**: Linux for production deployment

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/Raghuram777/AI-Based-Intrusion-Detection-System-Intelligent-Cyber-Defense-Platform-.git
cd "AI based Intrusion detection System"
```

### Step 2: Set Up Virtual Environment
**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation
```bash
python -c "import numpy, pandas, sklearn, flask, scapy; print('All dependencies OK')"
```

---

## Running the System

### Method 1: Complete System (Recommended)
Runs all phases with training, testing, and web dashboard.

```bash
cd src
python complete_system.py
```

**Expected Output:**
```
================================================================================
INITIALIZING PRODUCTION AI-POWERED INTRUSION DETECTION SYSTEM
================================================================================
[TRAINING PHASE] Training ML models on baseline data...
[OK] Isolation Forest trained
[OK] Statistical baseline learned
[OK] LSTM detector trained

[COMPREHENSIVE SYSTEM TEST - ALL ATTACK TYPES]
[TEST 1/4] Normal Traffic Processing...
[TEST 2/4] Port Scan Detection...
[TEST 3/4] Brute Force Detection...
[TEST 4/4] DoS Attack Detection...

**COMPREHENSIVE TEST COMPLETED SUCCESSFULLY**

**PRODUCTION AI-IDS READY**
Dashboard: http://127.0.0.1:5000
Press Ctrl+C to shutdown
```

### Method 2: Core IDS Only (No Dashboard)
For headless/server deployments.

```bash
cd src
python main.py
```

### Method 3: Custom Configuration
Edit `src/utils/config.py` before running:
- Change port: `api_port = 8080`
- Modify thresholds: `anomaly_threshold = 0.85`
- Adjust database: `db_path = "/custom/path/ids.db"`

---

## Web Dashboard Access

### Opening the Dashboard

Once the system is running, open your web browser and navigate to:

**URL**: `http://127.0.0.1:5000`

Or from another machine on your network:

**URL**: `http://<YOUR_IP_ADDRESS>:5000`

### Dashboard Components

#### 1. System Status
- **Uptime**: Time system has been running
- **Status**: OPERATIONAL / ALERTING
- **Last Event**: Timestamp of last detection

#### 2. Alert Statistics
- **Today's Alerts**: Count for current day
- **Severity Breakdown**: Critical, High, Medium, Low distribution
- **Last 24 Hours**: Graph visualization

#### 3. ML Models Performance
- **Isolation Forest**: Accuracy percentage
- **Statistical Detector**: Accuracy percentage
- **Attack Classifier**: Accuracy percentage
- **Last Training**: Model update timestamp

#### 4. Recent Alerts
- **Alert ID**: Unique identifier
- **Type**: Attack classification
- **Severity**: Alert priority level
- **Confidence**: Detection confidence (0-100%)
- **Source IP**: Attack origin
- **Timestamp**: Detection time
- **Actions**: Acknowledge, Mark as False Positive

#### 5. Attack Simulation Lab
Interactive buttons to trigger simulated attacks:
- **🎯 Simulate Port Scan**: Generate port scanning traffic
- **🔐 Simulate Brute Force**: Generate login attempts
- **⚡ Simulate DoS**: Generate denial of service attack

### Real-Time Updates
Dashboard automatically refreshes every 5 seconds for real-time monitoring.

---

## API Usage

### Base URL
```
http://127.0.0.1:5000/api
```

### Authentication
Currently no authentication required. For production, add:
```python
# In flask_api.py
from functools import wraps
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = request.headers.get('X-API-Key')
        if key != os.getenv('API_KEY'):
            return {'error': 'Invalid API key'}, 401
        return f(*args, **kwargs)
    return decorated_function
```

### Endpoints

#### 1. Get System Status
**Request:**
```bash
curl http://127.0.0.1:5000/api/status
```

**Response:**
```json
{
  "status": "operational",
  "uptime": 3600,
  "alerts_today": 5,
  "last_alert": "2026-01-15 12:00:00"
}
```

#### 2. Get Recent Alerts
**Request:**
```bash
curl http://127.0.0.1:5000/api/alerts?hours=24&limit=10
```

**Response:**
```json
{
  "alerts": [
    {
      "id": 1,
      "type": "port_scan",
      "severity": "HIGH",
      "confidence": 0.95,
      "source_ip": "192.168.1.100",
      "timestamp": "2026-01-15 12:05:23"
    }
  ],
  "count": 1
}
```

#### 3. Acknowledge Alert
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/alerts/1/acknowledge
```

**Response:**
```json
{
  "success": true,
  "message": "Alert 1 acknowledged"
}
```

#### 4. Mark as False Positive
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/alerts/1/false-positive
```

**Response:**
```json
{
  "success": true,
  "message": "Alert 1 marked as false positive - Model updated"
}
```

#### 5. Get Statistics
**Request:**
```bash
curl "http://127.0.0.1:5000/api/statistics?hours=24"
```

**Response:**
```json
{
  "total_alerts": 5,
  "severity_distribution": {
    "CRITICAL": 0,
    "HIGH": 2,
    "MEDIUM": 2,
    "LOW": 1
  },
  "average_confidence": 0.85,
  "attacks_by_type": {
    "port_scan": 2,
    "dos": 1,
    "brute_force": 2
  }
}
```

#### 6. Get ML Models Status
**Request:**
```bash
curl http://127.0.0.1:5000/api/models/status
```

**Response:**
```json
{
  "models": {
    "isolation_forest": {"accuracy": 0.95, "last_trained": "2026-01-15"},
    "statistical": {"accuracy": 0.92, "last_trained": "2026-01-15"},
    "lstm": {"accuracy": 0.94, "last_trained": "2026-01-15"}
  }
}
```

#### 7. Simulate Attack
**Request:**
```bash
curl -X POST http://127.0.0.1:5000/api/simulate/attack \
  -H "Content-Type: application/json" \
  -d '{"type": "port_scan", "intensity": "high"}'
```

**Response:**
```json
{
  "success": true,
  "alert_id": 42,
  "attack_type": "port_scan",
  "confidence": 0.95
}
```

---

## Attack Simulation

### Using the Web Dashboard
1. Open http://127.0.0.1:5000
2. Scroll to "Attack Simulation Lab"
3. Click desired attack button
4. Watch alerts appear in real-time

### Using API
```bash
# Port Scan
curl -X POST http://127.0.0.1:5000/api/simulate/port-scan \
  -d '{"intensity": "high"}'

# Brute Force
curl -X POST http://127.0.0.1:5000/api/simulate/brute-force \
  -d '{"intensity": "medium"}'

# DoS Attack
curl -X POST http://127.0.0.1:5000/api/simulate/dos \
  -d '{"intensity": "high"}'
```

### Using Python
```python
from src.simulation import AttackSimulator

sim = AttackSimulator()

# Port Scan
packets = sim.simulate('port_scan', intensity='high')
print(f"Generated {len(packets)} port scan packets")

# Brute Force
packets = sim.simulate('brute_force', intensity='medium')
print(f"Generated {len(packets)} brute force events")

# SQL Injection
packets = sim.simulate('sql_injection', intensity='high')
print(f"Generated {len(packets)} SQL injection packets")

# DoS Attack
packets = sim.simulate('dos', intensity='high')
print(f"Generated {len(packets)} DoS packets")

# Data Exfiltration
packets = sim.simulate('data_exfiltration', intensity='medium')
print(f"Generated {len(packets)} exfiltration packets")

# Malware Traffic
packets = sim.simulate('malware_traffic', intensity='high')
print(f"Generated {len(packets)} malware traffic packets")
```

### Pre-Built Scenarios
```python
from src.simulation import IntrusionScenario

scenario = IntrusionScenario()

# Advanced Persistent Threat
attacks = scenario.scenario_advanced_persistent_threat()
print(f"APT scenario: {len(attacks)} stages")

# DDoS Attack
attacks = scenario.scenario_ddos_attack()
print(f"DDoS scenario: {len(attacks)} sources")

# Insider Threat
attacks = scenario.scenario_insider_threat()
print(f"Insider threat: {len(attacks)} stages")
```

---

## Troubleshooting

### Issue: "Address already in use" on port 5000
**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <PID> /F

# Or use different port in complete_system.py
ids = ProductionAIIDS(enable_api=True, api_port=8080)
```

### Issue: Database locked
**Solution:**
```bash
# Close all running instances
# Delete database file
rm ../data/ids.db

# Restart system (database will be recreated)
python complete_system.py
```

### Issue: Import errors
**Solution:**
```bash
# Reinstall dependencies
pip uninstall -r requirements.txt -y
pip install -r requirements.txt

# Verify installation
python -c "from src.data_collection import PacketSniffer; print('OK')"
```

### Issue: Permission denied on packet capture
**Windows:**
```bash
# Run Python as Administrator
# Or use mock mode by editing config.py
packet_sniffer = PacketSniffer(use_mock=True)
```

**Linux:**
```bash
# Grant packet capture permissions
sudo setcap cap_net_raw=ep /path/to/python3

# Or run as sudo
sudo python complete_system.py
```

### Issue: Low detection accuracy
**Solution:**
1. Check model training data
2. Verify feature extraction
3. Review thresholds in config.py
4. Retrain models with more data

---

## Configuration

### Main Configuration File
**Location**: `src/utils/config.py`

```python
# API Configuration
API_HOST = '127.0.0.1'
API_PORT = 5000

# Detection Thresholds
ANOMALY_THRESHOLD = 0.7
CONFIDENCE_THRESHOLD = 0.5

# Feature Extraction
WINDOW_SIZE = 100
NUM_FEATURES = 26

# Model Parameters
CONTAMINATION = 0.1
ISOLATION_FOREST_TREES = 100

# Database
DB_PATH = '../data/ids.db'
MAX_ALERTS = 10000

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = '../logs/ids.log'
```

### Environment Variables
```bash
# .env file or system environment
export IDS_DB_PATH="/custom/path/ids.db"
export IDS_API_PORT=8080
export IDS_LOG_LEVEL=DEBUG
```

### Database Configuration
```python
# In utils/database.py
class Database:
    def __init__(self, db_path='../data/ids.db'):
        self.db_path = db_path
        # Modify as needed
```

---

## Production Deployment

### Using Gunicorn (Linux)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "src.api.flask_api:IDSFlaskAPI().app"
```

### Using Docker
```dockerfile
FROM python:3.12-slim
WORKDIR /ids
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ src/
CMD ["python", "src/complete_system.py"]
```

Build and run:
```bash
docker build -t ai-ids .
docker run -p 5000:5000 -v $(pwd)/data:/ids/data ai-ids
```

### Using Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-ids
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ai-ids
  template:
    metadata:
      labels:
        app: ai-ids
    spec:
      containers:
      - name: ai-ids
        image: ai-ids:latest
        ports:
        - containerPort: 5000
        volumeMounts:
        - name: data
          mountPath: /ids/data
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: ids-data-pvc
```

---

## Monitoring & Maintenance

### Check System Health
```bash
curl http://127.0.0.1:5000/api/status
```

### View Logs
```bash
tail -f ../logs/ids.log
```

### Database Backup
```bash
cp ../data/ids.db ../data/ids.db.backup.$(date +%Y%m%d)
```

### Model Retraining
```python
from src.complete_system import ProductionAIIDS
ids = ProductionAIIDS()
ids.train_models()  # Retrains on baseline data
```

---

## Performance Tuning

### Increase Detection Speed
```python
# Reduce feature extraction window
WINDOW_SIZE = 50  # Default: 100

# Use fewer trees in Isolation Forest
ISOLATION_FOREST_TREES = 50  # Default: 100
```

### Improve Detection Accuracy
```python
# Lower anomaly threshold
ANOMALY_THRESHOLD = 0.6  # Default: 0.7

# Collect more training data
# More baseline samples = better accuracy
```

### Optimize Memory
```python
# Reduce database retention
MAX_ALERTS = 5000  # Default: 10000

# Enable memory mapping
import mmap  # For large datasets
```

---

## Support & Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: See PROJECT_COMPLETE.md for architecture
- **Examples**: Check src/complete_system.py for usage patterns
- **Tests**: Run integration tests in src/

---

**Version**: 1.0
**Last Updated**: January 15, 2026
**Status**: Production Ready ✅
