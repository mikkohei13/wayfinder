from flask import Flask, render_template, send_from_directory, jsonify
import os
import json

# Load the configuration
with open('secrets.json', 'r') as file:
    config = json.load(file)

app = Flask(__name__)
local_dir = 'local_files'
monitor_dir = config['monitor_dir']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_files')
def get_files():
    files = [f for f in os.listdir(monitor_dir) if os.path.isfile(os.path.join(monitor_dir, f))]
    return jsonify(files)

@app.route('/files/<path:filename>')
def download_file(filename):
    return send_from_directory(monitor_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
