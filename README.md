# Distributed Time Synchronization System

A Flask-based web application for managing and testing a distributed system with time synchronization nodes. This system provides a web interface to monitor, control, and test a network of time-synchronized nodes.

## Features

- Web-based dashboard for system monitoring
- Real-time node status updates
- Comprehensive test suite execution
- Performance benchmarking
- System logs with timestamps
- Start/Stop system control
- Support for multiple nodes in the network

## Prerequisites

- Python 3.x
- Flask
- Other dependencies (to be listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

- `GET /`: Main dashboard interface
- `GET /api/status`: Get current system status and node information
- `GET /api/start`: Start the distributed system
- `GET /api/stop`: Stop the distributed system
- `GET /api/run_tests`: Execute the test suite

## System Components

- **TimeSyncNode**: Individual nodes in the distributed system
- **TestSuite**: Comprehensive test suite for system validation
- **PerformanceBenchmark**: Performance testing and benchmarking tools

## Logging

The system maintains a log of all operations with timestamps. Logs are limited to the last 1000 entries and are available through the web interface.

## Development

The application is built with:
- Flask for the web framework
- Python for the backend logic
- HTML templates for the frontend interface

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here] 