from flask import Flask, Response, request, redirect, flash, render_template, url_for
from openpyxl.writer.excel import save_virtual_workbook

import lib.Automation as Automation

EXCEL_MIMETYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.secret_key = 'thatsagoodasecret'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def build_filename():
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    return date_str + "_Kids_Sheet.xlsx"


@app.route('/', methods=['GET'])
def show_form():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    redirect_response = redirect(request.url)
    if 'file' not in request.files:
        flash('No file provided')
        return redirect_response

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect_response

    if not allowed_file(file.filename):
        flash('File type not supported. Please provide a PDF.')
        return redirect_response

    wb = Automation.format_pdf_to_excel(file)
    return Response(save_virtual_workbook(wb),
                    mimetype=EXCEL_MIMETYPE,
                    headers={"Content-Disposition": "attachment;filename=" + build_filename()})
