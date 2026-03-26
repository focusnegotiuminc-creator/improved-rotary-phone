from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

GITHUB_USER = os.environ.get('GITHUB_USER', 'thegreatmachevilli')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
BASE_PATH = os.environ.get('BASE_PATH', './github_repos')


@app.route('/sync', methods=['POST'])
def sync_repos():
    try:
        cmd = (
            f'python3 github_remote_connector.py --user {GITHUB_USER} '
            f'--token {GITHUB_TOKEN} --path {BASE_PATH} --action sync'
        )
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'message': 'Repositories synced'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/clone', methods=['POST'])
def clone_repos():
    try:
        cmd = (
            f'python3 github_remote_connector.py --user {GITHUB_USER} '
            f'--token {GITHUB_TOKEN} --path {BASE_PATH} --action clone'
        )
        subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'message': 'All repositories cloned'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/report', methods=['GET'])
def get_report():
    try:
        cmd = (
            f'python3 github_remote_connector.py --user {GITHUB_USER} '
            f'--token {GITHUB_TOKEN} --path {BASE_PATH} --action report'
        )
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return jsonify({'status': 'success', 'report': result.stdout})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'user': GITHUB_USER})


@app.route('/', methods=['GET'])
def index():
    return jsonify({'endpoints': ['/health', '/sync', '/clone', '/report']})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
