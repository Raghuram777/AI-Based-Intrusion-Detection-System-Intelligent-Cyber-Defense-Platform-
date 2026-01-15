"""
Multi-Agent System for AI-IDS
Five specialized agents working in coordination for comprehensive security
"""

import logging
from typing import Dict, List, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import json
import numpy as np

logger = logging.getLogger(__name__)


class AgentRole(Enum):
    """Agent role types"""
    MONITORING = "monitoring"
    DETECTION = "detection"
    CLASSIFICATION = "classification"
    EXPLANATION = "explanation"
    RESPONSE = "response"


@dataclass
class Message:
    """Inter-agent message format"""
    sender: str
    recipient: str
    message_type: str
    content: Dict
    timestamp: str
    
    def to_dict(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'type': self.message_type,
            'content': self.content,
            'timestamp': self.timestamp
        }


class SecurityAgent:
    """Base security agent class"""
    
    def __init__(self, agent_id: str, role: AgentRole):
        """
        Initialize a security agent.
        
        Args:
            agent_id: Unique agent identifier
            role: Agent role/responsibility
        """
        self.agent_id = agent_id
        self.role = role
        self.messages = []
        self.knowledge_base = {}
        self.status = "idle"
        
        logger.info(f"Agent {agent_id} ({role.value}) initialized")
    
    def receive_message(self, message: Message) -> None:
        """Receive a message from another agent"""
        self.messages.append(message)
        logger.debug(f"Agent {self.agent_id} received message from {message.sender}")
    
    def send_message(self, recipient: str, message_type: str, content: Dict) -> Message:
        """Send a message to another agent"""
        msg = Message(
            sender=self.agent_id,
            recipient=recipient,
            message_type=message_type,
            content=content,
            timestamp=datetime.now().isoformat()
        )
        logger.debug(f"Agent {self.agent_id} sending {message_type} to {recipient}")
        return msg
    
    def update_knowledge(self, key: str, value) -> None:
        """Update knowledge base"""
        self.knowledge_base[key] = value


class MonitoringAgent(SecurityAgent):
    """
    Monitors network and system activity
    Collects raw data from all sources
    """
    
    def __init__(self):
        super().__init__("monitor-agent", AgentRole.MONITORING)
        self.data_sources = []
        self.collection_rate = 0
    
    def collect_data(self, packets: List[Dict], events: List[Dict]) -> Message:
        """
        Collect data from network and logs.
        
        Args:
            packets: Network packets
            events: Log events
            
        Returns:
            Message for detection agent
        """
        self.status = "collecting"
        
        data_summary = {
            'packet_count': len(packets),
            'event_count': len(events),
            'protocols': {},
            'timestamps': []
        }
        
        # Analyze protocols
        for packet in packets:
            protocol = packet.get('protocol', 'Unknown')
            data_summary['protocols'][protocol] = data_summary['protocols'].get(protocol, 0) + 1
        
        self.status = "idle"
        
        return self.send_message(
            "detect-agent",
            "raw_data",
            {
                'packets': packets,
                'events': events,
                'summary': data_summary
            }
        )


class DetectionAgent(SecurityAgent):
    """
    Detects anomalies in network traffic
    Flags suspicious patterns
    """
    
    def __init__(self):
        super().__init__("detect-agent", AgentRole.DETECTION)
        self.detection_models = []
        self.anomaly_threshold = 0.7
    
    def process_data(self, packets: List[Dict], events: List[Dict], 
                    anomaly_scores: np.ndarray = None) -> Message:
        """
        Process data and detect anomalies.
        
        Args:
            packets: Packet data
            events: Event data
            anomaly_scores: Pre-calculated anomaly scores
            
        Returns:
            Message for classification agent
        """
        import numpy as np
        
        self.status = "detecting"
        
        detections = []
        
        if anomaly_scores is not None:
            for i, score in enumerate(anomaly_scores):
                if score > self.anomaly_threshold:
                    detections.append({
                        'anomaly_score': float(score),
                        'index': i,
                        'severity': 'CRITICAL' if score > 0.9 else 'WARNING'
                    })
        else:
            # Use statistical detection on packet data
            if packets:
                packet_sizes = [p.get('packet_size', 0) for p in packets]
                if packet_sizes:
                    mean_size = np.mean(packet_sizes)
                    std_size = np.std(packet_sizes)
                    
                    for packet in packets:
                        size = packet.get('packet_size', 0)
                        z_score = abs((size - mean_size) / (std_size + 1e-8))
                        if z_score > 3:  # 3-sigma rule
                            detections.append({
                                'anomaly_score': min(1.0, z_score / 5),
                                'packet': packet,
                                'reason': 'Unusual packet size'
                            })
        
        self.status = "idle"
        
        return self.send_message(
            "classify-agent",
            "anomalies_detected",
            {
                'detections': detections,
                'detection_count': len(detections),
                'timestamp': datetime.now().isoformat()
            }
        )


class ClassificationAgent(SecurityAgent):
    """
    Classifies detected anomalies by attack type
    Determines attack severity and confidence
    """
    
    def __init__(self):
        super().__init__("classify-agent", AgentRole.CLASSIFICATION)
        self.attack_types = [
            'Port Scan', 'Brute Force', 'SQL Injection',
            'DoS Attack', 'Data Exfiltration', 'Malware Traffic'
        ]
    
    def classify_attacks(self, detections: List[Dict], 
                        features: Dict = None) -> Message:
        """
        Classify detected anomalies.
        
        Args:
            detections: List of detected anomalies
            features: Feature dictionary
            
        Returns:
            Message for explanation agent
        """
        self.status = "classifying"
        
        classifications = []
        
        for detection in detections:
            # Simple heuristic-based classification
            attack_type = self._classify_single(detection, features)
            
            classifications.append({
                'detection': detection,
                'attack_type': attack_type['type'],
                'confidence': attack_type['confidence'],
                'indicators': attack_type['indicators']
            })
        
        self.status = "idle"
        
        return self.send_message(
            "explain-agent",
            "classifications_ready",
            {
                'classifications': classifications,
                'timestamp': datetime.now().isoformat()
            }
        )
    
    def _classify_single(self, detection: Dict, features: Dict) -> Dict:
        """Classify a single detection"""
        score = detection.get('anomaly_score', 0.5)
        
        # Simple heuristic: vary attack type based on score and patterns
        if score > 0.95:
            return {
                'type': 'DoS Attack',
                'confidence': min(1.0, score * 1.1),
                'indicators': ['high_packet_rate', 'packet_flood']
            }
        elif score > 0.8:
            return {
                'type': 'Port Scan',
                'confidence': score,
                'indicators': ['multiple_ports', 'syn_flood']
            }
        else:
            return {
                'type': 'Anomalous Traffic',
                'confidence': score,
                'indicators': ['unusual_pattern']
            }


class ExplanationAgent(SecurityAgent):
    """
    Provides human-readable explanations for alerts
    Generates insight and context
    """
    
    def __init__(self):
        super().__init__("explain-agent", AgentRole.EXPLANATION)
    
    def generate_explanations(self, classifications: List[Dict]) -> Message:
        """
        Generate explanations for classifications.
        
        Args:
            classifications: List of classifications
            
        Returns:
            Message for response agent
        """
        self.status = "explaining"
        
        explanations = []
        
        for classification in classifications:
            explanation = self._generate_explanation(classification)
            explanations.append(explanation)
        
        self.status = "idle"
        
        return self.send_message(
            "response-agent",
            "explanations_generated",
            {
                'explanations': explanations,
                'timestamp': datetime.now().isoformat()
            }
        )
    
    def _generate_explanation(self, classification: Dict) -> Dict:
        """Generate explanation for single classification"""
        attack_type = classification.get('attack_type', 'Unknown')
        confidence = classification.get('confidence', 0.5)
        indicators = classification.get('indicators', [])
        
        severity = 'CRITICAL' if confidence > 0.9 else 'WARNING' if confidence > 0.7 else 'INFO'
        
        explanation_text = f"Detected {attack_type} attack with {confidence*100:.1f}% confidence.\n"
        explanation_text += f"Indicators: {', '.join(indicators)}\n"
        
        if confidence > 0.9:
            explanation_text += "This is a critical threat requiring immediate action."
        elif confidence > 0.7:
            explanation_text += "Recommend immediate investigation and monitoring."
        
        return {
            'severity': severity,
            'attack_type': attack_type,
            'confidence': confidence,
            'explanation': explanation_text,
            'recommendations': self._get_recommendations(attack_type)
        }
    
    def _get_recommendations(self, attack_type: str) -> List[str]:
        """Get recommendations for attack type"""
        recommendations = {
            'Port Scan': [
                'Review firewall rules',
                'Monitor source IP for further activity',
                'Consider implementing port knocking'
            ],
            'Brute Force': [
                'Implement rate limiting',
                'Enforce password policies',
                'Enable MFA on affected accounts'
            ],
            'SQL Injection': [
                'Review application code for input validation',
                'Update database access controls',
                'Implement parameterized queries'
            ],
            'DoS Attack': [
                'Activate DDoS mitigation',
                'Block source IP addresses',
                'Scale infrastructure capacity'
            ],
            'Data Exfiltration': [
                'Block source IP immediately',
                'Review data access logs',
                'Implement data loss prevention'
            ]
        }
        
        return recommendations.get(attack_type, [
            'Investigate further',
            'Collect forensic evidence',
            'Update security policies'
        ])


class ResponseAgent(SecurityAgent):
    """
    Recommends and orchestrates responses to threats
    Coordinates defensive actions
    """
    
    def __init__(self):
        super().__init__("response-agent", AgentRole.RESPONSE)
        self.action_queue = []
    
    def generate_response(self, explanations: List[Dict]) -> Dict:
        """
        Generate response actions based on explanations.
        
        Args:
            explanations: List of explanations from explanation agent
            
        Returns:
            Response action dictionary
        """
        self.status = "responding"
        
        actions = []
        alerts = []
        
        for explanation in explanations:
            severity = explanation.get('severity', 'INFO')
            recommendations = explanation.get('recommendations', [])
            
            action = {
                'timestamp': datetime.now().isoformat(),
                'severity': severity,
                'alert_type': explanation.get('attack_type', 'Unknown'),
                'confidence': explanation.get('confidence', 0),
                'explanation': explanation.get('explanation', ''),
                'recommended_actions': recommendations,
                'automated_actions': self._get_automated_actions(severity)
            }
            
            actions.append(action)
            
            alert_entry = {
                'type': explanation.get('attack_type'),
                'severity': severity,
                'confidence': explanation.get('confidence'),
                'explanation': explanation.get('explanation')
            }
            alerts.append(alert_entry)
        
        self.status = "idle"
        
        return {
            'response_timestamp': datetime.now().isoformat(),
            'total_threats': len(explanations),
            'actions': actions,
            'alerts': alerts,
            'status': 'READY_FOR_EXECUTION'
        }
    
    def _get_automated_actions(self, severity: str) -> List[str]:
        """Get automated response actions"""
        if severity == 'CRITICAL':
            return [
                'Log all activity',
                'Capture network traffic',
                'Alert security team',
                'Prepare isolation commands'
            ]
        elif severity == 'WARNING':
            return [
                'Log activity',
                'Monitor source IP',
                'Alert security team'
            ]
        else:
            return [
                'Log activity',
                'Monitor'
            ]


class MultiAgentSystem:
    """
    Orchestrates communication and coordination between all agents
    """
    
    def __init__(self):
        """Initialize the multi-agent system"""
        self.monitoring_agent = MonitoringAgent()
        self.detection_agent = DetectionAgent()
        self.classification_agent = ClassificationAgent()
        self.explanation_agent = ExplanationAgent()
        self.response_agent = ResponseAgent()
        
        self.agents = [
            self.monitoring_agent,
            self.detection_agent,
            self.classification_agent,
            self.explanation_agent,
            self.response_agent
        ]
        
        self.message_queue = []
        logger.info("MultiAgentSystem initialized with 5 agents")
    
    def process_threat(self, packets: List[Dict], events: List[Dict],
                      anomaly_scores: np.ndarray = None, 
                      features: Dict = None) -> Dict:
        """
        Process a potential threat through the entire agent pipeline.
        
        Args:
            packets: Network packets
            events: Log events
            anomaly_scores: Anomaly detection scores
            features: Feature dictionary
            
        Returns:
            Final response with recommended actions
        """
        logger.info(f"MultiAgentSystem processing {len(packets)} packets, {len(events)} events")
        
        # Step 1: Monitoring Agent collects data
        msg1 = self.monitoring_agent.collect_data(packets, events)
        self.message_queue.append(msg1)
        
        # Step 2: Detection Agent detects anomalies
        msg2 = self.detection_agent.process_data(packets, events, anomaly_scores)
        self.message_queue.append(msg2)
        
        detections = msg2.content.get('detections', [])
        
        if not detections:
            logger.info("No anomalies detected")
            return {
                'status': 'NORMAL',
                'threat_detected': False,
                'message': 'No threats detected'
            }
        
        # Step 3: Classification Agent classifies attacks
        msg3 = self.classification_agent.classify_attacks(detections, features)
        self.message_queue.append(msg3)
        
        classifications = msg3.content.get('classifications', [])
        
        # Step 4: Explanation Agent generates explanations
        msg4 = self.explanation_agent.generate_explanations(classifications)
        self.message_queue.append(msg4)
        
        explanations = msg4.content.get('explanations', [])
        
        # Step 5: Response Agent generates response
        response = self.response_agent.generate_response(explanations)
        
        logger.info(f"Threat processing complete: {response['total_threats']} threats, "
                   f"status: {response['status']}")
        
        return {
            'status': 'THREATS_DETECTED',
            'threat_detected': True,
            'pipeline_messages': len(self.message_queue),
            'agents_involved': len(self.agents),
            'response': response
        }
    
    def get_system_status(self) -> Dict:
        """Get status of all agents"""
        return {
            'timestamp': datetime.now().isoformat(),
            'agents': [
                {'id': agent.agent_id, 'role': agent.role.value, 'status': agent.status}
                for agent in self.agents
            ],
            'messages_processed': len(self.message_queue),
            'system_status': 'OPERATIONAL'
        }


# Import numpy at module level for type hints
import numpy as np
