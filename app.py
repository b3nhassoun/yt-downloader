from flask import Flask, render_template, request, url_for, redirect, send_file, session
from pytube import YouTube
from io import BytesIO
from flask import *


app = Flask(__name__)
app.config['SECRET_KEY'] = "dUE7dyqrVh"

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        session['link'] = request.form.get('yt_url')
        try:
            url = YouTube(session['link'])
            url.check_availability()
        except:
            return render_template("error.html")
        return render_template("download.html", url = url)
    return render_template("index.html")


@app.route("/download" , methods = ["GET", "POST"])
def download():
    if request.method == "POST":
        buffer = BytesIO()
        url = YouTube(session['link'])
        itag = request.form.get("itag")
        video = url.streams.get_by_itag(itag)
        video.stream_to_buffer(buffer)
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name="Video - YTVD.mp4", mimetype="video/mp4")
    return redirect(url_for("home"))



if __name__ == "__main__":
    app.run(port=5050, debug=True)