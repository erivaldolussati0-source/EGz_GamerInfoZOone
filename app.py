from flask import Flask, render_template, request, redirect, url_for
import os
import json
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Pasta para salvar imagens enviadas pelo admin
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Arquivos JSON para cada categoria
FILES = {
    "Futebol": "jogos_futebol.json",
    "Tiro": "jogos_tiro.json",
    "Aventura": "jogos_aventura.json"
}

# Carregar dados dos arquivos JSON
def load_json(file):
    try:
        with open(file) as f:
            return json.load(f)
    except:
        return []

# Salvar dados nos arquivos JSON
def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f)

# Inicializar dados
jogos = {cat: load_json(f) for cat, f in FILES.items()}


@app.route("/")
def index():
    pesquisa = request.args.get("q", "")
    resultados = []
    for categoria, lista in jogos.items():
        for j in lista:
            if pesquisa.lower() in j["titulo"].lower():
                resultados.append(j)
    return render_template("index.html", jogos=resultados, pesquisa=pesquisa)


@app.route("/<categoria>")
def categoria_page(categoria):
    categoria_cap = categoria.capitalize()
    if categoria_cap not in jogos:
        return "Categoria não encontrada", 404
    pesquisa = request.args.get("q", "")
    lista = jogos[categoria_cap]
    if pesquisa:
        lista = [j for j in lista if pesquisa.lower() in j["titulo"].lower()]
    return render_template(f"{categoria}.html", jogos=lista, categoria=categoria_cap, pesquisa=pesquisa)


@app.route("/egzadmin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        categoria = request.form["categoria"]
        titulo = request.form["titulo"]
        requisitos = request.form["requisitos"]
        imagem_file = request.files["imagem"]

        if imagem_file:
            filename = secure_filename(imagem_file.filename)
            caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            imagem_file.save(caminho)
        else:
            filename = ""

        novo_jogo = {
            "titulo": titulo,
            "imagem": f"/{caminho}" if filename else "",
            "requisitos": requisitos
        }

        jogos[categoria].append(novo_jogo)
        save_json(FILES[categoria], jogos[categoria])

        return redirect(url_for('categoria_page', categoria=categoria.lower()))

    return render_template("admin.html", categorias=list(FILES.keys()))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
