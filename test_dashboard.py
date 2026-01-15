"""
Dashboard Test Script - Demonstrates the enhanced interactive dashboard
Run this after starting complete_system.py
"""

import requests
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000/api"

def print_status():
    """Print current system status"""
    try:
        resp = requests.get(f"{BASE_URL}/status")
        print("[SYSTEM STATUS]")
        print(resp.json())
        print()
    except Exception as e:
        print(f"Error: {e}\n")

def get_alerts():
    """Get current alerts"""
    try:
        resp = requests.get(f"{BASE_URL}/alerts")
        data = resp.json()
        print(f"[ALERTS] Total: {data.get('count', 0)}")
        if data.get('alerts'):
            for alert in data['alerts']:
                print(f"  - {alert.get('alert_type', 'Unknown')}: {alert.get('severity', 'N/A')} ({alert.get('confidence', 0)*100:.0f}%)")
        print()
    except Exception as e:
        print(f"Error: {e}\n")

def simulate_port_scan():
    """Simulate port scan attack"""
    try:
        print("[SIMULATING] Port Scan...")
        resp = requests.post(f"{BASE_URL}/simulate/port-scan")
        print(resp.json())
        print()
        time.sleep(1)
        get_alerts()
    except Exception as e:
        print(f"Error: {e}\n")

def simulate_brute_force():
    """Simulate brute force attack"""
    try:
        print("[SIMULATING] Brute Force...")
        resp = requests.post(f"{BASE_URL}/simulate/brute-force")
        print(resp.json())
        print()
        time.sleep(1)
        get_alerts()
    except Exception as e:
        print(f"Error: {e}\n")

def simulate_dos():
    """Simulate DoS attack"""
    try:
        print("[SIMULATING] DoS Attack...")
        resp = requests.post(f"{BASE_URL}/simulate/dos")
        print(resp.json())
        print()
        time.sleep(1)
        get_alerts()
    except Exception as e:
        print(f"Error: {e}\n")

def main():
    print("="*70)
    print("AI-IDS DASHBOARD TEST SCRIPT")
    print("="*70)
    print()
    
    print("STEPS:")
    print("1. Open http://127.0.0.1:5000 in your browser")
    print("2. Watch the dashboard while we simulate attacks")
    print("3. You should see alerts appearing in real-time")
    print()
    
    # Test 1: Check initial status
    print("TEST 1: Checking system status...")
    print_status()
    input("Press Enter to continue...")
    print()
    
    # Test 2: Simulate Port Scan
    print("TEST 2: Simulating Port Scan attack...")
    print("Check the dashboard - you should see the alert appear!")
    simulate_port_scan()
    input("Press Enter to continue...")
    print()
    
    # Test 3: Simulate Brute Force
    print("TEST 3: Simulating Brute Force attack...")
    print("The dashboard should update automatically!")
    simulate_brute_force()
    input("Press Enter to continue...")
    print()
    
    # Test 4: Simulate DoS
    print("TEST 4: Simulating DoS attack...")
    print("More alerts should appear!")
    simulate_dos()
    input("Press Enter to continue...")
    print()
    
    # Final status
    print("TEST 5: Final alert count...")
    get_alerts()
    
    print("="*70)
    print("ALL TESTS COMPLETE!")
    print("Dashboard Features:")
    print("  ✓ Real-time alert updates (refreshes every 2 seconds)")
    print("  ✓ Attack simulation buttons")
    print("  ✓ Alert severity indicators")
    print("  ✓ Confidence scores")
    print("  ✓ Source IP tracking")
    print("  ✓ Interactive interface")
    print("="*70)

if __name__ == '__main__':
    main()
