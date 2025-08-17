from flask import Flask, render_template, jsonify, request
import os
import subprocess

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/scan', methods=['GET'])
def scan_directories():
    base_dir = os.getcwd()
    dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    return jsonify({'dirs': dirs})

@app.route('/redeploy/<dirname>', methods=['POST'])
def redeploy(dirname):
    base_dir = os.getcwd()
    target_dir = os.path.join(base_dir, dirname)
    if not os.path.isdir(target_dir):
        return jsonify({'status': 'error', 'message': 'Directory not found'}), 404
    try:
        cmds = [
            'docker-compose down',
            'git pull',
            'docker-compose build',
            'docker-compose up -d'
        ]
        for cmd in cmds:
            subprocess.run(cmd, shell=True, cwd=target_dir, check=True)
        return jsonify({'status': 'ok'})
    except subprocess.CalledProcessError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
