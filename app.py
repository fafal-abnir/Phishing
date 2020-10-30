from flask import Flask, request, render_template,jsonify
import logging
from concurrent.futures import ThreadPoolExecutor

Nonephishing_list = ['google.com', 'facebook.com', 'twitter.com']
phishing_list = ['gooogle.com', 'facebbook.com', 'twitter.com']
app = Flask(__name__)


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s: line number:%(lineno)d')

file_handler = logging.FileHandler('panoptes.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class InvalidURL:
    def __init__(self, message):
        self.message = message

    def logging(self):
        logger.warning("This URL is Invalid {}".format(self.message))

class InternalServer(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


app.config["DEBUG"] = True


@app.route('/')
def my_form():
    return render_template('page.html')


@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    text = text.lower()
    try:
        if text in Nonephishing_list:
            return jsonify("this URl is not Phishing")
        elif text in phishing_list:
            return jsonify("Zane hamid Jendast!!!")
        else:
            log = InvalidURL(text)
            log.logging()
            return jsonify("This url is invalid")
    except Exception as err:
        logger.exception(err)
        raise InternalServer("Internal Server Error", status_code=500)
