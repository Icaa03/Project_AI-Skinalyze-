from flask import Flask, request, render_template
import google.generativeai as genai
from PIL import Image
import markdown
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "upload"

genai.configure(api_key="AIzaSyAyKJh70O3qPYHYN-l94CXyIqBhNglV2sU")  
model = genai.GenerativeModel("gemini-2.0-flash")  

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    reply = ""
    jenis_kulit = request.form["jenis_kulit"]
    masalah_kulit = request.form["masalah_kulit"]
    budget = request.form["budget"]
    file = request.files["foto"]

    if file.filename != "":
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        file.save(filepath)

        img = Image.open(filepath)

        prompt = f"""
        Saya memiliki kulit {jenis_kulit} dan mengalami masalah {masalah_kulit}.
        Budget saya untuk skincare adalah {budget}.
        Berdasarkan foto wajah yang saya unggah, tolong rekomendasikan produk skincare yang cocok
        beserta komposisi bahan yang direkomendasikan. Jika memungkinkan, sertakan nama dan gambar produk.
        Jelaskan alasannya juga secara singkat.
        """

        response = model.generate_content([prompt, img])
        reply_raw = response.text
        reply = markdown.markdown(reply_raw)

    return render_template("index.html", reply=reply)

if __name__ == "main":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
