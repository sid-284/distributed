from flask import Flask, render_template, jsonify, request
import logging
import time
from datetime import datetime
import threading
from checking import TimeSyncNode, TestSuite, Benchmark

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state
system_state = {
    'nodes': {},
    'test_suite': None,
    'benchmark': None,
    'logs': [],
    'is_running': False,
    'last_update': None
}

# Lock for thread safety
state_lock = threading.Lock()

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

def add_log(message, level='info'):
    with state_lock:
        timestamp = time.time()
        system_state['logs'].append({
            'timestamp': timestamp,
            'message': message,
            'level': level
        })
        # Keep only last 1000 logs
        if len(system_state['logs']) > 1000:
            system_state['logs'] = system_state['logs'][-1000:]
        system_state['last_update'] = timestamp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    with state_lock:
        return jsonify({
            'nodes': system_state['nodes'],
            'is_running': system_state['is_running'],
            'last_update': system_state['last_update']
        })

@app.route('/api/start', methods=['POST'])
def start_system():
    with state_lock:
        if system_state['is_running']:
            return jsonify({'status': 'error', 'message': 'System is already running'})

        try:
            # Initialize test suite
            system_state['test_suite'] = TestSuite()
            system_state['benchmark'] = Benchmark()
            
            # Start nodes
            for i in range(5):
                node_id = f'node_{i:02d}'
                port = 8000 + i
                node = TimeSyncNode(node_id, port)
                node.start()
                system_state['nodes'][node_id] = {
                    'id': node_id,
                    'port': port,
                    'status': 'running',
                    'drift': 0,
                    'last_seen': time.time()
                }
            
            system_state['is_running'] = True
            add_log('System started successfully')
            return jsonify({'status': 'success'})
        except Exception as e:
            add_log(f'Error starting system: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/stop', methods=['POST'])
def stop_system():
    with state_lock:
        if not system_state['is_running']:
            return jsonify({'status': 'error', 'message': 'System is not running'})

        try:
            # Stop all nodes
            for node_id, node_data in system_state['nodes'].items():
                node = TimeSyncNode(node_id, node_data['port'])
                node.stop()
                system_state['nodes'][node_id]['status'] = 'stopped'
            
            system_state['is_running'] = False
            add_log('System stopped successfully')
            return jsonify({'status': 'success'})
        except Exception as e:
            add_log(f'Error stopping system: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/run_tests', methods=['POST'])
def run_tests():
    with state_lock:
        if not system_state['is_running']:
            return jsonify({'status': 'error', 'message': 'System is not running'})

        try:
            # Run test suite
            results = system_state['test_suite'].run_all()
            add_log('Test suite completed successfully')
            return jsonify({'status': 'success', 'results': results})
        except Exception as e:
            add_log(f'Error running tests: {str(e)}', 'error')
            return jsonify({'status': 'error', 'message': str(e)})

def update_node_status():
    """Background thread to update node status"""
    while True:
        with state_lock:
            if system_state['is_running']:
                current_time = time.time()
                for node_id, node_data in system_state['nodes'].items():
                    node = TimeSyncNode(node_id, node_data['port'])
                    if node.is_running():
                        stats = node.get_stats()
                        system_state['nodes'][node_id].update({
                            'status': 'running',
                            'drift': stats.get('drift', 0),
                            'last_seen': current_time
                        })
                    else:
                        system_state['nodes'][node_id]['status'] = 'failed'
                system_state['last_update'] = current_time
        time.sleep(1)

if __name__ == '__main__':
    # Start background thread for node status updates
    status_thread = threading.Thread(target=update_node_status, daemon=True)
    status_thread.start()
    
    # Run Flask app
    app.run(debug=True, use_reloader=False) 