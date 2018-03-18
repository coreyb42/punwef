from hashlib import md5
import time

from flask import Flask, jsonify, request, send_file, abort
from redis import Redis
from simulators import *

app = Flask(__name__)
redis = Redis(host='redis', port=6379)

image_directory = 'output_images'


@app.route('/details')
def details():
    target_url = request.args.get('url', '')
    file_path, _, _, source = take_screenshot(target_url)
    response = jsonify({'target_url': target_url, 'filename': file_path.split('/')[-1], 'source_html': source})
    return response


@app.route('/retrieve')
def retrieve():
    filename = request.args.get('filename', '')
    file_path = os.path.abspath(os.path.join(image_directory, filename))
    try:
        response = send_file(file_path, mimetype='image/png')
    except IOError:
        abort(404)
    os.remove(file_path)
    return response


@app.route('/')
def default_behavior():
    target_url = request.args.get('url', '')
    file_path, _, _, _ = take_screenshot(target_url)
    response = send_file(file_path, mimetype='image/png')
    os.remove(file_path)
    return response


def take_screenshot(target_url):
    filename = md5(target_url.encode('utf8', 'replace')).hexdigest() + '-' + str(int(time.time())) + '.png'
    return get_screen_shot(url=target_url, filename=filename, path=image_directory)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5001)
