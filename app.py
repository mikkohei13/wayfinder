from flask import Flask, send_from_directory, jsonify, render_template
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import shutil
import os
import json


# Load the configuration
with open('secrets.json', 'r') as file:
    config = json.load(file)

app = Flask(__name__)
local_dir = 'local_files'
monitor_dir = config['monitor_dir']

if not os.path.exists(local_dir):
    os.makedirs(local_dir)

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        for filename in os.listdir(monitor_dir):
            if filename not in os.listdir(local_dir):
                shutil.copy(os.path.join(monitor_dir, filename), os.path.join(local_dir, filename))
                print(f'Copied: {filename}')

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path=monitor_dir, recursive=False)
observer.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_files')
def get_files():
    files = os.listdir(local_dir)
    return jsonify(files)

@app.route('/files/<path:filename>')
def download_file(filename):
    return send_from_directory(local_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
