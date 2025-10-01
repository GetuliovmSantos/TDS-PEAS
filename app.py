from flask import Flask, render_template, redirect, url_for, request
from bd import init_db, validar_usuario

app = Flask(__name__)
init_db(app)

usuario_logado = None

@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", mensagem=None)


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    print(f"usuario = {usuario} - senha = {senha}")

    global usuario_logado
    usuario_logado = validar_usuario(usuario, senha)

    print(usuario_logado)

    if usuario_logado == None:
        return render_template("index.html", mensagem="Usuário ou senha inválidos!")
    else:
        return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
