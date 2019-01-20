from functools import wraps
from flask import request, jsonify
from http import HTTPStatus
from utils import join_uploads_dir_with_filename
import mimetypes

ALLOWED_MIMETYPES = {'image/png', 'image/jpeg'}


def fields_required_for_upload(func):
    @wraps(func)
    def decorated(matrix, *args, **kwargs):
        if 'image' not in request.files:
            json_res = jsonify({'message': "image field isn't provided!"})
            json_res.status_code = HTTPStatus.BAD_REQUEST
            return json_res
        return func(matrix, request.files['image'], *args, **kwargs)

    return decorated


def save_file_and_get_file_path(func):
    @wraps(func)
    def decorated(matrix, file, *args, **kwargs):
        uploaded_file_path, timestamp = join_uploads_dir_with_filename('uploads/',
                                                                       mimetypes.guess_all_extensions(file.mimetype)[
                                                                           -1])
        file.save(uploaded_file_path)
        return func(matrix, uploaded_file_path, timestamp, *args, **kwargs)
    return decorated


def allowed_mimetypes(func):
    @wraps(func)
    def decorated(matrix, file, *args, **kwargs):
        if file.mimetype not in ALLOWED_MIMETYPES:
            json_res = jsonify({'message': "incorrect file format!"})
            json_res.status_code = HTTPStatus.UNSUPPORTED_MEDIA_TYPE
            return json_res
        return func(matrix, file, *args, **kwargs)

    return decorated
