from flask import Flask, render_template, jsonify
from checking import TimeSyncNode, TestSuite, PerformanceBenchmark
import threading
import time
import json
from datetime import datetime

app = Flask(__name__)

# Global variables to store system state
system_state = {
    'nodes': [],
    'test_suite': None,
    'benchmark': None,
    'is_running': False,
    'last_update': None,
    'logs': []
}

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def log_message(message, level='INFO'):
    timestamp = time.time()
    system_state['logs'].append({
        'timestamp': timestamp,
        'formatted_time': format_timestamp(timestamp),
        'message': message,
        'level': level
    })
    # Keep only last 1000 logs
    if len(system_state['logs']) > 1000:
        system_state['logs'] = system_state['logs'][-1000:]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    if not system_state['nodes']:
        return jsonify({
            'status': 'stopped',
            'nodes': [],
            'logs': system_state['logs'][-100:],  # Last 100 logs
            'last_update': system_state['last_update']
        })
    
    nodes_status = []
    for node in system_state['nodes']:
        if node.is_running:
            status = node.get_status()
            status['uptime'] = format_timestamp(time.time() - status['uptime'])
            nodes_status.append(status)
    
    system_state['last_update'] = format_timestamp(time.time())
    
    return jsonify({
        'status': 'running' if system_state['is_running'] else 'stopped',
        'nodes': nodes_status,
        'logs': system_state['logs'][-100:],  # Last 100 logs
        'last_update': system_state['last_update']
    })

@app.route('/api/start')
def start_system():
    if system_state['is_running']:
        return jsonify({'status': 'error', 'message': 'System is already running'})
    
    try:
        # Initialize test suite
        system_state['test_suite'] = TestSuite()
        system_state['benchmark'] = PerformanceBenchmark()
        
        # Setup test network
        log_message("Setting up test network with 5 nodes...")
        system_state['nodes'] = system_state['test_suite'].setup_test_network(5)
        
        # Start all nodes
        for node in system_state['nodes']:
            node.start()
            log_message(f"Started node: {node.node_id}")
        
        system_state['is_running'] = True
        return jsonify({'status': 'success', 'message': 'System started successfully'})
    except Exception as e:
        log_message(f"Error starting system: {str(e)}", 'ERROR')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stop')
def stop_system():
    if not system_state['is_running']:
        return jsonify({'status': 'error', 'message': 'System is not running'})
    
    try:
        for node in system_state['nodes']:
            if node.is_running:
                node.stop()
                log_message(f"Stopped node: {node.node_id}")
        
        system_state['is_running'] = False
        system_state['nodes'] = []
        return jsonify({'status': 'success', 'message': 'System stopped successfully'})
    except Exception as e:
        log_message(f"Error stopping system: {str(e)}", 'ERROR')
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/run_tests')
def run_tests():
    if not system_state['is_running']:
        return jsonify({'status': 'error', 'message': 'System must be running to execute tests'})
    
    try:
        log_message("Starting comprehensive test suite...")
        results = system_state['test_suite'].run_all_tests()
        
        # Log test results
        for test_name, result in results.items():
            if test_name != 'summary':
                log_message(f"Test {test_name}: {json.dumps(result)}")
        
        return jsonify({
            'status': 'success',
            'results': results
        })
    except Exception as e:
        log_message(f"Error running tests: {str(e)}", 'ERROR')
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000) 