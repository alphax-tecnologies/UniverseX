from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for
from functools import wraps
from urllib.parse import quote
import json
import yt_dlp
import os

app = Flask(__name__)

MUSICS_DIR = os.path.join(app.root_path, "musics")
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".ogg", ".opus", ".webm", ".flac"}


def nome_bonito(filename: str) -> str:
    base = os.path.splitext(filename)[0].replace("_", " ")
    palavras = base.split()
    return " ".join(p[:1].upper() + p[1:] for p in palavras)


def listar_musicas():
    if not os.path.isdir(MUSICS_DIR):
        return None
    arquivos = [
        f for f in os.listdir(MUSICS_DIR)
        if os.path.isfile(os.path.join(MUSICS_DIR, f))
        and os.path.splitext(f)[1].lower() in AUDIO_EXTS
    ]
    arquivos.sort(key=str.lower)
    return [
        {"music_name": nome_bonito(f), "src": "/musics/" + quote(f)}
        for f in arquivos
    ]

def verify_user(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with open("data.json", mode="r", encoding="utf-8") as arq:
            data = json.load(arq)
            name = data.get("user", "User")

        if name.lower() == "user":
            return redirect(url_for("setup"))

        return f(*args, **kwargs)
    return wrapper

@app.route("/musics/<path:filename>")
def musics(filename):
    return send_from_directory(MUSICS_DIR, filename)


@app.route("/", methods=["GET"])
@verify_user
def home():
    with open("data.json", mode="r", encoding="utf-8") as arq:
        data = json.load(arq)
        name = data.get("user", "User")
        color = data.get("color_app", None)

    payload = {
        "name": str(name),
        "color": color,
        "data": listar_musicas(),
    }
    return render_template("system/home.html", payload=payload)

@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "GET":
        with open("data.json", mode="r", encoding="utf-8") as arq:
            data = json.load(arq)
            name = data.get("user", "User")

        if name.lower() != "user":
            return redirect(url_for("home"))

        return render_template("system/setup.html")

    elif request.method == "POST":
        new_name = request.form.get("name").strip()
        new_color = request.form.get("appcolor").strip()
        with open("data.json", mode="r", encoding="utf-8") as arq:
            data = json.load(arq)

        data["user"] = new_name
        data["color_app"] = "#" + str(new_color)

        with open("data.json", mode="w+", encoding="utf-8") as arq:
            json.dump(data, arq, indent=4, ensure_ascii=False)

        return redirect(url_for("home"))

@app.route("/search", methods=["GET"])
@verify_user
def search():
    with open("data.json", mode="r", encoding="utf-8") as arq:
        data = json.load(arq)
        name = data.get("user", "User")
        color = data.get("color_app", None)
        
    payload = {
        "name":name,
        "color":color,
        "data":listar_musicas()
    }

    return render_template("system/search.html", payload=payload)

@app.route("/settings", methods=["GET", "POST"])
@verify_user
def settings():
    if request.method == "GET":
        with open("data.json", mode="r", encoding="utf-8") as arq:
            data = json.load(arq)
        payload = {
            "name":data["user"],
            "color":data["color_app"]
        }
        return render_template("system/settings.html", payload=payload)
    
    elif request.method == "POST":
        new_name = request.form.get("name")
        new_color = request.form.get("colorapp")
        with open("data.json", mode="r", encoding="utf-8") as arq:
            data = json.load(arq)
        data["user"] = new_name
        data["color_app"] = "#" + new_color if not "#" in str(new_color) else new_color

        with open("data.json", mode="w+", encoding="utf-8") as arq:
            json.dump(data, arq, ensure_ascii=False, indent=4)

        return redirect(url_for("home"))
            

        
@app.route("/download", methods=["POST"])
def download():
    url = (request.get_json(silent=True) or {}).get("url", "")
    opts = {
        "format": "bestaudio/best",
        "outtmpl": "musics/%(title)s.%(ext)s",
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3"}],
        "noplaylist": True,
    }
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
        return jsonify(message=f"“{info['title']}” baixada!",
                       download_url=f"/musics/{info['title']}.mp3")
    except Exception:
        return jsonify(error="Não consegui baixar esse vídeo."), 400

@app.errorhandler(404)
def not_found(error):
    with open("data.json", mode="r", encoding="utf-8") as arq:
        data = json.load(arq)

    payload = {
        "name":data["user"],
        "color":data["color_app"]
    }

    return render_template("system/error404.html", payload=payload)


if __name__ == "__main__":
    print("[ LOG ] Spotify Free Ativado! Acesse: http://127.0.0.1:8888")
    app.run(host="0.0.0.0", port=8888, debug=False)