from flask import Flask, request, render_template
from flask import url_for, redirect, render_template
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = "kkkeeeyyy"


class UploadForm(FlaskForm):
    file = FileField()


def get_images_count() -> int:
    with open("static/images/images_count.txt") as file:
        count = int(file.read().strip())

    return count


def add_images_count(count):
    with open("static/images/images_count.txt", "w") as file:
        file.write(str(count + 1))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        images_count = get_images_count()
        form.file.data.save(f'static/images/mars_image_{images_count + 1}.jpg')
        add_images_count(images_count)
        return redirect(url_for('index'))

    params = dict()
    params["pictures"] = list()
    params["form"] = form
    for num in range(1, get_images_count() + 1):
        params["pictures"].append(f"static/images/mars_image_{num}.jpg")
    return render_template('index.html', **params)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
