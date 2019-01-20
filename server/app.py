from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_reggie import Reggie
import os
from http import HTTPStatus
from decorators import fields_required_for_upload, allowed_mimetypes, save_file_and_get_file_path
from utils import split_image, create_zip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['PROJECT_ROOT_DIR'] = os.path.dirname(os.path.abspath(__file__))
CORS(app)
Reggie(app)


@app.route('/download/<path:file_path>', methods=['GET'])
def download_zip(file_path):
    os.chdir(app.config['UPLOAD_FOLDER'])
    try:
        if os.path.isdir(file_path):
            zip_file_name = create_zip(file_path)
            file_res = send_from_directory(app.config['UPLOAD_FOLDER'], zip_file_name, as_attachment=True)
            os.remove(zip_file_name)
            return file_res
        elif os.path.isfile(file_path):
            print(os.path.exists(file_path))
            return send_from_directory(app.config['UPLOAD_FOLDER'], file_path, as_attachment=True)
        else:
            json_res = jsonify({'message': 'Unknown path!'})
            json_res.status_code = HTTPStatus.BAD_REQUEST
            return json_res
    except FileNotFoundError:
        json_res = jsonify({'message': 'File Not Found!'})
        json_res.status_code = HTTPStatus.BAD_REQUEST
        return json_res
    finally:
        os.chdir(app.config['PROJECT_ROOT_DIR'])


@app.route('/uploads/<path:file_path>', methods=['GET'])
def serve_files(file_path):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], file_path)
    except FileNotFoundError:
        json_res = jsonify({'message': 'File Not Found!'})
        json_res.status_code = HTTPStatus.BAD_REQUEST
        return json_res


@app.route('/split/<regex("[1-9]+x[1-9]+"):matrix>', methods=['POST'])
@fields_required_for_upload
@allowed_mimetypes
@save_file_and_get_file_path
def split(matrix, uploaded_file_path, timestamp):
    split_image(uploaded_file_path, matrix)

    os.remove(uploaded_file_path)

    json_res = jsonify(
        {'dirname': timestamp, 'files': os.listdir(app.config['UPLOAD_FOLDER'] + timestamp)})
    json_res.status_code = HTTPStatus.CREATED
    return json_res


if __name__ == '__main__':
    app.run('0.0.0.0')
