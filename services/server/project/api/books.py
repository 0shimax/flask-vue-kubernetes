import os
import pandas as pd

from flask import Flask, render_template
from flask import Blueprint, jsonify, request
from werkzeug import secure_filename

from project.api.models import Book
# from project import db


books_blueprint = Blueprint('books', __name__)
app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
ALLOWED_EXTENSIONS = ['csv', 'tsv']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@books_blueprint.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {
        'status': 'success',
        'container_id': os.uname()[1]
    }
    if request.method == 'POST':
        post_data = request.get_json()
        title = post_data.get('title')
        author = post_data.get('author')
        read = post_data.get('read')
        db.session.add(Book(title=title, author=author, read=read))
        db.session.commit()
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = [book.to_json() for book in Book.query.all()]
    return jsonify(response_object)


@books_blueprint.route('/books/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'pong!',
        'container_id': os.uname()[1]
    })


@books_blueprint.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {
      'status': 'success',
      'container_id': os.uname()[1]
    }
    book = Book.query.filter_by(id=book_id).first()
    if request.method == 'PUT':
        post_data = request.get_json()
        book.title = post_data.get('title')
        book.author = post_data.get('author')
        book.read = post_data.get('read')
        db.session.commit()
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        db.session.delete(book)
        db.session.commit()
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


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
            img_path = os.path.join(file_path, 'pd_image.png')
            plt.savefig(img_path)
            plt.close()

            img_fname = ''.join(img_path.split()[2:])
            img_url = '/uploads/' + img_fname
            return render_template('index.html', img_url=img_url)
        else:
            return " <p>許可されていない拡張子です</p> "
    else:
        return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    app.run()
