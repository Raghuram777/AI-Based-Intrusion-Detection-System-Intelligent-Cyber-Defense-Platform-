"""
Feature Extractor Module
Extracts security-relevant features from network packets and logs
"""

import logging
from typing import List, Dict, Tuple
import numpy as np
from collections import defaultdict, Counter
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """
    Extracts security-relevant features from packets and logs.
    
    Features Extracted:
    - Network-based: packet sizes, protocols, port patterns, IP patterns
    - Temporal: connection frequency, timing patterns
    - Behavioral: user actions, command patterns
    - Statistical: distribution analysis, anomaly scores
    """
    
    def __init__(self, window_size: int = 100):
        """
        Initialize the FeatureExtractor.
        
        Args:
            window_size: Number of recent packets/events to analyze
        """
        self.window_size = window_size
        self.packet_history = []
        self.log_history = []
        
        logger.info(f"FeatureExtractor initialized (window_size={window_size})")
    
    def extract_packet_features(self, packets: List[Dict]) -> Dict[str, float]:
        """
        Extract features from network packets.
        
        Args:
            packets: List of packet dictionaries
            
        Returns:
            Dictionary of extracted features
        """
        if not packets:
            return self._get_zero_features()
        
        self.packet_history.extend(packets)
        # Keep only recent packets
        self.packet_history = self.packet_history[-self.window_size:]
        
        features = {}
        
        # Basic statistics
        features['packet_count'] = len(packets)
        features['avg_packet_size'] = np.mean([p['packet_size'] for p in packets])
        features['max_packet_size'] = np.max([p['packet_size'] for p in packets])
        features['min_packet_size'] = np.min([p['packet_size'] for p in packets])
        features['std_packet_size'] = np.std([p['packet_size'] for p in packets])
        
        # Protocol distribution
        protocols = [p['protocol'] for p in packets]
        protocol_counts = Counter(protocols)
        features['tcp_ratio'] = protocol_counts.get('TCP', 0) / len(packets)
        features['udp_ratio'] = protocol_counts.get('UDP', 0) / len(packets)
        features['icmp_ratio'] = protocol_counts.get('ICMP', 0) / len(packets)
        
        # Port analysis
        src_ports = [p['src_port'] for p in packets if isinstance(p['src_port'], int)]
        dst_ports = [p['dst_port'] for p in packets if isinstance(p['dst_port'], int)]
        
        features['unique_src_ports'] = len(set(src_ports))
        features['unique_dst_ports'] = len(set(dst_ports))
        features['avg_src_port'] = np.mean(src_ports) if src_ports else 0
        features['avg_dst_port'] = np.mean(dst_ports) if dst_ports else 0
        
        # IP analysis
        src_ips = [p['src_ip'] for p in packets if p['src_ip'] != 'N/A']
        dst_ips = [p['dst_ip'] for p in packets if p['dst_ip'] != 'N/A']
        
        features['unique_src_ips'] = len(set(src_ips))
        features['unique_dst_ips'] = len(set(dst_ips))
        
        # Flag analysis (for TCP packets)
        tcp_packets = [p for p in packets if p['protocol'] == 'TCP']
        if tcp_packets:
            syn_count = sum(1 for p in tcp_packets if 'SYN' in p.get('flags', []))
            ack_count = sum(1 for p in tcp_packets if 'ACK' in p.get('flags', []))
            rst_count = sum(1 for p in tcp_packets if 'RST' in p.get('flags', []))
            fin_count = sum(1 for p in tcp_packets if 'FIN' in p.get('flags', []))
            
            features['syn_count'] = syn_count
            features['ack_count'] = ack_count
            features['rst_count'] = rst_count
            features['fin_count'] = fin_count
            features['syn_ack_ratio'] = syn_count / (ack_count + 1)  # +1 to avoid division by zero
            features['rst_fin_ratio'] = (rst_count + fin_count) / (len(tcp_packets) + 1)
        
        # TTL analysis
        ttls = [p['ttl'] for p in packets if p['ttl'] > 0]
        if ttls:
            features['avg_ttl'] = np.mean(ttls)
            features['ttl_variance'] = np.std(ttls)
            features['ttl_anomaly'] = len([t for t in ttls if t < 32 or t > 255]) / len(ttls)
        
        # Temporal features
        features['packet_rate'] = len(packets) / max(1, self.window_size)  # packets per unit time
        
        # Payload size distribution
        payload_sizes = [p['payload_size'] for p in packets if isinstance(p['payload_size'], int)]
        if payload_sizes:
            features['avg_payload_size'] = np.mean(payload_sizes)
            features['zero_payload_ratio'] = sum(1 for p in payload_sizes if p == 0) / len(payload_sizes)
        
        logger.debug(f"Extracted {len(features)} packet features")
        return features
    
    def extract_log_features(self, events: List[Dict]) -> Dict[str, float]:
        """
        Extract features from log events.
        
        Args:
            events: List of log event dictionaries
            
        Returns:
            Dictionary of extracted features
        """
        if not events:
            return self._get_zero_log_features()
        
        self.log_history.extend(events)
        self.log_history = self.log_history[-self.window_size:]
        
        features = {}
        
        # Event counts
        features['total_events'] = len(events)
        
        # Severity distribution
        severity_counts = Counter([e.get('severity', 'UNKNOWN') for e in events])
        features['critical_events'] = severity_counts.get('CRITICAL', 0)
        features['warning_events'] = severity_counts.get('WARNING', 0)
        features['info_events'] = severity_counts.get('INFO', 0)
        features['critical_ratio'] = features['critical_events'] / len(events)
        features['warning_ratio'] = features['warning_events'] / len(events)
        
        # Indicator detection
        all_indicators = []
        for event in events:
            all_indicators.extend(event.get('indicators', []))
        
        indicator_counts = Counter(all_indicators)
        features['failed_login_count'] = indicator_counts.get('failed_login', 0)
        features['port_scan_count'] = indicator_counts.get('port_scan', 0)
        features['suspicious_command_count'] = indicator_counts.get('suspicious_command', 0)
        features['sql_injection_count'] = indicator_counts.get('sql_injection_attempt', 0)
        features['privilege_escalation_count'] = indicator_counts.get('privilege_escalation', 0)
        features['access_violation_count'] = indicator_counts.get('access_violation', 0)
        features['total_suspicious_indicators'] = len(all_indicators)
        
        # Source diversity
        sources = [e.get('source', 'unknown') for e in events]
        features['unique_sources'] = len(set(sources))
        
        # Temporal concentration
        if events:
            # Check if events are clustered in time
            features['event_concentration'] = len(events) / max(1, features['unique_sources'])
        
        logger.debug(f"Extracted {len(features)} log features")
        return features
    
    def create_feature_vector(self, packets: List[Dict] = None, 
                             events: List[Dict] = None) -> np.ndarray:
        """
        Create a normalized feature vector for ML model input.
        
        Args:
            packets: List of packet dictionaries
            events: List of log event dictionaries
            
        Returns:
            Normalized feature vector as numpy array
        """
        features = {}
        
        # Extract packet features
        if packets:
            packet_features = self.extract_packet_features(packets)
            features.update(packet_features)
        
        # Extract log features
        if events:
            log_features = self.extract_log_features(events)
            features.update(log_features)
        
        # Convert to ordered list of values
        feature_vector = np.array(list(features.values()), dtype=np.float32)
        
        # Normalize features (0-1 range)
        normalized = self._normalize_features(feature_vector)
        
        logger.debug(f"Created feature vector with {len(normalized)} dimensions")
        return normalized
    
    def _normalize_features(self, features: np.ndarray) -> np.ndarray:
        """
        Normalize feature vector to 0-1 range.
        
        Args:
            features: Raw feature vector
            
        Returns:
            Normalized feature vector
        """
        # Replace inf and nan values
        features = np.nan_to_num(features, nan=0.0, posinf=1.0, neginf=0.0)
        
        # Min-Max normalization per feature
        min_val = np.min(features)
        max_val = np.max(features)
        
        if max_val - min_val == 0:
            return np.zeros_like(features)
        
        normalized = (features - min_val) / (max_val - min_val)
        return np.clip(normalized, 0, 1)
    
    def detect_baseline_anomaly(self, current_features: Dict) -> float:
        """
        Detect anomalies by comparing to baseline.
        
        Args:
            current_features: Current feature dictionary
            
        Returns:
            Anomaly score (0-1, higher = more anomalous)
        """
        if len(self.packet_history) < self.window_size // 2:
            return 0.0  # Not enough history for comparison
        
        # Calculate baseline from historical data
        historical_features = self.extract_packet_features(self.packet_history[:-1])
        
        # Compare current to baseline
        differences = []
        for key in current_features:
            if key in historical_features and isinstance(current_features[key], (int, float)):
                # Calculate percentage difference
                baseline = historical_features[key]
                current = current_features[key]
                
                if baseline != 0:
                    diff = abs(current - baseline) / (abs(baseline) + 1)
                    differences.append(diff)
        
        if not differences:
            return 0.0
        
        # Calculate average difference as anomaly score
        anomaly_score = np.mean(differences)
        return min(1.0, anomaly_score)
    
    def get_feature_names(self) -> List[str]:
        """Get list of feature names"""
        return [
            'packet_count', 'avg_packet_size', 'max_packet_size', 'min_packet_size',
            'std_packet_size', 'tcp_ratio', 'udp_ratio', 'icmp_ratio',
            'unique_src_ports', 'unique_dst_ports', 'avg_src_port', 'avg_dst_port',
            'unique_src_ips', 'unique_dst_ips', 'syn_count', 'ack_count',
            'rst_count', 'fin_count', 'syn_ack_ratio', 'rst_fin_ratio',
            'avg_ttl', 'ttl_variance', 'ttl_anomaly', 'packet_rate',
            'avg_payload_size', 'zero_payload_ratio',
            'total_events', 'critical_events', 'warning_events', 'info_events',
            'critical_ratio', 'warning_ratio', 'failed_login_count', 'port_scan_count',
            'suspicious_command_count', 'sql_injection_count', 'privilege_escalation_count',
            'access_violation_count', 'total_suspicious_indicators', 'unique_sources',
            'event_concentration'
        ]
    
    def _get_zero_features(self) -> Dict[str, float]:
        """Get zero-initialized feature dict for empty packets"""
        return {
            'packet_count': 0, 'avg_packet_size': 0, 'max_packet_size': 0,
            'min_packet_size': 0, 'std_packet_size': 0, 'tcp_ratio': 0,
            'udp_ratio': 0, 'icmp_ratio': 0, 'unique_src_ports': 0,
            'unique_dst_ports': 0, 'avg_src_port': 0, 'avg_dst_port': 0,
            'unique_src_ips': 0, 'unique_dst_ips': 0, 'syn_count': 0,
            'ack_count': 0, 'rst_count': 0, 'fin_count': 0, 'syn_ack_ratio': 0,
            'rst_fin_ratio': 0, 'avg_ttl': 0, 'ttl_variance': 0, 'ttl_anomaly': 0,
            'packet_rate': 0, 'avg_payload_size': 0, 'zero_payload_ratio': 0
        }
    
    def _get_zero_log_features(self) -> Dict[str, float]:
        """Get zero-initialized feature dict for empty events"""
        return {
            'total_events': 0, 'critical_events': 0, 'warning_events': 0,
            'info_events': 0, 'critical_ratio': 0, 'warning_ratio': 0,
            'failed_login_count': 0, 'port_scan_count': 0,
            'suspicious_command_count': 0, 'sql_injection_count': 0,
            'privilege_escalation_count': 0, 'access_violation_count': 0,
            'total_suspicious_indicators': 0, 'unique_sources': 0,
            'event_concentration': 0
        }
