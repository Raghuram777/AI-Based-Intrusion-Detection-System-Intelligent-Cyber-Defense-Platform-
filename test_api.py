#!/usr/bin/env python3
"""
Dashboard API Test Script
Tests real-time updates and attack simulations
"""

import requests
import time
import json
import sys

BASE_URL = 'http://127.0.0.1:5000'

def test_alerts():
    """Test getting current alerts"""
    print('[TEST 1] Fetching current alerts...')
    try:
        response = requests.get(f'{BASE_URL}/api/alerts', timeout=5)
        if response.status_code == 200:
            data = response.json()
            alert_count = len(data.get('alerts', []))
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Current alerts: {alert_count}')
            return True
        else:
            print(f'✗ Status: {response.status_code}')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def test_statistics():
    """Test getting statistics"""
    print('\n[TEST 2] Fetching statistics...')
    try:
        response = requests.get(f'{BASE_URL}/api/statistics', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Total alerts: {data.get("total_alerts", 0)}')
            return True
        else:
            print(f'✗ Status: {response.status_code}')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def simulate_port_scan():
    """Simulate a port scan attack"""
    print('\n[TEST 3] Simulating Port Scan attack...')
    try:
        response = requests.post(f'{BASE_URL}/api/simulate/port-scan', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Attack Type: {data.get("attack_type")}')
            print(f'✓ Status: {data.get("status")}')
            print(f'✓ Confidence: {data.get("confidence")}')
            return True
        else:
            print(f'✗ Status: {response.status_code}')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def simulate_brute_force():
    """Simulate a brute force attack"""
    print('\n[TEST 4] Simulating Brute Force attack...')
    try:
        response = requests.post(f'{BASE_URL}/api/simulate/brute-force', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Attack Type: {data.get("attack_type")}')
            print(f'✓ Status: {data.get("status")}')
            print(f'✓ Confidence: {data.get("confidence")}')
            return True
        else:
            print(f'✗ Status: {response.status_code}')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def simulate_dos():
    """Simulate a DoS attack"""
    print('\n[TEST 5] Simulating DoS attack...')
    try:
        response = requests.post(f'{BASE_URL}/api/simulate/dos', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Attack Type: {data.get("attack_type")}')
            print(f'✓ Status: {data.get("status")}')
            print(f'✓ Confidence: {data.get("confidence")}')
            return True
        else:
            print(f'✗ Status: {response.status_code}')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def check_alerts_updated():
    """Check if alerts were updated after simulations"""
    print('\n[TEST 6] Checking if alerts were stored in database...')
    try:
        response = requests.get(f'{BASE_URL}/api/alerts', timeout=5)
        if response.status_code == 200:
            data = response.json()
            alert_count = len(data.get('alerts', []))
            print(f'✓ Status: {response.status_code}')
            print(f'✓ Total alerts in database: {alert_count}')
            
            if alert_count > 0:
                latest = data['alerts'][0]
                print(f'\nLatest Alert Details:')
                print(f'  Type: {latest.get("alert_type")}')
                print(f'  Severity: {latest.get("severity")}')
                print(f'  Confidence: {latest.get("confidence")}%')
                print(f'  Source IP: {latest.get("source_ip")}')
                print(f'  Timestamp: {latest.get("timestamp")}')
                return True
            else:
                print('✗ No alerts found in database')
                return False
        else:
            print(f'✗ Status: {response.status_code}')
            return False
    except Exception as e:
        print(f'✗ Error: {e}')
        return False

def main():
    """Run all tests"""
    print('=' * 70)
    print('DASHBOARD REAL-TIME UPDATE TEST')
    print('=' * 70)
    print(f'\nTesting API at: {BASE_URL}\n')
    
    results = []
    
    # Run tests
    results.append(('Fetch Alerts', test_alerts()))
    results.append(('Statistics', test_statistics()))
    
    # Wait for database to be ready
    print('\n⏳ Waiting 2 seconds for system stabilization...')
    time.sleep(2)
    
    # Simulate attacks
    results.append(('Port Scan Simulation', simulate_port_scan()))
    time.sleep(1)
    
    results.append(('Brute Force Simulation', simulate_brute_force()))
    time.sleep(1)
    
    results.append(('DoS Simulation', simulate_dos()))
    time.sleep(2)
    
    # Check if alerts were stored
    results.append(('Alerts Storage Check', check_alerts_updated()))
    
    # Print summary
    print('\n' + '=' * 70)
    print('TEST SUMMARY')
    print('=' * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = '✓ PASS' if result else '✗ FAIL'
        print(f'{status:8} | {test_name}')
    
    print('=' * 70)
    print(f'\nResults: {passed}/{total} tests passed')
    
    if passed == total:
        print('\n✓ ALL TESTS PASSED - Dashboard is working correctly!')
        return 0
    else:
        print(f'\n✗ {total - passed} test(s) failed')
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print('\n\nTest interrupted by user')
        sys.exit(1)
