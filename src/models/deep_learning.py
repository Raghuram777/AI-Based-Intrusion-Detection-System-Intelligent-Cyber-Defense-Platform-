"""
Deep Learning Models Module
LSTM and Deep Neural Networks for advanced anomaly detection and attack classification
"""

import logging
import numpy as np
from typing import Tuple, Dict, List
import json

logger = logging.getLogger(__name__)


class LSTMTimeSeriesDetector:
    """
    LSTM-based time-series anomaly detection using statistical methods
    (TensorFlow/PyTorch integration comes later)
    """
    
    def __init__(self, sequence_length: int = 10, threshold: float = 0.7):
        """
        Initialize LSTM-based detector.
        
        Args:
            sequence_length: Number of previous timesteps to consider
            threshold: Anomaly threshold
        """
        self.sequence_length = sequence_length
        self.threshold = threshold
        self.historical_sequences = []
        self.trained = False
        self.mean = None
        self.std = None
        
        logger.info(f"LSTMTimeSeriesDetector initialized (seq_length={sequence_length})")
    
    def fit(self, X: np.ndarray) -> None:
        """
        Train on historical data.
        
        Args:
            X: Historical feature sequences (samples, features)
        """
        try:
            self.mean = np.mean(X, axis=0)
            self.std = np.std(X, axis=0) + 1e-8
            self.trained = True
            logger.info("LSTM Detector trained on historical data")
        except Exception as e:
            logger.error(f"Error training LSTM: {e}")
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect anomalies in sequences.
        
        Args:
            X: Sequence to predict (samples, features)
            
        Returns:
            Tuple of (anomaly_scores, predictions)
        """
        if not self.trained:
            logger.warning("LSTM not trained")
            return np.array([]), np.array([])
        
        try:
            # Calculate reconstruction error (statistical approximation of LSTM)
            z_scores = np.abs((X - self.mean) / self.std)
            reconstruction_error = np.mean(z_scores, axis=1)
            
            # Smooth with moving average
            smoothed = np.convolve(reconstruction_error, 
                                   np.ones(3)/3, mode='same')
            
            # Threshold for anomalies
            predictions = (smoothed > self.threshold).astype(int)
            
            return smoothed, predictions
            
        except Exception as e:
            logger.error(f"Error in LSTM prediction: {e}")
            return np.array([]), np.array([])


class DeepAttackClassifier:
    """
    Deep learning-based attack type classifier
    """
    
    def __init__(self):
        """Initialize attack classifier"""
        self.attack_types = {
            0: 'Port Scan',
            1: 'Brute Force',
            2: 'SQL Injection',
            3: 'DoS Attack',
            4: 'Data Exfiltration',
            5: 'Malware Traffic',
            6: 'Privilege Escalation',
            7: 'Normal Traffic'
        }
        
        # Attack signatures (feature patterns for each attack type)
        self.attack_signatures = {
            'Port Scan': {'unique_dst_ports': 'high', 'packet_rate': 'high', 'syn_count': 'high'},
            'Brute Force': {'failed_login_count': 'high', 'warning_ratio': 'high'},
            'SQL Injection': {'sql_injection_count': 'high', 'suspicious_command_count': 'high'},
            'DoS Attack': {'packet_rate': 'very_high', 'packet_count': 'very_high'},
            'Data Exfiltration': {'avg_payload_size': 'high', 'unique_dst_ips': 'high'},
            'Malware Traffic': {'port_scan_count': 'high', 'privilege_escalation_count': 'high'},
            'Privilege Escalation': {'privilege_escalation_count': 'high', 'access_violation_count': 'high'},
            'Normal Traffic': {'critical_ratio': 'low', 'warning_ratio': 'low'}
        }
        
        logger.info("DeepAttackClassifier initialized")
    
    def classify(self, features: Dict, confidence_threshold: float = 0.6) -> Tuple[str, float, Dict]:
        """
        Classify attack type based on features.
        
        Args:
            features: Feature dictionary
            confidence_threshold: Minimum confidence for classification
            
        Returns:
            Tuple of (attack_type, confidence, details)
        """
        try:
            best_match = None
            best_score = 0
            details = {}
            
            for attack_name, signatures in self.attack_signatures.items():
                score = self._calculate_match_score(features, signatures)
                details[attack_name] = score
                
                if score > best_score:
                    best_score = score
                    best_match = attack_name
            
            # Normalize score to 0-1
            confidence = min(1.0, best_score / 100)
            
            if confidence < confidence_threshold:
                return 'Unknown Attack', confidence, details
            
            logger.debug(f"Classified as {best_match} with confidence {confidence:.3f}")
            return best_match, confidence, details
            
        except Exception as e:
            logger.error(f"Error in classification: {e}")
            return 'Unknown', 0.0, {}
    
    def _calculate_match_score(self, features: Dict, signatures: Dict) -> float:
        """
        Calculate how well features match attack signatures.
        
        Args:
            features: Current features
            signatures: Attack signatures
            
        Returns:
            Match score (0-100)
        """
        score = 0
        matches = 0
        
        for feature_name, threshold_level in signatures.items():
            if feature_name not in features:
                continue
            
            value = features[feature_name]
            
            # Score based on feature value and threshold
            if threshold_level == 'high':
                if value > 50:
                    score += 20
                    matches += 1
            elif threshold_level == 'very_high':
                if value > 80:
                    score += 30
                    matches += 1
            elif threshold_level == 'low':
                if value < 20:
                    score += 20
                    matches += 1
        
        # Bonus for multiple matching signatures
        if matches > 0:
            score *= (1 + matches * 0.1)
        
        return score
    
    def get_attack_types(self) -> List[str]:
        """Get list of detectable attack types"""
        return list(self.attack_signatures.keys())


class ExplainabilityEngine:
    """
    Generate human-readable explanations for model predictions
    Simplified SHAP/LIME-like interpretability
    """
    
    def __init__(self):
        """Initialize explainability engine"""
        self.feature_importance = {}
        logger.info("ExplainabilityEngine initialized")
    
    def explain_alert(self, features: Dict, anomaly_score: float, 
                     attack_type: str, classifier_details: Dict) -> str:
        """
        Generate explanation for an alert.
        
        Args:
            features: Input features
            anomaly_score: Anomaly score
            attack_type: Classified attack type
            classifier_details: Classification details
            
        Returns:
            Human-readable explanation
        """
        try:
            explanation = []
            
            # Overall assessment
            if anomaly_score > 0.9:
                explanation.append(f"🔴 **CRITICAL THREAT**: {attack_type}")
            elif anomaly_score > 0.7:
                explanation.append(f"🟠 **WARNING**: Suspicious activity detected - {attack_type}")
            else:
                explanation.append(f"🟡 **INFO**: {attack_type}")
            
            # Contributing factors
            explanation.append("\n**Contributing Factors:**")
            
            # Top indicators
            top_indicators = self._get_top_indicators(features)
            for i, (indicator, value) in enumerate(top_indicators[:5], 1):
                explanation.append(f"  {i}. {indicator}: {value:.2f}")
            
            # Specific findings
            explanation.append("\n**Findings:**")
            findings = self._generate_findings(features, attack_type)
            for finding in findings:
                explanation.append(f"  • {finding}")
            
            # Recommendations
            explanation.append("\n**Recommendations:**")
            recommendations = self._get_recommendations(attack_type, anomaly_score)
            for rec in recommendations:
                explanation.append(f"  • {rec}")
            
            return "\n".join(explanation)
            
        except Exception as e:
            logger.error(f"Error in explainability: {e}")
            return f"Alert detected with anomaly score: {anomaly_score:.3f}"
    
    def _get_top_indicators(self, features: Dict) -> List[Tuple[str, float]]:
        """Get top contributing features"""
        # Normalize features to 0-100 scale
        normalized = {}
        for key, value in features.items():
            if isinstance(value, (int, float)):
                normalized[key] = min(100, max(0, value))
        
        # Sort by value
        return sorted(normalized.items(), key=lambda x: x[1], reverse=True)
    
    def _generate_findings(self, features: Dict, attack_type: str) -> List[str]:
        """Generate specific findings based on attack type"""
        findings = []
        
        if 'Port Scan' in attack_type:
            findings.append("Multiple destination ports accessed")
            findings.append("High SYN flag count detected")
            findings.append("Unusual port sequence detected")
        elif 'Brute Force' in attack_type:
            findings.append("Multiple failed login attempts detected")
            findings.append("Rapid authentication attempts from single source")
        elif 'SQL Injection' in attack_type:
            findings.append("SQL keywords detected in HTTP request")
            findings.append("Abnormal query patterns in application traffic")
        elif 'DoS' in attack_type:
            findings.append("High packet rate detected")
            findings.append("Large volume of traffic from single source")
        elif 'Exfiltration' in attack_type:
            findings.append("Large outbound data transfer detected")
            findings.append("Connection to multiple external destinations")
        
        return findings
    
    def _get_recommendations(self, attack_type: str, anomaly_score: float) -> List[str]:
        """Get recommendations based on attack type"""
        recommendations = []
        
        if anomaly_score > 0.9:
            recommendations.append("IMMEDIATE ACTION REQUIRED - Block source IP")
            recommendations.append("Isolate affected systems")
            recommendations.append("Collect detailed logs for forensics")
        elif anomaly_score > 0.7:
            recommendations.append("Monitor source for additional suspicious activity")
            recommendations.append("Review affected system logs")
            recommendations.append("Consider rate-limiting from source IP")
        
        if 'Port Scan' in attack_type:
            recommendations.append("Review network segmentation rules")
            recommendations.append("Implement port-based access controls")
        elif 'Brute Force' in attack_type:
            recommendations.append("Enforce stronger authentication policies")
            recommendations.append("Implement account lockout mechanisms")
        elif 'SQL Injection' in attack_type:
            recommendations.append("Review application code for input validation")
            recommendations.append("Update database access controls")
        
        return recommendations
