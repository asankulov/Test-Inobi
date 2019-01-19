from PIL import Image
import os
from time import time
from zipfile import ZipFile, ZIP_DEFLATED


def chop_image_from_path(file_path, matrix):
    dirname, file_extension = os.path.splitext(file_path)
    os.mkdir(dirname)

    image = Image.open(file_path)
    horizontal_ratio, vertical_ratio = [int(ratio) for ratio in matrix.split('x')]
    new_width, new_height = image.width // horizontal_ratio, image.height // vertical_ratio

    for i in range(vertical_ratio):
        upper = i * new_height
        lower = (i + 1) * new_height
        for j in range(horizontal_ratio):
            left = j * new_width
            right = (j + 1) * new_width
            new_file_path = os.path.join(dirname, str(j + horizontal_ratio * i + 1) + file_extension)
            image.crop((left, upper, right, lower)).save(new_file_path)


def join_uploads_dir_with_filename(path, ext):
    timestamp = str(time()).replace('.', '')
    return os.path.join(path, "{}{}".format(timestamp, ext)), timestamp


def create_zip(dirname):
    zip_file_name = dirname + '.zip'
    zip_file = ZipFile(zip_file_name, 'w', ZIP_DEFLATED)
    os.chdir(dirname)
    for root, dirs, files in os.walk('./'):
        for file in files:
            zip_file.write(file)
    zip_file.close()
    os.chdir('../')
    return zip_file_name
