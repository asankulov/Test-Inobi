from functools import wraps
from flask import request, jsonify
from http import HTTPStatus

ALLOWED_MIMETYPES = {'image/png', 'image/jpeg'}


def fields_required_for_download(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        json_data = request.json
        if 'file_path' not in json_data:
            json_res = jsonify({'message': "file_path field isn't provided!"})
            json_res.status_code = HTTPStatus.BAD_REQUEST
            return json_res
        return f(json_data['file_path'], *args, **kwargs)
    return decorated


def fields_required_for_upload(f):
    @wraps(f)
    def decorated(matrix, *args, **kwargs):
        if 'image' not in request.files:
            json_res = jsonify({'message': "image field isn't provided!"})
            json_res.status_code = HTTPStatus.BAD_REQUEST
            return json_res
        return f(matrix, request.files['image'], *args, **kwargs)
    return decorated


def allowed_mimetypes(f):
    @wraps(f)
    def decorated(matrix, file, *args, **kwargs):
        if file.mimetype not in ALLOWED_MIMETYPES:
            json_res = jsonify({'message': "incorrect file format!"})
            json_res.status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            return json_res
        return f(matrix, file, *args, **kwargs)
    return decorated
