from flask import Flask, render_template, request, redirect, url_for
import os, json
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

FILES = {
    "Futebol": "jogos_futebol.json",
    "Tiro": "jogos_tiro.json",
    "Aventura": "jogos_aventura.json"
}

def load_json(file):
    try:
        with open(file, encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def save_json(file, data):
    with open(file, "w", encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

jogos = {cat: load_json(f) for cat, f in FILES.items()}

@app.route("/")
def index():
    pesquisa = request.args.get("q", "")
    resultados = []
    for categoria, lista in jogos.items():
        for j in lista:
            if pesquisa.lower() in j["titulo"].lower() or not pesquisa:
                resultados.append(j)
    return render_template("index.html", jogos=resultados, pesquisa=pesquisa)

@app.route("/<categoria>")
def categoria_page(categoria):
    categoria_cap = categoria.capitalize()
    if categoria_cap not in jogos:
        return "Categoria não encontrada", 404
    pesquisa = request.args.get("q", "")
    lista = [j for j in jogos[categoria_cap] if pesquisa.lower() in j["titulo"].lower() or not pesquisa]
    return render_template("categoria.html", jogos=lista, categoria=categoria_cap, pesquisa=pesquisa)

@app.route("/egzadmin", methods=["GET","POST"])
def admin():
    if request.method == "POST":
        # Remover jogo
        if "remover" in request.form:
            categoria = request.form["categoria"]
            nome_jogo = request.form["nome_jogo"]
            jogos[categoria] = [j for j in jogos[categoria] if j["titulo"] != nome_jogo]
            save_json(FILES[categoria], jogos[categoria])
            return redirect(url_for('admin'))

        # Adicionar jogo
        categoria = request.form["categoria"]
        titulo = request.form["titulo"]
        requisitos = request.form["requisitos"]

        imagem_file = request.files.get("imagem")
        download_file = request.files.get("download")
        link = request.form.get("link")

        img_filename = secure_filename(imagem_file.filename) if imagem_file and imagem_file.filename else ""
        dl_filename = secure_filename(download_file.filename) if download_file and download_file.filename else ""

        if imagem_file and imagem_file.filename:
            imagem_file.save(os.path.join(app.config['UPLOAD_FOLDER'], img_filename))

        if download_file and download_file.filename:
            download_file.save(os.path.join(app.config['UPLOAD_FOLDER'], dl_filename))

        novo_jogo = {
            "titulo": titulo,
            "imagem": img_filename,
            "download": dl_filename,
            "link": link,
            "requisitos": requisitos
        }

        jogos[categoria].append(novo_jogo)
        save_json(FILES[categoria], jogos[categoria])

        return redirect(url_for('admin'))

    return render_template("admin.html", categorias=list(FILES.keys()), jogos=jogos)

if __name__=="__main__":
    app.run(host="0.0.0.0", port=5000)
