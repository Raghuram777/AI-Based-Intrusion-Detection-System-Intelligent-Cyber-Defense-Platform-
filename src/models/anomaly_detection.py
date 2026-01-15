"""
Anomaly Detection Module
Implements multiple anomaly detection algorithms
"""

import logging
import numpy as np
from typing import List, Tuple, Dict
from datetime import datetime

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    Multiple anomaly detection algorithms for network traffic analysis.
    
    Algorithms:
    - Isolation Forest (unsupervised)
    - Statistical methods (Z-score, MAD)
    - LSTM (time-series)
    - One-Class SVM
    """
    
    def __init__(self, contamination_ratio: float = 0.1):
        """
        Initialize the AnomalyDetector.
        
        Args:
            contamination_ratio: Expected ratio of anomalies in data
        """
        self.contamination_ratio = contamination_ratio
        self.isolation_forest = None
        self.baseline_stats = {}
        self.trained = False
        
        logger.info(f"AnomalyDetector initialized (contamination={contamination_ratio})")
    
    def fit_isolation_forest(self, X: np.ndarray) -> None:
        """
        Train Isolation Forest model.
        
        Args:
            X: Training data (samples, features)
        """
        try:
            from sklearn.ensemble import IsolationForest
            
            self.isolation_forest = IsolationForest(
                contamination=self.contamination_ratio,
                random_state=42,
                n_estimators=100
            )
            
            self.isolation_forest.fit(X)
            self.trained = True
            logger.info("Isolation Forest trained successfully")
            
        except ImportError:
            logger.warning("scikit-learn not installed. Install with: pip install scikit-learn")
        except Exception as e:
            logger.error(f"Error training Isolation Forest: {e}")
    
    def fit_statistical_baseline(self, X: np.ndarray) -> None:
        """
        Learn statistical baseline from training data.
        
        Args:
            X: Training data (samples, features)
        """
        try:
            self.baseline_stats = {
                'mean': np.mean(X, axis=0),
                'std': np.std(X, axis=0),
                'min': np.min(X, axis=0),
                'max': np.max(X, axis=0),
                'median': np.median(X, axis=0),
                'mad': self._median_absolute_deviation(X)
            }
            logger.info("Statistical baseline calculated")
        except Exception as e:
            logger.error(f"Error calculating baseline: {e}")
    
    def detect_isolation_forest(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Detect anomalies using Isolation Forest.
        
        Args:
            X: Data to predict (samples, features)
            
        Returns:
            Tuple of (predictions, anomaly_scores)
            - predictions: -1 for anomaly, 1 for normal
            - anomaly_scores: float scores (higher = more anomalous)
        """
        if self.isolation_forest is None:
            logger.warning("Isolation Forest not trained")
            return np.array([]), np.array([])
        
        try:
            predictions = self.isolation_forest.predict(X)
            scores = -self.isolation_forest.score_samples(X)  # Negate to get positive anomaly scores
            
            return predictions, scores
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return np.array([]), np.array([])
    
    def detect_statistical(self, X: np.ndarray, z_threshold: float = 3.0) -> np.ndarray:
        """
        Detect anomalies using statistical methods (Z-score).
        
        Args:
            X: Data to analyze (samples, features)
            z_threshold: Z-score threshold for anomaly
            
        Returns:
            Array of anomaly scores
        """
        if not self.baseline_stats:
            logger.warning("Statistical baseline not calculated")
            return np.array([])
        
        try:
            mean = self.baseline_stats['mean']
            std = self.baseline_stats['std']
            
            # Calculate Z-scores
            z_scores = np.abs((X - mean) / (std + 1e-8))
            
            # Maximum Z-score across features for each sample
            anomaly_scores = np.max(z_scores, axis=1)
            
            return anomaly_scores
            
        except Exception as e:
            logger.error(f"Error in statistical detection: {e}")
            return np.array([])
    
    def detect_mad(self, X: np.ndarray, mad_threshold: float = 3.0) -> np.ndarray:
        """
        Detect anomalies using Median Absolute Deviation (MAD).
        
        Args:
            X: Data to analyze
            mad_threshold: MAD threshold multiplier
            
        Returns:
            Array of anomaly scores
        """
        if not self.baseline_stats:
            logger.warning("Statistical baseline not calculated")
            return np.array([])
        
        try:
            median = self.baseline_stats['median']
            mad = self.baseline_stats['mad']
            
            # Calculate MAD scores
            abs_dev = np.abs(X - median)
            mad_scores = abs_dev / (mad + 1e-8)
            
            # Maximum MAD score across features
            anomaly_scores = np.max(mad_scores, axis=1)
            
            return anomaly_scores
            
        except Exception as e:
            logger.error(f"Error in MAD detection: {e}")
            return np.array([])
    
    def ensemble_detection(self, X: np.ndarray, 
                          weights: Dict[str, float] = None) -> Tuple[np.ndarray, Dict]:
        """
        Combine multiple anomaly detection methods.
        
        Args:
            X: Data to analyze
            weights: Weights for each method
            
        Returns:
            Tuple of (ensemble_scores, method_scores_dict)
        """
        if weights is None:
            weights = {
                'isolation_forest': 0.4,
                'statistical': 0.3,
                'mad': 0.3
            }
        
        method_scores = {}
        
        # Isolation Forest
        if self.isolation_forest:
            _, if_scores = self.detect_isolation_forest(X)
            method_scores['isolation_forest'] = np.clip(if_scores / np.max(if_scores + 1e-8), 0, 1)
        
        # Statistical
        stat_scores = self.detect_statistical(X)
        if stat_scores.size > 0:
            method_scores['statistical'] = np.clip(stat_scores / np.max(stat_scores + 1e-8), 0, 1)
        
        # MAD
        mad_scores = self.detect_mad(X)
        if mad_scores.size > 0:
            method_scores['mad'] = np.clip(mad_scores / np.max(mad_scores + 1e-8), 0, 1)
        
        # Ensemble
        ensemble_scores = np.zeros(len(X))
        total_weight = 0
        
        for method, scores in method_scores.items():
            weight = weights.get(method, 0)
            ensemble_scores += weight * scores
            total_weight += weight
        
        if total_weight > 0:
            ensemble_scores /= total_weight
        
        return ensemble_scores, method_scores
    
    def _median_absolute_deviation(self, X: np.ndarray) -> np.ndarray:
        """Calculate median absolute deviation"""
        median = np.median(X, axis=0)
        abs_dev = np.abs(X - median)
        return np.median(abs_dev, axis=0)
    
    def get_anomaly_threshold(self) -> float:
        """
        Get recommended anomaly threshold.
        
        Returns:
            Anomaly threshold value
        """
        return 1.0 - self.contamination_ratio
    
    def classify_anomaly(self, anomaly_score: float, 
                        critical_threshold: float = 0.9,
                        warning_threshold: float = 0.7) -> Tuple[str, str]:
        """
        Classify anomaly severity based on score.
        
        Args:
            anomaly_score: Anomaly score (0-1)
            critical_threshold: Score for critical severity
            warning_threshold: Score for warning severity
            
        Returns:
            Tuple of (severity, label)
        """
        if anomaly_score >= critical_threshold:
            return 'CRITICAL', f'Critical anomaly detected (score: {anomaly_score:.3f})'
        elif anomaly_score >= warning_threshold:
            return 'WARNING', f'Suspicious behavior detected (score: {anomaly_score:.3f})'
        else:
            return 'NORMAL', f'Normal behavior (score: {anomaly_score:.3f})'
