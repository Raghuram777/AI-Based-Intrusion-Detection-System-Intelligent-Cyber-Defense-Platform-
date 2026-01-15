"""
Packet Sniffer Module
Captures network packets using Scapy for analysis
"""

import logging
from typing import List, Dict, Callable, Optional
from datetime import datetime
import json

logger = logging.getLogger(__name__)


class PacketSniffer:
    """
    Captures and processes network packets in real-time.
    
    Features:
    - Capture packets from specified network interface
    - Filter packets by protocol, IP address, port
    - Extract relevant security features
    - Store packet data for analysis
    """
    
    def __init__(self, interface: Optional[str] = None, packet_count: int = 100):
        """
        Initialize the PacketSniffer.
        
        Args:
            interface: Network interface to sniff on (None = auto-detect)
            packet_count: Number of packets to capture (0 = unlimited)
        """
        self.interface = interface
        self.packet_count = packet_count
        self.packets_captured = []
        self.packet_callbacks = []
        self.filters = {}
        self.is_running = False
        
        logger.info(f"PacketSniffer initialized on interface: {interface}")
    
    def add_packet_callback(self, callback: Callable) -> None:
        """
        Register a callback function to be called for each packet.
        
        Args:
            callback: Function that takes a packet dict as argument
        """
        self.packet_callbacks.append(callback)
        logger.info(f"Packet callback registered: {callback.__name__}")
    
    def set_filter(self, filter_type: str, value: str) -> None:
        """
        Set filter for packet capture.
        
        Args:
            filter_type: Type of filter ('protocol', 'src_ip', 'dst_ip', 'port')
            value: Filter value
        """
        self.filters[filter_type] = value
        logger.info(f"Filter set: {filter_type}={value}")
    
    def start_capture(self) -> List[Dict]:
        """
        Start capturing packets from the network interface.
        
        Returns:
            List of captured packet dictionaries
        """
        logger.info(f"Starting packet capture (count={self.packet_count})")
        self.is_running = True
        
        try:
            # Try to import Scapy (optional dependency)
            from scapy.all import sniff, IP, TCP, UDP, ICMP
            
            def packet_callback(packet):
                """Process each captured packet"""
                if not self.is_running:
                    return False
                
                packet_data = self._extract_packet_info(packet)
                
                # Apply filters
                if self._passes_filters(packet_data):
                    self.packets_captured.append(packet_data)
                    
                    # Call registered callbacks
                    for callback in self.packet_callbacks:
                        try:
                            callback(packet_data)
                        except Exception as e:
                            logger.error(f"Error in packet callback: {e}")
                    
                    logger.debug(f"Packet captured: {packet_data['src_ip']} -> {packet_data['dst_ip']}")
                
                # Check if we've captured enough packets
                if self.packet_count > 0 and len(self.packets_captured) >= self.packet_count:
                    return False  # Stop sniffing
                
                return True
            
            # Start sniffing
            sniff(
                iface=self.interface,
                prn=packet_callback,
                store=False,
                stop_filter=lambda x: not self.is_running,
                quiet=True
            )
            
            logger.info(f"Packet capture completed. Total packets: {len(self.packets_captured)}")
            return self.packets_captured
            
        except ImportError:
            logger.warning("Scapy not installed. Using mock packet generation.")
            return self._generate_mock_packets()
    
    def stop_capture(self) -> None:
        """Stop packet capture"""
        self.is_running = False
        logger.info("Packet capture stopped")
    
    def _extract_packet_info(self, packet) -> Dict:
        """
        Extract relevant security information from a packet.
        
        Args:
            packet: Scapy packet object
            
        Returns:
            Dictionary with extracted packet information
        """
        from scapy.all import IP, TCP, UDP, ICMP
        
        packet_data = {
            'timestamp': datetime.now().isoformat(),
            'protocol': 'Unknown',
            'src_ip': 'N/A',
            'dst_ip': 'N/A',
            'src_port': 'N/A',
            'dst_port': 'N/A',
            'packet_size': len(packet),
            'payload_size': 0,
            'flags': [],
            'ttl': 0
        }
        
        try:
            # Extract IP layer information
            if IP in packet:
                ip_layer = packet[IP]
                packet_data['src_ip'] = ip_layer.src
                packet_data['dst_ip'] = ip_layer.dst
                packet_data['protocol'] = ip_layer.proto
                packet_data['ttl'] = ip_layer.ttl
            
            # Extract TCP information
            if TCP in packet:
                tcp_layer = packet[TCP]
                packet_data['src_port'] = tcp_layer.sport
                packet_data['dst_port'] = tcp_layer.dport
                packet_data['protocol'] = 'TCP'
                
                # Extract flags
                if tcp_layer.flags.F:
                    packet_data['flags'].append('FIN')
                if tcp_layer.flags.S:
                    packet_data['flags'].append('SYN')
                if tcp_layer.flags.R:
                    packet_data['flags'].append('RST')
                if tcp_layer.flags.A:
                    packet_data['flags'].append('ACK')
            
            # Extract UDP information
            elif UDP in packet:
                udp_layer = packet[UDP]
                packet_data['src_port'] = udp_layer.sport
                packet_data['dst_port'] = udp_layer.dport
                packet_data['protocol'] = 'UDP'
            
            # Extract ICMP information
            elif ICMP in packet:
                packet_data['protocol'] = 'ICMP'
                packet_data['dst_port'] = packet[ICMP].type
        
        except Exception as e:
            logger.debug(f"Error extracting packet info: {e}")
        
        return packet_data
    
    def _passes_filters(self, packet_data: Dict) -> bool:
        """
        Check if packet passes all configured filters.
        
        Args:
            packet_data: Packet information dictionary
            
        Returns:
            True if packet passes filters, False otherwise
        """
        if not self.filters:
            return True
        
        # Check protocol filter
        if 'protocol' in self.filters:
            if packet_data['protocol'] != self.filters['protocol']:
                return False
        
        # Check source IP filter
        if 'src_ip' in self.filters:
            if packet_data['src_ip'] != self.filters['src_ip']:
                return False
        
        # Check destination IP filter
        if 'dst_ip' in self.filters:
            if packet_data['dst_ip'] != self.filters['dst_ip']:
                return False
        
        # Check port filter
        if 'port' in self.filters:
            if packet_data['src_port'] != self.filters['port'] and \
               packet_data['dst_port'] != self.filters['port']:
                return False
        
        return True
    
    def _generate_mock_packets(self) -> List[Dict]:
        """
        Generate mock packets for testing when Scapy is not available.
        
        Returns:
            List of mock packet dictionaries
        """
        logger.info("Generating mock packets for testing...")
        import random
        
        mock_packets = []
        protocols = ['TCP', 'UDP', 'ICMP']
        src_ips = ['192.168.1.100', '192.168.1.101', '192.168.1.102', '10.0.0.5']
        dst_ips = ['8.8.8.8', '1.1.1.1', '208.67.222.222', '192.168.1.1']
        
        for i in range(min(self.packet_count, 100)):
            packet = {
                'timestamp': datetime.now().isoformat(),
                'protocol': random.choice(protocols),
                'src_ip': random.choice(src_ips),
                'dst_ip': random.choice(dst_ips),
                'src_port': random.randint(1024, 65535),
                'dst_port': random.choice([22, 80, 443, 3306, 5432, 27017]),
                'packet_size': random.randint(40, 1500),
                'payload_size': random.randint(0, 1460),
                'flags': random.choice([['SYN'], ['ACK'], ['FIN'], ['RST'], []]),
                'ttl': random.choice([32, 64, 128, 255])
            }
            mock_packets.append(packet)
        
        self.packets_captured = mock_packets
        return mock_packets
    
    def get_captured_packets(self) -> List[Dict]:
        """Get list of captured packets"""
        return self.packets_captured
    
    def clear_packets(self) -> None:
        """Clear captured packets"""
        self.packets_captured = []
        logger.info("Captured packets cleared")
    
    def save_packets_to_json(self, filepath: str) -> None:
        """
        Save captured packets to JSON file.
        
        Args:
            filepath: Path to save JSON file
        """
        try:
            with open(filepath, 'w') as f:
                json.dump(self.packets_captured, f, indent=2)
            logger.info(f"Packets saved to {filepath}")
        except Exception as e:
            logger.error(f"Error saving packets: {e}")
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about captured packets.
        
        Returns:
            Dictionary with packet statistics
        """
        if not self.packets_captured:
            return {'total_packets': 0, 'message': 'No packets captured'}
        
        protocols = {}
        total_size = 0
        src_ips = set()
        dst_ips = set()
        
        for packet in self.packets_captured:
            protocol = packet['protocol']
            protocols[protocol] = protocols.get(protocol, 0) + 1
            total_size += packet['packet_size']
            src_ips.add(packet['src_ip'])
            dst_ips.add(packet['dst_ip'])
        
        return {
            'total_packets': len(self.packets_captured),
            'protocols': protocols,
            'total_bytes': total_size,
            'avg_packet_size': total_size / len(self.packets_captured),
            'unique_source_ips': len(src_ips),
            'unique_dest_ips': len(dst_ips),
            'source_ips': list(src_ips),
            'dest_ips': list(dst_ips)
        }
