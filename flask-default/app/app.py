from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/uploads/"


@app.route("/")
def upload_form():
    return render_template("form.html")


@app.route("/upload", methods=["POST"])
def upload_test_file():
    print(request.files)
    f = request.files["uploadFile"]
    filename = secure_filename(f.filename)
    # f.save(secure_filename(f.filename))
    print(filename)

    f.save(app.config["UPLOAD_FOLDER"] + filename)

    try:
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
