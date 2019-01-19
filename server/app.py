from flask import Flask, jsonify, send_from_directory, send_file
from flask_cors import CORS, cross_origin
from flask_reggie import Reggie
import mimetypes
import os
from http import HTTPStatus
from decorators import fields_required_for_download, fields_required_for_upload, allowed_mimetypes
from utils import join_uploads_dir_with_filename, chop_image_from_path, create_zip

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
CORS(app)
Reggie(app)

ALLOWED_EXTENSIONS = {'image/png', 'image/jpeg'}


@app.route('/download/<dirname>', methods=['GET'])
@cross_origin()
def download_zip(dirname):
    os.chdir(app.config['UPLOAD_FOLDER'])
    try:
        zip_file_name = create_zip(dirname)
        file_res = send_from_directory(os.getcwd(), zip_file_name, as_attachment=True)
        os.remove(zip_file_name)
        return file_res
    except FileNotFoundError:
        json_res = jsonify({'message': 'File Not Found!'})
        json_res.status_code = HTTPStatus.BAD_REQUEST
        return json_res
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))


@app.route('/download/<dirname>/<filename>', methods=['GET'])
def download_single_image(dirname, filename):
    os.chdir(app.config['UPLOAD_FOLDER'])
    try:
        return send_from_directory(os.path.join(os.getcwd(), dirname), filename, as_attachment=True)
    except FileNotFoundError:
        json_res = jsonify({'message': 'File Not Found!'})
        json_res.status_code = HTTPStatus.BAD_REQUEST
        return json_res
    finally:
        os.chdir(os.path.dirname(os.path.abspath(__file__)))


@app.route('/uploads/<dirname>/<filename>', methods=['GET'])
def serve_files(dirname, filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'] + dirname, filename)


@app.route('/chop/<regex("[1-9]+x[1-9]+"):matrix>', methods=['POST'])
@fields_required_for_upload
@allowed_mimetypes
def chop(matrix, file):
    uploaded_file_path, timestamp = join_uploads_dir_with_filename(app.config['UPLOAD_FOLDER'],
                                                                   mimetypes.guess_all_extensions(file.mimetype)[-1])
    file.save(uploaded_file_path)

    chop_image_from_path(uploaded_file_path, matrix)

    os.remove(uploaded_file_path)

    json_res = jsonify(
        {'dirname': timestamp, 'files': os.listdir(app.config['UPLOAD_FOLDER'] + timestamp)})
    json_res.status_code = HTTPStatus.CREATED
    return json_res


if __name__ == '__main__':
    app.run()
