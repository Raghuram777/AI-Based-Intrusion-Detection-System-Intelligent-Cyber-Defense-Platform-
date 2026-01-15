"""
Attack Simulation Tools
Simulate various cyberattacks for testing IDS detection capabilities
"""

import logging
from typing import List, Dict
import random
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class AttackSimulator:
    """Simulates various cyberattacks for testing"""
    
    def __init__(self):
        """Initialize attack simulator"""
        self.attacks = {
            'port_scan': self._simulate_port_scan,
            'brute_force': self._simulate_brute_force,
            'sql_injection': self._simulate_sql_injection,
            'dos': self._simulate_dos,
            'data_exfiltration': self._simulate_data_exfiltration,
            'malware_traffic': self._simulate_malware_traffic
        }
        logger.info("AttackSimulator initialized")
    
    def simulate(self, attack_type: str, intensity: str = 'medium') -> List[Dict]:
        """
        Simulate an attack.
        
        Args:
            attack_type: Type of attack to simulate
            intensity: 'low', 'medium', 'high'
            
        Returns:
            List of simulated packets/events
        """
        if attack_type not in self.attacks:
            logger.warning(f"Unknown attack type: {attack_type}")
            return []
        
        logger.info(f"Simulating {attack_type} attack ({intensity} intensity)")
        return self.attacks[attack_type](intensity)
    
    def _simulate_port_scan(self, intensity: str) -> List[Dict]:
        """Simulate port scanning attack"""
        packet_counts = {'low': 50, 'medium': 100, 'high': 200}
        packets = []
        
        for i in range(packet_counts.get(intensity, 50)):
            packet = {
                'timestamp': (datetime.now() - timedelta(seconds=i)).isoformat(),
                'protocol': 'TCP',
                'src_ip': '192.168.1.100',
                'dst_ip': '192.168.1.1',
                'src_port': random.randint(49152, 65535),
                'dst_port': random.randint(1, 65535),
                'packet_size': random.randint(40, 100),
                'payload_size': 0,
                'flags': ['SYN'],
                'ttl': 64,
                'attack_type': 'port_scan'
            }
            packets.append(packet)
        
        logger.info(f"Generated {len(packets)} port scan packets")
        return packets
    
    def _simulate_brute_force(self, intensity: str) -> List[Dict]:
        """Simulate brute force attack"""
        event_counts = {'low': 30, 'medium': 100, 'high': 300}
        packets = []
        
        for i in range(event_counts.get(intensity, 50)):
            packet = {
                'timestamp': (datetime.now() - timedelta(seconds=i)).isoformat(),
                'protocol': 'SSH',
                'src_ip': '203.0.113.100',
                'dst_ip': '192.168.1.20',
                'src_port': random.randint(49152, 65535),
                'dst_port': 22,
                'packet_size': random.randint(50, 200),
                'payload_size': random.randint(20, 100),
                'flags': ['PSH'],
                'ttl': 64,
                'attack_type': 'brute_force'
            }
            packets.append(packet)
        
        logger.info(f"Generated {len(packets)} brute force events")
        return packets
    
    def _simulate_sql_injection(self, intensity: str) -> List[Dict]:
        """Simulate SQL injection attack"""
        sql_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "UNION SELECT * FROM users",
            "1' AND SLEEP(5)",
            "admin' --"
        ]
        
        packet_counts = {'low': 20, 'medium': 50, 'high': 100}
        packets = []
        
        for i in range(packet_counts.get(intensity, 30)):
            packet = {
                'timestamp': (datetime.now() - timedelta(seconds=i)).isoformat(),
                'protocol': 'HTTP',
                'src_ip': '203.0.113.42',
                'dst_ip': '192.168.1.50',
                'src_port': random.randint(49152, 65535),
                'dst_port': 80,
                'packet_size': random.randint(100, 500),
                'payload_size': random.randint(50, 300),
                'payload': f"GET /search?query={random.choice(sql_payloads)}",
                'attack_type': 'sql_injection',
                'ttl': 64
            }
            packets.append(packet)
        
        logger.info(f"Generated {len(packets)} SQL injection packets")
        return packets
    
    def _simulate_dos(self, intensity: str) -> List[Dict]:
        """Simulate DoS attack"""
        packet_rates = {'low': 5000, 'medium': 50000, 'high': 200000}
        packets = []
        
        # Generate burst of packets
        for i in range(min(1000, packet_rates.get(intensity, 10000) // 100)):
            packet = {
                'timestamp': (datetime.now() - timedelta(milliseconds=i)).isoformat(),
                'protocol': 'TCP',
                'src_ip': f'203.0.113.{random.randint(1, 254)}',
                'dst_ip': '192.168.1.10',
                'src_port': random.randint(1024, 65535),
                'dst_port': 80,
                'packet_size': random.randint(40, 1500),
                'payload_size': random.randint(20, 1400),
                'flags': ['SYN'],
                'ttl': random.choice([32, 64, 128]),
                'attack_type': 'dos'
            }
            packets.append(packet)
        
        logger.info(f"Generated {len(packets)} DoS packets")
        return packets
    
    def _simulate_data_exfiltration(self, intensity: str) -> List[Dict]:
        """Simulate data exfiltration"""
        packet_counts = {'low': 100, 'medium': 500, 'high': 1000}
        packets = []
        
        for i in range(packet_counts.get(intensity, 200)):
            packet = {
                'timestamp': (datetime.now() - timedelta(seconds=i)).isoformat(),
                'protocol': 'TCP',
                'src_ip': '192.168.1.51',
                'dst_ip': f'203.0.113.{random.randint(1, 254)}',
                'src_port': random.randint(49152, 65535),
                'dst_port': 443,
                'packet_size': random.randint(1000, 1500),
                'payload_size': random.randint(800, 1450),
                'flags': ['ACK'],
                'ttl': 64,
                'attack_type': 'data_exfiltration'
            }
            packets.append(packet)
        
        logger.info(f"Generated {len(packets)} data exfiltration packets")
        return packets
    
    def _simulate_malware_traffic(self, intensity: str) -> List[Dict]:
        """Simulate malware C&C traffic"""
        c2_domains = ['malicious.com', 'botnet.net', 'phishing.org', 'exploit.io']
        packets = []
        
        packet_counts = {'low': 50, 'medium': 150, 'high': 300}
        
        for i in range(packet_counts.get(intensity, 100)):
            packet = {
                'timestamp': (datetime.now() - timedelta(seconds=i)).isoformat(),
                'protocol': 'TCP',
                'src_ip': '192.168.1.102',
                'dst_ip': f'203.0.113.{random.randint(1, 254)}',
                'src_port': random.randint(49152, 65535),
                'dst_port': 443,
                'packet_size': random.randint(100, 500),
                'payload_size': random.randint(50, 300),
                'domain': random.choice(c2_domains),
                'ttl': 64,
                'flags': ['ACK'],
                'attack_type': 'malware'
            }
            packets.append(packet)
        
        logger.info(f"Generated {len(packets)} malware traffic packets")
        return packets
    
    def get_available_attacks(self) -> List[str]:
        """Get list of available attack types"""
        return list(self.attacks.keys())


class IntrusionScenario:
    """Pre-built intrusion scenarios combining multiple attacks"""
    
    def __init__(self):
        """Initialize scenarios"""
        self.simulator = AttackSimulator()
    
    def scenario_advanced_persistent_threat(self) -> Dict:
        """
        Simulate an Advanced Persistent Threat (APT)
        Combines reconnaissance, exploitation, and exfiltration
        """
        logger.info("Simulating APT scenario")
        
        return {
            'name': 'Advanced Persistent Threat',
            'duration': '1 hour',
            'stages': [
                {
                    'stage': 'Reconnaissance',
                    'attack': self.simulator.simulate('port_scan', 'low'),
                    'duration': '10 minutes'
                },
                {
                    'stage': 'Initial Access',
                    'attack': self.simulator.simulate('brute_force', 'medium'),
                    'duration': '15 minutes'
                },
                {
                    'stage': 'Exploitation',
                    'attack': self.simulator.simulate('sql_injection', 'medium'),
                    'duration': '10 minutes'
                },
                {
                    'stage': 'Data Exfiltration',
                    'attack': self.simulator.simulate('data_exfiltration', 'high'),
                    'duration': '25 minutes'
                }
            ]
        }
    
    def scenario_ddos_attack(self) -> Dict:
        """Simulate a distributed DoS attack"""
        logger.info("Simulating DDoS scenario")
        
        return {
            'name': 'Distributed Denial of Service',
            'duration': '30 minutes',
            'attack': self.simulator.simulate('dos', 'high'),
            'sources': f"50+ compromised hosts",
            'target_bandwidth': '1 Gbps+'
        }
    
    def scenario_insider_threat(self) -> Dict:
        """Simulate insider threat with data theft"""
        logger.info("Simulating insider threat scenario")
        
        return {
            'name': 'Insider Threat - Data Theft',
            'duration': '2 hours',
            'stages': [
                {
                    'stage': 'Privilege Escalation',
                    'attack': self.simulator.simulate('brute_force', 'low'),
                    'duration': '20 minutes'
                },
                {
                    'stage': 'Large File Access',
                    'description': 'Accessing sensitive databases',
                    'duration': '40 minutes'
                },
                {
                    'stage': 'Data Transfer',
                    'attack': self.simulator.simulate('data_exfiltration', 'high'),
                    'duration': '60 minutes'
                }
            ]
        }
