from colorextract import ColorExtract
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed
import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}
app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = os.urandom(32)


class Upload(FlaskForm):
    file = FileField('Upload File', validators=[FileRequired(), FileAllowed(ALLOWED_EXTENSIONS)])
    colors = IntegerField('Number of Colors',
                          validators=[DataRequired(), NumberRange(1, 20, message='Input a number between 1~20')])
    submit = SubmitField('Extract')

colors = ColorExtract(file='static/5a6fa5908188f.jpg', color_number=10).colors_hex

@app.route('/', methods=['post', 'get'])
def home():
    form = Upload()
    file = '5a6fa5908188f.jpg'
    colors_number = 6
    if form.validate_on_submit():
        f = form.file.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static/upload', filename))
        colors_number = form.colors.data
        file = f'upload/{filename}'

    color_extract = ColorExtract(file=f"./static/{file}", color_number=colors_number)
    colors = color_extract.colors_hex
    percent = color_extract.percentage
    return render_template('index.html', form=form, colors=colors, filename=file, percent=percent)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
