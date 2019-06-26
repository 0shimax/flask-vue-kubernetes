import os
from datetime import datetime
import matplotlib.pyplot as plt

import pandas as pd
from flask import Flask, render_template, send_from_directory
from flask import Blueprint, jsonify, request
from werkzeug import secure_filename


# app = Flask(__name__, template_folder='../templates')

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = ['.csv', '.tsv']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def index():
    contents = {'message': "Hello World!"}
    return render_template("index.html", contents=contents)


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        if csv_file and os.path.splitext(csv_file.filename)[-1] in ALLOWED_EXTENSIONS:
            filename = secure_filename(csv_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            csv_file.save(file_path)
            df = pd.read_csv(file_path)

            plt.figure()
            df.plot()
            img_name = filename
            img_name += datetime.now().strftime('%Y%m%d%H%M%S') + 'pd_image.png'

            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
            plt.savefig(img_path)
            plt.close()

            contents = []
            img_url = '/uploads/' + img_name
            content = {'image_title':'sample' , 'image_path':img_url}
            print(content)
            contents.append(content)
            return render_template('show_images.html', contents=contents)
        else:
            return " <p>許可されていない拡張子です</p> "
    else:
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run(debug=True)
