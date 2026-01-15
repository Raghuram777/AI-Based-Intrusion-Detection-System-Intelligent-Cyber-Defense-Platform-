"""
Main Entry Point for AI-Powered Intrusion Detection System

This is the main application that orchestrates all components:
- Data collection (packet capture, log parsing)
- Feature extraction
- Anomaly detection
- Alert generation
- Database storage
"""

import logging
import sys
import os
from datetime import datetime
import time

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from data_collection import PacketSniffer, LogParser
from feature_extraction import FeatureExtractor
from models import AnomalyDetector
from utils import Config, Database
import numpy as np

# Create logs directory
os.makedirs('logs', exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('..', 'logs', 'ids.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AIIntrustionDetectionSystem:
    """
    Main AI-IDS Application
    
    Orchestrates the complete intrusion detection pipeline:
    1. Data Collection: Capture network packets and parse logs
    2. Feature Extraction: Transform raw data into ML features
    3. Anomaly Detection: Use ML models to detect attacks
    4. Alert Management: Generate and store alerts
    5. Feedback Loop: Learn from false positives
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize the AI-IDS system.
        
        Args:
            config_file: Path to configuration file
        """
        logger.info("=" * 70)
        logger.info("INITIALIZING AI-POWERED INTRUSION DETECTION SYSTEM")
        logger.info("=" * 70)
        
        # Load configuration
        self.config = Config(config_file)
        logger.info("Configuration loaded")
        
        # Initialize components
        self.packet_sniffer = PacketSniffer(
            interface=self.config.get('network', 'interface'),
            packet_count=self.config.get('network', 'packet_count')
        )
        
        self.log_parser = LogParser()
        self.feature_extractor = FeatureExtractor(
            window_size=self.config.get('ai_models', 'feature_window_size')
        )
        self.anomaly_detector = AnomalyDetector(
            contamination_ratio=1 - self.config.get('ai_models', 'anomaly_threshold')
        )
        self.database = Database(
            db_path=self.config.get('database', 'path')
        )
        
        self.running = False
        logger.info("AI-IDS System initialized successfully")
    
    def demo_mode(self, duration: int = 60):
        """
        Run in demo mode with mock data (no real network capture required).
        
        Args:
            duration: How long to run in seconds
        """
        logger.info(f"\n{'=' * 70}")
        logger.info("STARTING DEMO MODE (Duration: {} seconds)".format(duration))
        logger.info("=" * 70)
        
        start_time = time.time()
        self.running = True
        
        try:
            # Phase 1: Data Collection
            logger.info("\n[PHASE 1] Capturing network packets...")
            packets = self.packet_sniffer._generate_mock_packets()
            logger.info(f"✓ Captured {len(packets)} packets")
            
            # Display packet statistics
            stats = self.packet_sniffer.get_statistics()
            logger.info("Packet Statistics:")
            logger.info(f"  - Protocols: {stats['protocols']}")
            logger.info(f"  - Total Size: {stats['total_bytes']} bytes")
            logger.info(f"  - Unique Source IPs: {stats['unique_source_ips']}")
            logger.info(f"  - Unique Dest IPs: {stats['unique_dest_ips']}")
            
            # Phase 2: Parse Logs (simulated)
            logger.info("\n[PHASE 2] Parsing system logs...")
            sample_logs = [
                "Failed password for user admin from 192.168.1.100",
                "Port scan detected from 10.0.0.5",
                "Successful login for user admin",
                "SQL injection attempt detected in HTTP request",
                "Privilege escalation attempt by user testuser",
                "Unusual outbound traffic detected",
                "Too many connection attempts",
            ]
            events = self.log_parser.parse_lines(sample_logs, 'generic')
            logger.info(f"✓ Parsed {len(events)} log events")
            
            # Display log statistics
            log_stats = self.log_parser.get_statistics()
            logger.info("Log Statistics:")
            logger.info(f"  - Critical Events: {log_stats['critical_events']}")
            logger.info(f"  - Suspicious Events: {log_stats['suspicious_events']}")
            logger.info(f"  - Indicator Counts: {log_stats['indicator_counts']}")
            
            # Phase 3: Feature Extraction
            logger.info("\n[PHASE 3] Extracting features from data...")
            packet_features = self.feature_extractor.extract_packet_features(packets)
            log_features = self.feature_extractor.extract_log_features(events)
            logger.info("✓ Features extracted successfully")
            
            logger.info("Top 10 Packet Features:")
            for i, (key, value) in enumerate(sorted(packet_features.items(), 
                                                     key=lambda x: x[1], reverse=True)[:10]):
                logger.info(f"  {i+1}. {key}: {value:.4f}")
            
            logger.info("Top 5 Log Features:")
            for i, (key, value) in enumerate(sorted(log_features.items(),
                                                     key=lambda x: x[1], reverse=True)[:5]):
                logger.info(f"  {i+1}. {key}: {value:.4f}")
            
            # Phase 4: Prepare Training Data
            logger.info("\n[PHASE 4] Preparing training data...")
            normal_features_list = []
            
            for _ in range(10):  # Generate multiple samples
                packets_batch = self.packet_sniffer._generate_mock_packets()
                features = self.feature_extractor.extract_packet_features(packets_batch)
                feature_vector = [features.get(name, 0) for name in self.feature_extractor.get_feature_names()[:26]]
                normal_features_list.append(feature_vector)
            
            X_train = np.array(normal_features_list)
            logger.info(f"Training data prepared: shape {X_train.shape}")
            
            # Phase 5: Train Anomaly Detection Models
            logger.info("\n[PHASE 5] Training anomaly detection models...")
            self.anomaly_detector.fit_isolation_forest(X_train)
            self.anomaly_detector.fit_statistical_baseline(X_train)
            logger.info("Models trained successfully")
            
            # Phase 6: Anomaly Detection on Test Data
            logger.info("\n[PHASE 6] Running anomaly detection on captured packets...")
            combined_features = {**packet_features, **log_features}
            X_test_array = np.array([[combined_features.get(name, 0) for name in self.feature_extractor.get_feature_names()[:26]]])
            
            ensemble_scores, method_scores = self.anomaly_detector.ensemble_detection(X_test_array)
            
            logger.info("Anomaly Detection Results:")
            logger.info(f"  - Ensemble Score: {ensemble_scores[0]:.4f}")
            logger.info(f"  - Method Scores: {method_scores}")
            
            severity, label = self.anomaly_detector.classify_anomaly(ensemble_scores[0])
            logger.info(f"  - Classification: {severity} - {label}")
            
            # Phase 7: Generate Alerts
            logger.info("\n[PHASE 7] Generating alerts...")
            if ensemble_scores[0] > self.config.get('ai_models', 'anomaly_threshold'):
                alert_data = {
                    'alert_type': 'ANOMALY_DETECTED',
                    'severity': severity,
                    'confidence': float(ensemble_scores[0]),
                    'source_ip': stats['source_ips'][0] if stats['source_ips'] else 'unknown',
                    'destination_ip': stats['dest_ips'][0] if stats['dest_ips'] else 'unknown',
                    'protocol': list(stats['protocols'].keys())[0] if stats['protocols'] else 'unknown',
                    'description': f'Anomalous network behavior detected. Ensemble anomaly score: {ensemble_scores[0]:.4f}',
                    'indicators': list(log_stats['indicator_counts'].keys()),
                    'recommendation': 'Investigate network activity and review logs for suspicious patterns'
                }
                
                alert_id = self.database.insert_alert(alert_data)
                logger.info(f"✓ Alert generated with ID {alert_id}")
                logger.info(f"  - Severity: {alert_data['severity']}")
                logger.info(f"  - Confidence: {alert_data['confidence']:.4f}")
                logger.info(f"  - Indicators: {', '.join(alert_data['indicators'])}")
            else:
                logger.info("✓ No anomalies detected - traffic appears normal")
            
            # Phase 8: Database Statistics
            logger.info("\n[PHASE 8] Database statistics...")
            db_stats = self.database.get_alert_statistics(hours=1)
            logger.info(f"Alert Statistics (Last Hour):")
            logger.info(f"  - Total Alerts: {db_stats['total_alerts']}")
            logger.info(f"  - Severity Distribution: {db_stats['severity_distribution']}")
            logger.info(f"  - Average Confidence: {db_stats['average_confidence']:.4f}")
            
            logger.info("\n" + "=" * 70)
            logger.info("DEMO MODE COMPLETED SUCCESSFULLY")
            logger.info("=" * 70 + "\n")
            
        except Exception as e:
            logger.error(f"Error in demo mode: {e}", exc_info=True)
        finally:
            self.running = False
    
    def run_capture_mode(self, duration: int = 60):
        """
        Run in real packet capture mode.
        
        Args:
            duration: Duration to capture in seconds
        """
        logger.info("\n" + "=" * 70)
        logger.info("STARTING PACKET CAPTURE MODE")
        logger.info("=" * 70)
        logger.info(f"Capturing packets for {duration} seconds...")
        
        # Note: Real implementation would require network privileges
        # and proper interface configuration
        logger.warning("Real packet capture requires administrative privileges")
        logger.info("Falling back to demo mode for testing...")
        
        self.demo_mode(duration)
    
    def shutdown(self):
        """Gracefully shutdown the system"""
        logger.info("\nShutting down AI-IDS System...")
        self.running = False
        
        # Close database connection
        self.database.close()
        
        logger.info("AI-IDS System shut down successfully")
    
    def __del__(self):
        """Cleanup on object deletion"""
        try:
            self.shutdown()
        except:
            pass


def main():
    """Main entry point"""
    try:
        # Create logs directory
        os.makedirs('logs', exist_ok=True)
        os.makedirs('data', exist_ok=True)
        
        # Initialize system
        ids_system = AIIntrustionDetectionSystem('config/config.json')
        
        # Run in demo mode
        ids_system.demo_mode(duration=60)
        
        # Cleanup
        ids_system.shutdown()
        
        logger.info("\n✅ Application completed successfully")
        return 0
        
    except KeyboardInterrupt:
        logger.info("\nInterrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == '__main__':
    sys.exit(main())
