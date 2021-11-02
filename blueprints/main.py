#!/usr/bin/env python3

from time import time
from os import path, remove
from flask import Blueprint, request, redirect, url_for, flash
from flask.templating import render_template
from werkzeug.utils import secure_filename
from analyzer.analyze import Loglevel, analyze_logfile
from config import ANALYZER_CFG

main_handlers = Blueprint('main_handlers', __name__)

ALLOWED_EXTS = ANALYZER_CFG.get('allowed_extensions', [])
ALLOWED_FILETYPES = ','.join([f'.{ext}' for ext in ALLOWED_EXTS])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS


@main_handlers.route('/', methods=['POST', 'GET'])
def landing():
    if request.method == 'GET':
        return render_template('index.html', supported_filetypes=ALLOWED_FILETYPES)

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect('/')

    if file and allowed_file(file.filename):
        filename = path.join('data', secure_filename(
            f'{round(time())}_{file.filename}'))

        file.save(filename)
        with open(filename, 'r', encoding='utf-8') as f:
            # print(f.read())

            analyze_logfile(f, Loglevel.DEBUG)

        remove(filename)
        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return "yay"
