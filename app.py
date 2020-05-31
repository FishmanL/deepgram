from flask import Flask, request, Response, render_template, flash, redirect, send_file
from wavprocessor import processfile, savetotemp
from dbhandler import searchformatches, insertmatch
from json import dumps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MVP-no-CSRF-Prot'
@app.route('/post', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        name = file.filename
        if file.filename == '':
            flash('No selected file')
            return "No file was given!"
        if file:
            try:
                filedict = processfile(file)
                filedict["filename"] = name
                insertmatch(filedict)
                return("{} successfully added".format(name))
            except Exception as e:
                return str(e)




@app.route('/list', methods=['GET'])
def list_files():
    try:
        results = searchformatches(request.args.to_dict())
        return dumps([item["filename"] for item in results])
    except Exception as e:
        return str(e)

@app.route('/info', methods=['GET'])
def info_files():
    try:
        results = searchformatches(request.args.to_dict())
        items = [{key: value for key, value in result.items() if key != 'content'} for result in results]
        return dumps(items)

    except Exception as e:
        return str(e)

@app.route('/download', methods=['GET'])
def download_files():
    try:
        results = searchformatches(request.args.to_dict())
        lst = []
        for item in results:
            savetotemp(item)
            return send_file("test1.wav", as_attachment=True, attachment_filename=item["filename"])
    except Exception as e:
        return str(e)


