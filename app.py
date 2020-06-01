import wave
from json import dumps

from flask import Flask, request, flash, send_file

from dbhandler import searchformatches, insertmatch
from wavprocessor import processfile, savetotemp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MVP-no-CSRF-Prot'
@app.route('/post', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if len(request.files)==0:
            return 'No file given'
        file = request.files[list(request.files.keys())[0]]
        # if user does not select file, browser also
        # submit a empty part without filename
        name = file.filename
        if file.filename == '':
            flash('No selected file')
            return "No file was given!"
        if file:
            try:
                with open("tempfile.wav", "wb") as tmp:
                    tmp.write(file.read())
                with wave.open("tempfile.wav", "rb") as f:
                    filedict = processfile(f)
                filedict["filename"] = name
                if filedict["seconds"] == -1:
                    return ("File content invalid, not inserted")
                insertmatch(filedict)
                return ("{} successfully added".format(str(name)))
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
        for item in results:
            savetotemp(item)
            return send_file("test1.wav", as_attachment=True, attachment_filename=item["filename"])
    except Exception as e:
        return str(e)


