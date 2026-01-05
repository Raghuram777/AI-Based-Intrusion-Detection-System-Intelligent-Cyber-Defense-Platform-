"""
AI-Powered IDS Architecture Diagram Generator
Generates all necessary diagrams for the project presentation
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np

# Set style for professional diagrams
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 9
plt.rcParams['font.family'] = 'sans-serif'

def draw_box(ax, xy, width, height, text, color='lightblue', textcolor='black'):
    """Helper function to draw a rounded box with text"""
    box = FancyBboxPatch(xy, width, height, boxstyle="round,pad=0.05", 
                          edgecolor='black', facecolor=color, linewidth=2)
    ax.add_patch(box)
    ax.text(xy[0] + width/2, xy[1] + height/2, text, 
            ha='center', va='center', fontsize=9, weight='bold', color=textcolor)

def draw_arrow(ax, start, end, style='->', color='black', width=2):
    """Helper function to draw an arrow"""
    arrow = FancyArrowPatch(start, end, arrowstyle=style, color=color, 
                           linewidth=width, mutation_scale=20)
    ax.add_patch(arrow)

def generate_system_architecture():
    """Generate Overall System Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(8, 11.5, 'AI-Powered Intrusion Detection System\nOverall Architecture', 
            ha='center', fontsize=16, weight='bold')
    
    # Layer 1: Data Collection Layer
    ax.text(8, 10.5, 'Data Collection Layer', ha='center', fontsize=12, 
            weight='bold', style='italic', color='darkblue')
    draw_box(ax, (0.5, 9.5), 2.5, 0.8, 'Network\nTraffic', '#FFD700')
    draw_box(ax, (3.5, 9.5), 2.5, 0.8, 'System\nLogs', '#FFD700')
    draw_box(ax, (6.5, 9.5), 2.5, 0.8, 'Application\nLogs', '#FFD700')
    draw_box(ax, (9.5, 9.5), 2.5, 0.8, 'User\nBehavior', '#FFD700')
    draw_box(ax, (12.5, 9.5), 2.5, 0.8, 'Packet\nCapture', '#FFD700')
    
    # Layer 2: Data Processing Layer
    ax.text(8, 8.8, 'Data Processing & Normalization Layer', ha='center', 
            fontsize=12, weight='bold', style='italic', color='darkblue')
    draw_box(ax, (2, 7.8), 3, 0.8, 'Stream Processing\nEngine', '#87CEEB')
    draw_box(ax, (6, 7.8), 3, 0.8, 'Data Normalization\n& Enrichment', '#87CEEB')
    draw_box(ax, (10, 7.8), 3, 0.8, 'Feature\nExtraction', '#87CEEB')
    
    # Arrows from collection to processing
    for x in [1.75, 4.75, 7.75, 10.75, 13.75]:
        draw_arrow(ax, (x, 9.4), (7.5, 8.7), '->', 'gray', 1.5)
    
    # Layer 3: AI Intelligence Layer
    ax.text(8, 7.2, 'AI Intelligence & Detection Layer', ha='center', 
            fontsize=12, weight='bold', style='italic', color='darkred')
    
    # Behavioral Baseline Model
    draw_box(ax, (0.5, 5.5), 3, 0.8, 'Behavioral Baseline\nModel', '#98FB98')
    
    # Anomaly Detection
    draw_box(ax, (4, 6.2), 2.5, 0.8, 'Statistical\nAnomaly Detection', '#FF6B6B')
    draw_box(ax, (4, 5.5), 2.5, 0.8, 'ML Clustering\nDetection', '#FF6B6B')
    draw_box(ax, (4, 4.8), 2.5, 0.8, 'Time-Series\nAnalysis', '#FF6B6B')
    
    # Classification Engine
    draw_box(ax, (7, 6.2), 2.5, 0.8, 'Attack Type\nClassifier', '#FFB6C1')
    draw_box(ax, (7, 5.5), 2.5, 0.8, 'Threat Severity\nScoring', '#FFB6C1')
    draw_box(ax, (7, 4.8), 2.5, 0.8, 'Pattern\nMatching', '#FFB6C1')
    
    # Zero-Day Detection
    draw_box(ax, (10, 5.5), 2.5, 0.8, 'Zero-Day Attack\nDetection', '#DDA0DD')
    
    # Explainable AI
    draw_box(ax, (13, 5.5), 2.5, 0.8, 'Explainable AI\nEngine', '#F0E68C')
    
    # Arrows from processing to AI layer
    draw_arrow(ax, (3.5, 7.7), (2, 6.4), '->', 'blue', 1.5)
    draw_arrow(ax, (7.5, 7.7), (5.25, 7.1), '->', 'blue', 1.5)
    draw_arrow(ax, (11.5, 7.7), (11.25, 6.4), '->', 'blue', 1.5)
    
    # Layer 4: Multi-Agent System
    ax.text(8, 4.2, 'Multi-Agent Security System', ha='center', 
            fontsize=12, weight='bold', style='italic', color='darkgreen')
    draw_box(ax, (1, 3.2), 2.2, 0.8, 'Monitoring\nAgent', '#E0FFFF')
    draw_box(ax, (3.7, 3.2), 2.2, 0.8, 'Detection\nAgent', '#E0FFFF')
    draw_box(ax, (6.4, 3.2), 2.2, 0.8, 'Classification\nAgent', '#E0FFFF')
    draw_box(ax, (9.1, 3.2), 2.2, 0.8, 'Explanation\nAgent', '#E0FFFF')
    draw_box(ax, (11.8, 3.2), 2.2, 0.8, 'Response\nAdvisor', '#E0FFFF')
    
    # Arrows connecting agents
    for i in range(4):
        x_start = 2.1 + i * 2.7 + 1.1
        x_end = 2.1 + (i + 1) * 2.7
        draw_arrow(ax, (x_start, 3.6), (x_end, 3.6), '<->', 'darkgreen', 1.5)
    
    # Layer 5: Alert & Response Layer
    ax.text(8, 2.6, 'Alert Management & Response Layer', ha='center', 
            fontsize=12, weight='bold', style='italic', color='darkred')
    draw_box(ax, (2, 1.6), 2.5, 0.8, 'Alert\nCorrelation', '#FFA07A')
    draw_box(ax, (5, 1.6), 2.5, 0.8, 'Smart Priority\nEngine', '#FFA07A')
    draw_box(ax, (8, 1.6), 2.5, 0.8, 'Timeline\nReconstruction', '#FFA07A')
    draw_box(ax, (11, 1.6), 2.5, 0.8, 'Response\nOrchestrator', '#FFA07A')
    
    # Arrows from agents to alert layer
    for x in [2.1, 4.8, 7.5, 10.2, 12.9]:
        draw_arrow(ax, (x, 3.1), (6.5, 2.5), '->', 'darkred', 1.5)
    
    # Layer 6: Feedback & Learning
    ax.text(8, 1.0, 'Self-Learning Feedback Loop', ha='center', 
            fontsize=12, weight='bold', style='italic', color='purple')
    draw_box(ax, (3, 0.1), 3.5, 0.7, 'Admin Feedback\n& False Positive Learning', '#E6E6FA')
    draw_box(ax, (7, 0.1), 3.5, 0.7, 'Model Retraining\n& Baseline Update', '#E6E6FA')
    draw_box(ax, (11, 0.1), 3.5, 0.7, 'Attack Pattern\nDatabase', '#E6E6FA')
    
    # Feedback arrows
    draw_arrow(ax, (4.75, 0.8), (2, 5.4), '->', 'purple', 2, )
    draw_arrow(ax, (8.75, 0.8), (5.25, 4.7), '->', 'purple', 2)
    draw_arrow(ax, (12.75, 0.8), (11.25, 4.7), '->', 'purple', 2)
    
    plt.tight_layout()
    plt.savefig('images/01_system_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: System Architecture Diagram")

def generate_data_flow_diagram():
    """Generate Data Flow Diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'AI-IDS Data Flow Diagram', ha='center', 
            fontsize=16, weight='bold')
    
    # Stage 1: Data Sources
    draw_box(ax, (0.5, 8), 2, 0.8, 'Network\nPackets', '#FFD700')
    draw_box(ax, (3, 8), 2, 0.8, 'System\nLogs', '#FFD700')
    draw_box(ax, (5.5, 8), 2, 0.8, 'Application\nLogs', '#FFD700')
    draw_box(ax, (8, 8), 2, 0.8, 'Firewall\nLogs', '#FFD700')
    draw_box(ax, (10.5, 8), 2, 0.8, 'User Activity\nData', '#FFD700')
    
    # Stage 2: Data Ingestion
    draw_box(ax, (4, 6.8), 5, 0.8, 'Real-Time Data Ingestion Pipeline', '#87CEEB')
    
    # Arrows to ingestion
    for x in [1.5, 4, 6.5, 9, 11.5]:
        draw_arrow(ax, (x, 7.9), (6.5, 7.7), '->', 'blue', 2)
    
    # Stage 3: Preprocessing
    draw_box(ax, (1, 5.6), 3, 0.8, 'Data Cleaning &\nNormalization', '#ADD8E6')
    draw_box(ax, (5, 5.6), 3, 0.8, 'Feature\nEngineering', '#ADD8E6')
    draw_box(ax, (9, 5.6), 3, 0.8, 'Data\nEnrichment', '#ADD8E6')
    
    # Arrow from ingestion to preprocessing
    draw_arrow(ax, (6.5, 6.7), (6.5, 6.5), '->', 'blue', 2)
    
    # Stage 4: Baseline & Detection
    draw_box(ax, (0.5, 4.2), 2.5, 0.8, 'Baseline\nProfiling', '#98FB98')
    draw_box(ax, (3.5, 4.2), 2.5, 0.8, 'Anomaly\nDetection', '#FF6B6B')
    draw_box(ax, (6.5, 4.2), 2.5, 0.8, 'Pattern\nMatching', '#FF6B6B')
    draw_box(ax, (9.5, 4.2), 2.5, 0.8, 'Zero-Day\nDetection', '#DDA0DD')
    
    # Arrows from preprocessing to detection
    draw_arrow(ax, (2.5, 5.5), (1.75, 5.1), '->', 'green', 1.5)
    draw_arrow(ax, (6.5, 5.5), (5, 5.1), '->', 'green', 1.5)
    draw_arrow(ax, (10.5, 5.5), (10.75, 5.1), '->', 'green', 1.5)
    
    # Stage 5: Classification
    draw_box(ax, (2.5, 2.8), 8, 0.8, 'AI-Based Threat Classification & Severity Scoring', '#FFB6C1')
    
    # Arrows from detection to classification
    for x in [1.75, 5, 7.75, 10.75]:
        draw_arrow(ax, (x, 4.1), (6.5, 3.7), '->', 'red', 1.5)
    
    # Stage 6: Explainability
    draw_box(ax, (2.5, 1.6), 8, 0.8, 'Explainable AI - Alert Reasoning & Context', '#F0E68C')
    
    draw_arrow(ax, (6.5, 2.7), (6.5, 2.5), '->', 'orange', 2)
    
    # Stage 7: Alert Output
    draw_box(ax, (1.5, 0.3), 3, 0.8, 'Alert\nDashboard', '#FFA07A')
    draw_box(ax, (5.5, 0.3), 3, 0.8, 'SIEM\nIntegration', '#FFA07A')
    draw_box(ax, (9.5, 0.3), 3, 0.8, 'Response\nActions', '#FFA07A')
    
    # Arrows to outputs
    for x in [3, 7, 11]:
        draw_arrow(ax, (6.5, 1.5), (x, 1.2), '->', 'darkred', 1.5)
    
    # Feedback Loop
    draw_arrow(ax, (1, 0.7), (1, 4.1), '->', 'purple', 2)
    ax.text(0.3, 2.5, 'Feedback\nLoop', fontsize=9, weight='bold', 
            color='purple', rotation=90, va='center')
    
    plt.tight_layout()
    plt.savefig('images/02_data_flow_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Data Flow Diagram")

def generate_ai_pipeline():
    """Generate AI Pipeline Flowchart"""
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(6, 13.5, 'AI Detection & Classification Pipeline', 
            ha='center', fontsize=16, weight='bold')
    
    y = 12.5
    
    # Step 1
    draw_box(ax, (3, y), 6, 0.7, 'Input: Network Traffic & System Logs', '#FFD700')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 2
    draw_box(ax, (3, y), 6, 0.7, 'Feature Extraction', '#87CEEB')
    ax.text(10, y+0.35, 'Extract:\n• Packet size\n• Frequency\n• Protocols\n• Ports', 
            fontsize=8, va='center')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 3
    draw_box(ax, (3, y), 6, 0.7, 'Load Behavioral Baseline Model', '#98FB98')
    ax.text(10, y+0.35, 'Normal:\n• Traffic patterns\n• Login times\n• CPU/Memory', 
            fontsize=8, va='center')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 4
    draw_box(ax, (3, y), 6, 0.7, 'Compare with Baseline', '#ADD8E6')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Decision Diamond
    draw_box(ax, (4, y), 4, 0.7, 'Anomaly\nDetected?', '#FFFF99')
    
    # No path
    draw_arrow(ax, (4, y+0.35), (1.5, y+0.35), '->', 'green', 1.5)
    draw_box(ax, (0.2, y), 1.5, 0.7, 'Continue\nMonitoring', '#90EE90')
    
    # Yes path
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'red', 2)
    ax.text(6.5, y-0.3, 'YES', fontsize=9, weight='bold', color='red')
    y -= 1.2
    
    # Step 5
    draw_box(ax, (2.5, y), 7, 0.7, 'Multi-Model Anomaly Detection', '#FF6B6B')
    draw_box(ax, (0.5, y-1), 2, 0.5, 'Statistical\nAnalysis', '#FFB6C1')
    draw_box(ax, (3, y-1), 2, 0.5, 'ML Clustering\n(Isolation Forest)', '#FFB6C1')
    draw_box(ax, (5.5, y-1), 2, 0.5, 'Time-Series\nLSTM', '#FFB6C1')
    draw_box(ax, (8, y-1), 2, 0.5, 'Rule-Based\nDetection', '#FFB6C1')
    
    draw_arrow(ax, (6, y-0.1), (1.5, y-0.5), '->', 'black', 1)
    draw_arrow(ax, (6, y-0.1), (4, y-0.5), '->', 'black', 1)
    draw_arrow(ax, (6, y-0.1), (6.5, y-0.5), '->', 'black', 1)
    draw_arrow(ax, (6, y-0.1), (9, y-0.5), '->', 'black', 1)
    
    y -= 1.8
    
    # Step 6
    draw_box(ax, (3, y), 6, 0.7, 'Aggregate Detection Scores', '#DDA0DD')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 7
    draw_box(ax, (3, y), 6, 0.7, 'Classify Attack Type', '#FFB6C1')
    ax.text(10, y+0.35, 'Types:\n• DoS/DDoS\n• Brute Force\n• Malware\n• Data Exfil', 
            fontsize=8, va='center')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 8
    draw_box(ax, (3, y), 6, 0.7, 'Calculate Confidence Score', '#F0E68C')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 9
    draw_box(ax, (3, y), 6, 0.7, 'Generate Explainable Alert', '#FFA07A')
    ax.text(10.5, y+0.35, 'Include:\n• Why flagged\n• Features\n• Severity', 
            fontsize=8, va='center')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Step 10
    draw_box(ax, (3, y), 6, 0.7, 'Alert Prioritization & Correlation', '#FF6347')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Final Output
    draw_box(ax, (3, y), 6, 0.7, 'Output: Structured Alert + Timeline', '#00FF00')
    
    # Feedback arrow
    draw_arrow(ax, (9.5, y+0.35), (11, y+0.35), '->', 'purple', 2)
    draw_arrow(ax, (11, y+0.35), (11, 12), '->', 'purple', 2)
    draw_arrow(ax, (11, 12), (9, 11.9), '->', 'purple', 2)
    ax.text(11.5, 8, 'Feedback\nLoop\nfor Model\nRetraining', fontsize=9, 
            weight='bold', color='purple', rotation=90, va='center')
    
    plt.tight_layout()
    plt.savefig('images/03_ai_pipeline_flowchart.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: AI Pipeline Flowchart")

def generate_multi_agent_architecture():
    """Generate Multi-Agent Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Multi-Agent Security Architecture', 
            ha='center', fontsize=16, weight='bold')
    
    # Central Coordinator
    draw_box(ax, (5.5, 7), 3, 1, 'Central Agent\nCoordinator', '#FF6347')
    
    # Agent 1: Monitoring Agent
    draw_box(ax, (1, 7), 2.5, 1, 'Monitoring\nAgent', '#87CEEB')
    ax.text(2.25, 6.2, '• Collect traffic\n• Parse logs\n• Extract features\n• Real-time stream', 
            fontsize=8, ha='center')
    draw_arrow(ax, (3.5, 7.5), (5.5, 7.5), '<->', 'blue', 2)
    
    # Agent 2: Detection Agent
    draw_box(ax, (1, 4.5), 2.5, 1, 'Detection\nAgent', '#FF6B6B')
    ax.text(2.25, 3.7, '• Anomaly detection\n• Pattern matching\n• Baseline comparison\n• Score threats', 
            fontsize=8, ha='center')
    draw_arrow(ax, (2.25, 5.5), (6.5, 6.9), '<->', 'red', 2)
    
    # Agent 3: Classification Agent
    draw_box(ax, (5, 4.5), 2.5, 1, 'Classification\nAgent', '#FFB6C1')
    ax.text(6.25, 3.7, '• Identify attack type\n• Assign severity\n• Confidence scoring\n• Multi-class ML', 
            fontsize=8, ha='center')
    draw_arrow(ax, (6.25, 5.5), (7, 6.9), '<->', 'purple', 2)
    
    # Agent 4: Explanation Agent
    draw_box(ax, (9, 4.5), 2.5, 1, 'Explanation\nAgent', '#F0E68C')
    ax.text(10.25, 3.7, '• Generate reasoning\n• Feature importance\n• Natural language\n• LLM-powered', 
            fontsize=8, ha='center')
    draw_arrow(ax, (10.25, 5.5), (7.5, 6.9), '<->', 'orange', 2)
    
    # Agent 5: Response Advisor Agent
    draw_box(ax, (10.5, 7), 2.5, 1, 'Response\nAdvisor Agent', '#98FB98')
    ax.text(11.75, 6.2, '• Suggest mitigation\n• Auto-response\n• Block/Allow rules\n• Playbook exec', 
            fontsize=8, ha='center')
    draw_arrow(ax, (10.5, 7.5), (8.5, 7.5), '<->', 'green', 2)
    
    # Knowledge Base
    draw_box(ax, (5.5, 2), 3, 0.8, 'Shared Knowledge Base', '#E6E6FA')
    ax.text(7, 1.2, '• Attack patterns\n• Baseline models\n• Historical alerts\n• Feedback data', 
            fontsize=8, ha='center')
    
    # Arrows to knowledge base
    for x in [2.25, 6.25, 10.25]:
        draw_arrow(ax, (x, 3.6), (7, 2.9), '<->', 'gray', 1.5)
    draw_arrow(ax, (7, 6.9), (7, 2.9), '<->', 'gray', 1.5)
    
    # External Systems
    draw_box(ax, (0.5, 0.2), 2, 0.7, 'SIEM\nSystem', '#FFA07A')
    draw_box(ax, (3, 0.2), 2, 0.7, 'Firewall\nControl', '#FFA07A')
    draw_box(ax, (6, 0.2), 2, 0.7, 'Alert\nDashboard', '#FFA07A')
    draw_box(ax, (9, 0.2), 2, 0.7, 'Incident\nResponse', '#FFA07A')
    draw_box(ax, (11.5, 0.2), 2, 0.7, 'Threat\nIntel Feed', '#FFA07A')
    
    # Arrows to external systems
    for x in [1.5, 4, 7, 10, 12.5]:
        draw_arrow(ax, (7, 1.9), (x, 1.0), '->', 'darkred', 1.5)
    
    plt.tight_layout()
    plt.savefig('images/04_multi_agent_architecture.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Multi-Agent Architecture Diagram")

def generate_attack_detection_process():
    """Generate Attack Detection Process Flowchart"""
    fig, ax = plt.subplots(figsize=(12, 14))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 14)
    ax.axis('off')
    
    # Title
    ax.text(6, 13.5, 'Attack Detection Process Flowchart', 
            ha='center', fontsize=16, weight='bold')
    
    y = 12.5
    
    # Start
    circle = Circle((6, y+0.35), 0.4, color='#00FF00', ec='black', linewidth=2)
    ax.add_patch(circle)
    ax.text(6, y+0.35, 'START', ha='center', va='center', fontsize=9, weight='bold')
    draw_arrow(ax, (6, y), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Capture Data
    draw_box(ax, (3, y), 6, 0.7, 'Capture Network Traffic & Logs', '#FFD700')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Parse & Normalize
    draw_box(ax, (3, y), 6, 0.7, 'Parse & Normalize Data', '#87CEEB')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Extract Features
    draw_box(ax, (3, y), 6, 0.7, 'Extract Security Features', '#ADD8E6')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Check Signature
    draw_box(ax, (4, y), 4, 0.7, 'Known Signature\nMatch?', '#FFFF99')
    
    # Yes - Known Attack
    draw_arrow(ax, (8, y+0.35), (10, y+0.35), '->', 'red', 2)
    draw_box(ax, (10, y), 1.5, 0.7, 'Known\nAttack', '#FF6347')
    ax.text(8.7, y+0.5, 'YES', fontsize=8, weight='bold', color='red')
    draw_arrow(ax, (10.75, y-0.1), (10.75, y-0.8), '->', 'red', 2)
    
    # No - Continue
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    ax.text(5.5, y-0.3, 'NO', fontsize=8, weight='bold')
    y -= 1.2
    
    # Run Anomaly Models
    draw_box(ax, (3, y), 6, 0.7, 'Run Multi-Model Anomaly Detection', '#FF6B6B')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Deviation Check
    draw_box(ax, (4, y), 4, 0.7, 'Significant\nDeviation?', '#FFFF99')
    
    # No - Normal
    draw_arrow(ax, (4, y+0.35), (1.5, y+0.35), '->', 'green', 2)
    draw_box(ax, (0.2, y), 1.5, 0.7, 'Normal\nBehavior', '#90EE90')
    ax.text(3.2, y+0.5, 'NO', fontsize=8, weight='bold', color='green')
    draw_arrow(ax, (0.95, y-0.1), (0.95, 0.5), '->', 'green', 1.5)
    
    # Yes - Continue
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'red', 2)
    ax.text(6.5, y-0.3, 'YES', fontsize=8, weight='bold', color='red')
    y -= 1.2
    
    # Correlation
    draw_box(ax, (3, y), 6, 0.7, 'Correlate with Recent Events', '#DDA0DD')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Classify
    draw_box(ax, (3, y), 6, 0.7, 'Classify Attack Type & Severity', '#FFB6C1')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    draw_arrow(ax, (10.75, y+3.5), (6, y+0.8), '->', 'red', 2)
    y -= 1.2
    
    # Generate Explanation
    draw_box(ax, (3, y), 6, 0.7, 'Generate Explainable Alert', '#F0E68C')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Priority Check
    draw_box(ax, (4, y), 4, 0.7, 'High Priority\nAlert?', '#FFFF99')
    
    # No - Log
    draw_arrow(ax, (4, y+0.35), (1.5, y+0.35), '->', 'orange', 2)
    draw_box(ax, (0.2, y), 1.5, 0.7, 'Log & Queue', '#FFE4B5')
    ax.text(3.2, y+0.5, 'NO', fontsize=8, weight='bold', color='orange')
    
    # Yes - Alert
    draw_arrow(ax, (8, y+0.35), (10, y+0.35), '->', 'red', 2)
    draw_box(ax, (10, y), 1.5, 0.7, 'Immediate\nAlert', '#FF6347')
    ax.text(8.7, y+0.5, 'YES', fontsize=8, weight='bold', color='red')
    
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Notify SOC
    draw_box(ax, (3, y), 6, 0.7, 'Notify SOC Team / Dashboard', '#FFA07A')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Wait for Feedback
    draw_box(ax, (3, y), 6, 0.7, 'Wait for Admin Feedback', '#E6E6FA')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Update Model
    draw_box(ax, (3, y), 6, 0.7, 'Update Baseline & Retrain Model', '#98FB98')
    draw_arrow(ax, (6, y-0.1), (6, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # End
    circle = Circle((6, y+0.35), 0.4, color='#FF6347', ec='black', linewidth=2)
    ax.add_patch(circle)
    ax.text(6, y+0.35, 'END', ha='center', va='center', fontsize=9, weight='bold')
    
    # Feedback loop arrow
    draw_arrow(ax, (0.95, 0.8), (0.2, 11.5), '->', 'purple', 2)
    draw_arrow(ax, (0.2, 11.5), (3, 11.9), '->', 'purple', 2)
    ax.text(0, 6, 'Continuous\nMonitoring', fontsize=9, weight='bold', 
            color='purple', rotation=90, va='center')
    
    plt.tight_layout()
    plt.savefig('images/05_attack_detection_process.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Attack Detection Process Flowchart")

def generate_alert_generation_workflow():
    """Generate Alert Generation Workflow"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Smart Alert Generation & Prioritization Workflow', 
            ha='center', fontsize=16, weight='bold')
    
    y = 8.5
    
    # Input
    draw_box(ax, (4.5, y), 5, 0.7, 'Detected Anomaly Event', '#FFD700')
    draw_arrow(ax, (7, y-0.1), (7, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Extract Context
    draw_box(ax, (4.5, y), 5, 0.7, 'Extract Event Context', '#87CEEB')
    ax.text(10.5, y+0.35, '• Timestamp\n• Source/Dest IP\n• Attack type\n• Confidence', 
            fontsize=8, va='center')
    draw_arrow(ax, (7, y-0.1), (7, y-0.5), '->', 'black', 2)
    y -= 1.5
    
    # Correlation Engine
    draw_box(ax, (2, y), 10, 0.9, 'Alert Correlation Engine', '#FF6B6B')
    
    # Sub-processes
    draw_box(ax, (0.5, y-1.2), 2.2, 0.7, 'Check Recent\nAlerts', '#FFB6C1')
    draw_box(ax, (3.2, y-1.2), 2.2, 0.7, 'Find Related\nEvents', '#FFB6C1')
    draw_box(ax, (5.9, y-1.2), 2.2, 0.7, 'Detect Attack\nChain', '#FFB6C1')
    draw_box(ax, (8.6, y-1.2), 2.2, 0.7, 'Group Similar\nAlerts', '#FFB6C1')
    draw_box(ax, (11.3, y-1.2), 2.2, 0.7, 'Calculate\nAggregated Risk', '#FFB6C1')
    
    for x in [1.6, 4.3, 7, 9.7, 12.4]:
        draw_arrow(ax, (7, y-0.1), (x, y-0.5), '->', 'red', 1.5)
        draw_arrow(ax, (x, y-1.2), (x, y-2.2), '->', 'red', 1.5)
    
    y -= 2.8
    
    # Severity Scoring
    draw_box(ax, (4.5, y), 5, 0.7, 'Calculate Severity Score', '#DDA0DD')
    ax.text(2, y+0.35, 'Factors:\n• Attack type\n• Target criticality\n• Confidence score\n• Impact scope', 
            fontsize=8, va='center')
    draw_arrow(ax, (7, y-0.1), (7, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Priority Assignment
    draw_box(ax, (4.5, y), 5, 0.7, 'Assign Priority Level', '#FFB6C1')
    
    # Priority branches
    draw_arrow(ax, (7, y-0.1), (2, y-1), '->', 'gray', 1.5)
    draw_arrow(ax, (7, y-0.1), (7, y-1), '->', 'orange', 1.5)
    draw_arrow(ax, (7, y-0.1), (12, y-1), '->', 'red', 1.5)
    
    y -= 1.5
    
    draw_box(ax, (0.5, y), 2.5, 0.7, 'Low Priority', '#90EE90')
    ax.text(1.75, y-0.5, 'Queue for review', fontsize=8, ha='center')
    
    draw_box(ax, (5.75, y), 2.5, 0.7, 'Medium Priority', '#FFE4B5')
    ax.text(7, y-0.5, 'Log & notify', fontsize=8, ha='center')
    
    draw_box(ax, (11, y), 2.5, 0.7, 'High/Critical', '#FF6347')
    ax.text(12.25, y-0.5, 'Immediate alert', fontsize=8, ha='center')
    
    y -= 1.3
    
    # Generate Explanation
    draw_box(ax, (4.5, y), 5, 0.7, 'Generate Explainable Alert', '#F0E68C')
    draw_arrow(ax, (1.75, y+1), (5.5, y+0.8), '->', 'green', 1.5)
    draw_arrow(ax, (7, y+1), (7, y+0.8), '->', 'orange', 1.5)
    draw_arrow(ax, (12.25, y+1), (8.5, y+0.8), '->', 'red', 1.5)
    
    ax.text(10.5, y+0.35, 'Include:\n• Root cause\n• Evidence\n• Timeline\n• Recommendation', 
            fontsize=8, va='center')
    draw_arrow(ax, (7, y-0.1), (7, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Format Output
    draw_box(ax, (4.5, y), 5, 0.7, 'Format as Structured JSON Alert', '#ADD8E6')
    draw_arrow(ax, (7, y-0.1), (7, y-0.5), '->', 'black', 2)
    y -= 1.2
    
    # Output Channels
    draw_box(ax, (1, y), 2, 0.7, 'Dashboard\nUI', '#FFA07A')
    draw_box(ax, (3.5, y), 2, 0.7, 'Email/SMS\nAlert', '#FFA07A')
    draw_box(ax, (6, y), 2, 0.7, 'SIEM\nIntegration', '#FFA07A')
    draw_box(ax, (8.5, y), 2, 0.7, 'Incident\nTicket', '#FFA07A')
    draw_box(ax, (11, y), 2, 0.7, 'API\nWebhook', '#FFA07A')
    
    for x in [2, 4.5, 7, 9.5, 12]:
        draw_arrow(ax, (7, y+0.8), (x, y+0.8), '->', 'darkred', 1.5)
    
    plt.tight_layout()
    plt.savefig('images/06_alert_generation_workflow.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Alert Generation Workflow")

def generate_feedback_loop():
    """Generate Self-Learning Feedback Loop Diagram"""
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)
    ax.axis('off')
    
    # Title
    ax.text(6, 11.5, 'Self-Learning Feedback Loop', 
            ha='center', fontsize=16, weight='bold')
    
    # Center - AI Model
    draw_box(ax, (4.5, 5), 3, 1, 'AI Detection\nModel', '#FF6347')
    
    # Stage 1: Detection & Alert
    draw_box(ax, (4.5, 8), 3, 0.8, 'Generate Alert', '#FFD700')
    draw_arrow(ax, (6, 7.9), (6, 6.1), '->', 'black', 2)
    ax.text(6.5, 7, '①', fontsize=14, weight='bold', color='blue')
    
    # Stage 2: Admin Review
    draw_box(ax, (8.5, 5), 3, 0.8, 'Admin\nReview', '#87CEEB')
    draw_arrow(ax, (7.5, 5.5), (8.5, 5.5), '->', 'blue', 2)
    ax.text(8, 5.7, '②', fontsize=14, weight='bold', color='blue')
    
    # Stage 3: Feedback
    draw_box(ax, (8.5, 2.5), 3, 1.2, 'Feedback\nClassification', '#98FB98')
    ax.text(10, 2.2, '✓ True Positive\n✗ False Positive\n⚠ Missed Attack', 
            fontsize=8, ha='center')
    draw_arrow(ax, (10, 4.9), (10, 3.8), '->', 'green', 2)
    ax.text(10.5, 4.3, '③', fontsize=14, weight='bold', color='blue')
    
    # Stage 4: Update Training Data
    draw_box(ax, (4.5, 2.5), 3, 0.8, 'Update Training\nDataset', '#FFB6C1')
    draw_arrow(ax, (8.5, 3), (7.5, 3), '->', 'purple', 2)
    ax.text(8, 3.2, '④', fontsize=14, weight='bold', color='blue')
    
    # Stage 5: Retrain Model
    draw_box(ax, (0.5, 5), 3, 0.8, 'Model\nRetraining', '#DDA0DD')
    draw_arrow(ax, (5, 2.9), (2, 4.9), '->', 'orange', 2)
    ax.text(3.5, 4, '⑤', fontsize=14, weight='bold', color='blue')
    
    # Stage 6: Update Baseline
    draw_box(ax, (0.5, 7.5), 3, 0.8, 'Update Behavioral\nBaseline', '#F0E68C')
    draw_arrow(ax, (2, 5.9), (2, 7.4), '->', 'red', 2)
    ax.text(2.5, 6.7, '⑥', fontsize=14, weight='bold', color='blue')
    
    # Stage 7: Deploy Updated Model
    draw_arrow(ax, (3.5, 7.9), (4.5, 6), '->', 'darkgreen', 2)
    ax.text(4, 7, '⑦', fontsize=14, weight='bold', color='blue')
    
    # Improvement Metrics Box
    draw_box(ax, (1, 1), 4, 1, 'Continuous Improvement\nMetrics', '#E6E6FA')
    ax.text(3, 0.3, '• Reduced false positives\n• Improved accuracy\n• Faster detection\n• Adaptive thresholds', 
            fontsize=8, ha='center')
    draw_arrow(ax, (2, 2.1), (3, 2.1), '<->', 'purple', 1.5)
    
    # Knowledge Base
    draw_box(ax, (7, 0.5), 4, 0.8, 'Attack Pattern Knowledge Base', '#FFA07A')
    draw_arrow(ax, (10, 1.4), (10, 2.4), '<->', 'brown', 1.5)
    
    # Timeline indicator
    ax.text(0.5, 10.5, 'Time', fontsize=11, weight='bold', style='italic')
    draw_arrow(ax, (0.5, 10.2), (0.5, 0.5), '->', 'gray', 2)
    ax.text(0.2, 5.5, '↓', fontsize=20, color='gray')
    
    # Cycle indicator
    from matplotlib.patches import Arc
    arc = Arc((6, 6), 8, 8, angle=0, theta1=80, theta2=460, 
              color='purple', linewidth=3, linestyle='--')
    ax.add_patch(arc)
    ax.text(0.8, 9.5, 'Continuous\nLearning Cycle', fontsize=10, 
            weight='bold', color='purple', style='italic')
    
    plt.tight_layout()
    plt.savefig('images/07_feedback_loop_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Self-Learning Feedback Loop Diagram")

def generate_attack_types_classification():
    """Generate Attack Types Classification Diagram"""
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(7, 9.5, 'Attack Types Classification & Detection Features', 
            ha='center', fontsize=16, weight='bold')
    
    # Central Classification Engine
    draw_box(ax, (5, 7.5), 4, 0.8, 'AI Classification Engine', '#FF6347')
    
    # Attack Type 1: DoS/DDoS
    draw_box(ax, (0.5, 6), 2.5, 0.7, 'DoS / DDoS', '#FFB6C1')
    ax.text(1.75, 5.2, '• Traffic spikes\n• SYN floods\n• UDP floods\n• Connection exhaustion', 
            fontsize=7, ha='center')
    draw_arrow(ax, (3, 6.3), (5, 7.8), '->', 'red', 1.5)
    
    # Attack Type 2: Brute Force
    draw_box(ax, (3.5, 6), 2.5, 0.7, 'Brute Force', '#FFB6C1')
    ax.text(4.75, 5.2, '• Failed login attempts\n• Password guessing\n• Credential stuffing\n• Dictionary attacks', 
            fontsize=7, ha='center')
    draw_arrow(ax, (5, 6.3), (6.3, 7.4), '->', 'red', 1.5)
    
    # Attack Type 3: Malware
    draw_box(ax, (6.5, 6), 2.5, 0.7, 'Malware Activity', '#FFB6C1')
    ax.text(7.75, 5.2, '• Suspicious processes\n• C&C communication\n• File encryption\n• Registry changes', 
            fontsize=7, ha='center')
    draw_arrow(ax, (7.5, 6.7), (7.5, 7.4), '->', 'red', 1.5)
    
    # Attack Type 4: Privilege Escalation
    draw_box(ax, (9.5, 6), 2.5, 0.7, 'Privilege\nEscalation', '#FFB6C1')
    ax.text(10.75, 5.2, '• Unauthorized access\n• Exploit attempts\n• Root access\n• Token manipulation', 
            fontsize=7, ha='center')
    draw_arrow(ax, (10, 6.7), (8.5, 7.6), '->', 'red', 1.5)
    
    # Attack Type 5: Data Exfiltration
    draw_box(ax, (0.5, 3.5), 2.5, 0.7, 'Data\nExfiltration', '#FFB6C1')
    ax.text(1.75, 2.7, '• Large data transfers\n• Unusual destinations\n• Off-hours activity\n• Encrypted channels', 
            fontsize=7, ha='center')
    draw_arrow(ax, (2, 4.2), (5.5, 7.4), '->', 'red', 1.5)
    
    # Attack Type 6: Port Scanning
    draw_box(ax, (3.5, 3.5), 2.5, 0.7, 'Port Scanning /\nReconnaissance', '#FFB6C1')
    ax.text(4.75, 2.7, '• Sequential port access\n• Service enumeration\n• Network mapping\n• Vulnerability probing', 
            fontsize=7, ha='center')
    draw_arrow(ax, (5, 4.2), (6, 7.4), '->', 'red', 1.5)
    
    # Attack Type 7: SQL Injection
    draw_box(ax, (6.5, 3.5), 2.5, 0.7, 'SQL Injection /\nCode Injection', '#FFB6C1')
    ax.text(7.75, 2.7, '• Malicious queries\n• Input validation bypass\n• DB error patterns\n• Union attacks', 
            fontsize=7, ha='center')
    draw_arrow(ax, (7.5, 4.2), (7.2, 7.4), '->', 'red', 1.5)
    
    # Attack Type 8: Lateral Movement
    draw_box(ax, (9.5, 3.5), 2.5, 0.7, 'Lateral\nMovement', '#FFB6C1')
    ax.text(10.75, 2.7, '• Internal scanning\n• Service hopping\n• Credential reuse\n• Remote execution', 
            fontsize=7, ha='center')
    draw_arrow(ax, (10.5, 4.2), (8.5, 7.5), '->', 'red', 1.5)
    
    # Detection Features Box
    draw_box(ax, (2, 1.2), 10, 1, 'Common Detection Features', '#F0E68C')
    ax.text(7, 0.5, 'Packet size • Request frequency • Protocol type • Port numbers • Payload patterns\n'
            'Time of day • Source/Destination IPs • User behavior • System calls • Network topology\n'
            'Connection duration • Byte rate • Error rates • Authentication patterns', 
            fontsize=8, ha='center')
    
    plt.tight_layout()
    plt.savefig('images/08_attack_types_classification.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Generated: Attack Types Classification Diagram")

# Main execution
if __name__ == "__main__":
    print("\n" + "="*60)
    print("Generating AI-IDS Architecture Diagrams...")
    print("="*60 + "\n")
    
    generate_system_architecture()
    generate_data_flow_diagram()
    generate_ai_pipeline()
    generate_multi_agent_architecture()
    generate_attack_detection_process()
    generate_alert_generation_workflow()
    generate_feedback_loop()
    generate_attack_types_classification()
    
    print("\n" + "="*60)
    print("✅ All diagrams generated successfully!")
    print("Location: architecture/images/")
    print("="*60 + "\n")
