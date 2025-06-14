from flask import Flask, render_template, request, send_file
import os
import requests
from dotenv import load_dotenv

# Load API credentials from config.env
load_dotenv("config.env")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    uploaded_file = request.files["file"]
    text = uploaded_file.read().decode("utf-8")
    to_lang = request.form["lang"]

    url = f"{os.environ['TRANSLATOR_ENDPOINT']}/translate?api-version=3.0&to={to_lang}"
    headers = {
        "Ocp-Apim-Subscription-Key": os.environ["TRANSLATOR_KEY"],
        "Ocp-Apim-Subscription-Region": os.environ["TRANSLATOR_REGION"],
        "Content-Type": "application/json"
    }
    body = [{"text": text}]

    try:
        res = requests.post(url, headers=headers, json=body)
        res.raise_for_status()
        translated = res.json()[0]["translations"][0]["text"]

        with open("translated.txt", "w", encoding="utf-8") as f:
            f.write(translated)

        return send_file("translated.txt", as_attachment=True, download_name="translated.txt")

    except Exception as e:
        return f"❌ Error: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
