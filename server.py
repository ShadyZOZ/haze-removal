import hashlib
import os
import time

from flask import (Flask, abort, jsonify, render_template, request,
                   send_from_directory, url_for)
from PIL import Image
from werkzeug.utils import secure_filename

from haze_removal import HazeRemovel
from utils import threshold_color_array

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file_data']
    image_key = hashlib.md5(f.read()).hexdigest()
    f.seek(0)
    image_ext = f.filename.split('.')[1]
    image_name = secure_filename('{}.{}'.format(image_key, image_ext))
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_name)
    if not os.path.isfile(image_path):
        f.save(image_path)
        print('image saved')
    return jsonify({'url': url_for('result', image=image_name)})


@app.route('/result/<image>')
def result(image):
    try:
        start_time = time.time()
        image_path = os.path.join('./', app.config['UPLOAD_FOLDER'], image)
        haze_removal = HazeRemovel(image=image_path)
        t1 = time.time()
        dark_channel = haze_removal.get_dark_channel(haze_removal.I)
        t2 = time.time()
        A = haze_removal.get_atmosphere(dark_channel)
        t3 = time.time()
        t = haze_removal.get_transmission(dark_channel, A)
        t4 = time.time()
        recover_image = haze_removal.get_recover_image(A, t)
        t5 = time.time()
        _save_image(dark_channel, image, 'dark')
        _save_image(t * 255, image, 't', True)
        _save_image(recover_image, image, 'res', True)
        end_time = time.time()
        ctx = {
            'image_org': _image_url(image, 'org'),
            'image_dark': _image_url(image, 'dark'),
            'image_t': _image_url(image, 't'),
            'image_recover': _image_url(image, 'res'),
            'atmosphere': A,
            'total_time': end_time - start_time,
            'real_time': t5 - t1,
            'dark_time': t2 - t1,
            'a_time': t3 - t2,
            't_time': t4 - t3,
            'res_time': t5 - t4,
        }
        return render_template('result.html', **ctx)
    except FileNotFoundError as e:
        abort(403)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def _image_url(image, image_type):
    if image_type != 'org':
        image = '{}_{}'.format(image_type, image)
    return '/{}/{}'.format(app.config['UPLOAD_FOLDER'], image)


def _save_image(image, image_name, image_type, threshold=False):
    if threshold:
        image = threshold_color_array(image)
    image = Image.fromarray(image)
    image.save('{}/{}_{}'.format(
        app.config['UPLOAD_FOLDER'],
        image_type,
        image_name
    ))


if __name__ == '__main__':
    app.run()
