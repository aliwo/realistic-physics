import os

from flask import Flask, request, json, Response
from config import IMAGE_DIR, ALLOWED_EXTENSIONS
from werkzeug.utils import secure_filename


app = Flask(__name__)
from flask_api import status


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def return_json(jsonifiable):
    return Response(json.dumps(jsonifiable), status=status.HTTP_400_BAD_REQUEST, mimetype='application/json; charset=utf-8')


@app.route('/', methods=['POST'])
def upload_image():

    if 'image' not in request.files:
        return return_json({'msg': 'No File'})

    image_file = request.files.get('image')

    if not allowed_file(image_file.filename):
        return return_json({'msg':'file format not allowed'})
    secured_file_name = secure_filename(image_file.filename)
    image_file.save(os.path.join(IMAGE_DIR, secured_file_name))

    return return_json({'result': True, 'filename':secured_file_name})


if __name__ == '__main__':
    app.run()
