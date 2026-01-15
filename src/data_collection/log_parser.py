"""
Log Parser Module
Parses system and application logs for security analysis
"""

import logging
import re
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class LogParser:
    """
    Parses various system and application logs.
    
    Supports:
    - Windows Event Logs
    - Linux syslog
    - Web server logs (Apache, Nginx)
    - Database logs (MySQL, PostgreSQL)
    - Application logs
    """
    
    def __init__(self):
        """Initialize the LogParser"""
        self.logs = []
        self.parsed_events = []
        
        # Log format patterns
        self.patterns = {
            'windows_event': r'(\d{1,2}/\d{1,2}/\d{4})\s+(\d{1,2}:\d{1,2}:\d{1,2})\s+(\w+)\s+(.*)',
            'syslog': r'(\w+\s+\d+\s+\d{1,2}:\d{1,2}:\d{1,2})\s+(\S+)\s+(\S+)\[(\d+)\]:\s+(.*)',
            'apache_access': r'(\S+)\s+\S+\s+\S+\s+\[([^\]]+)\]\s+"(\w+)\s+(\S+)\s+\S+"\s+(\d+)\s+(\d+)',
            'failed_login': r'(failed|invalid|incorrect|unauthorized|denied)',
            'port_scan': r'(syn|scan|probe)',
            'suspicious_command': r'(rm\s+-rf|mkfs|dd\s+if|wget|curl|chmod|sudo)',
        }
        
        logger.info("LogParser initialized")
    
    def parse_file(self, filepath: str, log_type: str = 'generic') -> List[Dict]:
        """
        Parse a log file.
        
        Args:
            filepath: Path to log file
            log_type: Type of log ('windows_event', 'syslog', 'apache', 'generic')
            
        Returns:
            List of parsed log events
        """
        logger.info(f"Parsing log file: {filepath} (type={log_type})")
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            
            parsed = []
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                event = self._parse_line(line, log_type)
                if event:
                    parsed.append(event)
                    self.parsed_events.append(event)
            
            logger.info(f"Parsed {len(parsed)} events from {filepath}")
            return parsed
            
        except Exception as e:
            logger.error(f"Error parsing log file: {e}")
            return []
    
    def parse_lines(self, lines: List[str], log_type: str = 'generic') -> List[Dict]:
        """
        Parse a list of log lines.
        
        Args:
            lines: List of log lines
            log_type: Type of log
            
        Returns:
            List of parsed log events
        """
        parsed = []
        
        for line in lines:
            event = self._parse_line(line, log_type)
            if event:
                parsed.append(event)
                self.parsed_events.append(event)
        
        logger.info(f"Parsed {len(parsed)} events")
        return parsed
    
    def _parse_line(self, line: str, log_type: str) -> Optional[Dict]:
        """
        Parse a single log line.
        
        Args:
            line: Log line to parse
            log_type: Type of log
            
        Returns:
            Parsed event dictionary or None
        """
        event = {
            'raw': line,
            'timestamp': datetime.now().isoformat(),
            'log_type': log_type,
            'severity': 'INFO',
            'source': 'unknown',
            'message': line,
            'indicators': []
        }
        
        # Parse based on log type
        if log_type == 'windows_event':
            match = re.search(self.patterns['windows_event'], line)
            if match:
                event['timestamp'] = match.group(1) + ' ' + match.group(2)
                event['severity'] = match.group(3)
                event['message'] = match.group(4)
        
        elif log_type == 'syslog':
            match = re.search(self.patterns['syslog'], line)
            if match:
                event['timestamp'] = match.group(1)
                event['source'] = match.group(2)
                event['process'] = match.group(3)
                event['pid'] = match.group(4)
                event['message'] = match.group(5)
        
        elif log_type == 'apache':
            match = re.search(self.patterns['apache_access'], line)
            if match:
                event['source'] = match.group(1)
                event['http_method'] = match.group(3)
                event['request_uri'] = match.group(4)
                event['http_status'] = match.group(5)
                event['response_size'] = match.group(6)
        
        # Detect security indicators
        event['indicators'] = self._detect_indicators(event['message'])
        
        # Determine severity based on indicators
        if event['indicators']:
            if any(indicator in ['critical', 'attack', 'breach'] for indicator in event['indicators']):
                event['severity'] = 'CRITICAL'
            elif any(indicator in ['suspicious', 'warning'] for indicator in event['indicators']):
                event['severity'] = 'WARNING'
        
        return event
    
    def _detect_indicators(self, message: str) -> List[str]:
        """
        Detect security indicators in log message.
        
        Args:
            message: Log message text
            
        Returns:
            List of detected indicators
        """
        indicators = []
        message_lower = message.lower()
        
        # Check for failed login attempts
        if re.search(self.patterns['failed_login'], message_lower):
            indicators.append('failed_login')
        
        # Check for port scanning
        if re.search(self.patterns['port_scan'], message_lower):
            indicators.append('port_scan')
        
        # Check for suspicious commands
        if re.search(self.patterns['suspicious_command'], message_lower):
            indicators.append('suspicious_command')
        
        # Check for SQL injection patterns
        if re.search(r"(union|select|insert|update|delete|drop|exec|script|<|>|'|--).*", message_lower):
            indicators.append('sql_injection_attempt')
        
        # Check for privilege escalation
        if 'sudo' in message_lower or 'root' in message_lower:
            indicators.append('privilege_escalation')
        
        # Check for file access violations
        if 'permission denied' in message_lower or 'access denied' in message_lower:
            indicators.append('access_violation')
        
        return indicators
    
    def get_events_by_severity(self, severity: str) -> List[Dict]:
        """
        Get all events with specific severity.
        
        Args:
            severity: Severity level (INFO, WARNING, CRITICAL)
            
        Returns:
            List of events with specified severity
        """
        return [e for e in self.parsed_events if e['severity'] == severity]
    
    def get_suspicious_events(self) -> List[Dict]:
        """
        Get events that indicate suspicious activity.
        
        Returns:
            List of suspicious events
        """
        suspicious = []
        for event in self.parsed_events:
            if event['indicators']:
                suspicious.append(event)
        return suspicious
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about parsed logs.
        
        Returns:
            Dictionary with log statistics
        """
        if not self.parsed_events:
            return {'total_events': 0, 'message': 'No events parsed'}
        
        severities = {}
        indicators_count = {}
        sources = set()
        
        for event in self.parsed_events:
            severity = event.get('severity', 'UNKNOWN')
            severities[severity] = severities.get(severity, 0) + 1
            
            for indicator in event.get('indicators', []):
                indicators_count[indicator] = indicators_count.get(indicator, 0) + 1
            
            if event.get('source'):
                sources.add(event['source'])
        
        return {
            'total_events': len(self.parsed_events),
            'severity_distribution': severities,
            'indicator_counts': indicators_count,
            'unique_sources': len(sources),
            'suspicious_events': len(self.get_suspicious_events()),
            'critical_events': len(self.get_events_by_severity('CRITICAL'))
        }
    
    def clear_logs(self) -> None:
        """Clear parsed logs"""
        self.parsed_events = []
        logger.info("Parsed logs cleared")
