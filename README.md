# Distributed Time Synchronization System

A distributed time synchronization system with a modern web interface for monitoring and managing time synchronization across multiple nodes.

## Features

- Distributed time synchronization across multiple nodes
- Real-time monitoring of node status and drift measurements
- Modern web interface with live updates
- Fault tolerance and automatic node recovery
- Blockchain-based timestamp verification
- Comprehensive logging and statistics

## Requirements

- Python 3.13 or higher
- Flask
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate a virtual environment:
```bash
python3.13 -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install flask
```

## Usage

1. Start the web interface:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

3. Use the web interface to:
   - Start/stop the time synchronization system
   - Monitor node status and drift measurements
   - View system logs
   - Run test suites

## System Architecture

The system consists of multiple components:

- **Time Sync Nodes**: Individual nodes that maintain time synchronization
- **Test Suite**: Validates system functionality and performance
- **Benchmark**: Measures system performance metrics
- **Web Interface**: Provides real-time monitoring and control

## Notes

- The system is designed to work in a test environment
- NTP sync failures are expected without external NTP server access
- The system includes fault tolerance mechanisms for node failures

## License

MIT License 