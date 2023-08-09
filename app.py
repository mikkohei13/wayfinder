from flask import Flask, render_template, send_from_directory, jsonify
import json
import helpers

# Load the configuration
with open('secrets.json', 'r') as file:
    config = json.load(file)

app = Flask(__name__)
local_dir = 'local_files'
monitor_dir = config['monitor_dir']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/latest')
def latest():
    return render_template('latest.html')

# Returns a json list of files
@app.route('/get_files')
def get_files():
    print("--")
    helpers.get_identifications(monitor_dir)
    files = helpers.get_photo_list(monitor_dir)
    return jsonify(files)

# Shows a file from mounted dir over Flask
@app.route('/files/<path:filename>')
def download_file(filename):
    return send_from_directory(monitor_dir, filename)

if __name__ == "__main__":
    app.run(debug=True)
