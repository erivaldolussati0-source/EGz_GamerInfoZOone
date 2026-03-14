from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

futebol = []
aventura = []
tiro = []

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/futebol")
def futebol_page():

    pesquisa = request.args.get("q")

    jogos = futebol

    if pesquisa:
        jogos = [j for j in futebol if pesquisa.lower() in j["titulo"].lower()]

    return render_template("futebol.html", jogos=jogos)


@app.route("/aventura")
def aventura_page():

    pesquisa = request.args.get("q")

    jogos = aventura

    if pesquisa:
        jogos = [j for j in aventura if pesquisa.lower() in j["titulo"].lower()]

    return render_template("aventura.html", jogos=jogos)


@app.route("/tiro")
def tiro_page():

    pesquisa = request.args.get("q")

    jogos = tiro

    if pesquisa:
        jogos = [j for j in tiro if pesquisa.lower() in j["titulo"].lower()]

    return render_template("tiro.html", jogos=jogos)


@app.route("/egzadmin", methods=["GET","POST"])
def admin():

    if request.method == "POST":

        categoria = request.form["categoria"]
        titulo = request.form["titulo"]
        link = request.form["link"]
        requisitos = request.form["requisitos"]

        imagem = request.files["imagem"]

        caminho = os.path.join(app.config["UPLOAD_FOLDER"], imagem.filename)
        imagem.save(caminho)

        jogo = {
            "titulo": titulo,
            "imagem": caminho,
            "link": link,
            "requisitos": requisitos
        }

        if categoria == "Futebol":
            futebol.append(jogo)

        if categoria == "Aventura":
            aventura.append(jogo)

        if categoria == "Tiro":
            tiro.append(jogo)

        return redirect("/")

    return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
