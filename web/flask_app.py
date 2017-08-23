from flask import Flask, request, redirect, flash, render_template, request, url_for

ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.secret_key = 'thatsagoodasecret'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def show_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if not allowed_file(file.filename):
        flash('File type not supported. Please provide a PDF.')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        flash('Got file: ' + file.filename)
        return redirect(request.url)