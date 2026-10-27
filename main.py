from flask import Flask, render_template, jsonify, request, send_from_directory
from urllib.parse import quote
import json
import yt_dlp
import static_ffmpeg
import os

app = Flask(__name__)

MUSICS_DIR = os.path.join(app.root_path, "musics")
AUDIO_EXTS = {".mp3", ".m4a", ".wav", ".ogg", ".opus", ".webm", ".flac"}


def nome_bonito(filename: str) -> str:
    """'montagem_tenta.mp3' -> 'Montagem Tenta'"""
    base = os.path.splitext(filename)[0].replace("_", " ")
    palavras = base.split()
    # põe só a 1ª letra de cada palavra em maiúscula (não mexe no resto, ex.: "DJ")
    return " ".join(p[:1].upper() + p[1:] for p in palavras)


def listar_musicas():
    """Retorna a lista de músicas da pasta, ou None se a pasta não existir."""
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


@app.route("/musics/<path:filename>")
def musics(filename):
    return send_from_directory(MUSICS_DIR, filename)


@app.route("/", methods=["GET"])
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

@app.route("/search", methods=["GET"])
def search():
    return "Nada"

static_ffmpeg.add_paths()
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888, debug=True)