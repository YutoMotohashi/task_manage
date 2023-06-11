from flask import Flask, render_template, jsonify, request
import json
import os
import time
import shutil
from . import progress_json_manage

app = Flask(__name__)

_file_path = None


def progress_display(file_path):
    global _file_path
    _file_path = file_path
    # get the directory of the current script
    script_dir = os.path.dirname(__file__)
    # join the script directory with the filename
    archive_path = os.path.join(os.path.dirname(_file_path), 'archive')
    if not os.path.exists(archive_path):
        os.makedirs(archive_path)

    current_time = time.localtime()
    timestamp = time.strftime("%y%m%d%H%M%S", current_time)
    dest = os.path.join(archive_path, f"{timestamp}.json")
    shutil.copy2(_file_path, dest)
    app.run(port=5000)


@app.route('/')
def home():
    return render_template('progress_display.html')


@app.route('/get_data')
def get_data():
    global _file_path
    print(f"data <- {_file_path}")
    with open(_file_path) as f:
        data = json.load(f)
    assert progress_json_manage.validate_progress_data_format(data[0])
    return jsonify(data)


@app.route('/save_data', methods=['POST'])
def save_data():
    global _file_path
    data = request.json
    # Save the data to a file or perform any other desired operations
    with open(_file_path, 'w') as f:
        json.dump(data, f)

    progress_json_manage.update_progress(_file_path)
    print("data saved successfully")
    # Return a response indicating the successful saving of the data
    return jsonify({'message': 'Data saved successfully'})


if __name__ == '__main__':
    progress_display(file_path)
