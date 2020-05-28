from flask import Flask, request, Response, render_template, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MVP-no-CSRF-Prot'
@app.route('/', methods=['GET', 'POST'])
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
            return redirect(request.url)
        if file:
            pass

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''