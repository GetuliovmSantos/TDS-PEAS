from flask import Flask, render_template, redirect, url_for, request
from bd import init_db, validar_usuario, buscar_produtos, buscar_produtos_por_nome, cadastrar_produto

app = Flask(__name__)
init_db(app)

usuario_logado = None

@app.route("/")
@app.route("/main")
def main():
    return render_template("index.html", mensagem=None)


@app.route("/login", methods=["POST"])
def login():
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")


    global usuario_logado
    usuario_logado = validar_usuario(usuario, senha)

    if usuario_logado == None:
        return render_template("index.html", mensagem="Usuário ou senha inválidos!")
    else:
        return redirect(url_for('home'))
    
@app.route("/logout")
def logout():
    global usuario_logado
    usuario_logado = None
    return redirect(url_for('main'))
    
@app.route("/home")
def home():
    if usuario_logado:
        return render_template("home.html", nome=usuario_logado['nome'])
    else:
        return redirect(url_for('main'))

@app.route("/cadastro_produto", methods=["GET", "POST"])
def cadastro_produto():
    if usuario_logado:

        pesquisa = request.form.get("pesquisa", None)

        print(pesquisa)

        if pesquisa:
            produtos = buscar_produtos_por_nome(pesquisa)
        else:
            produtos = buscar_produtos()

        return render_template("cadastro_produto.html", nome=usuario_logado['nome'], produtos=produtos)
    else:
        return redirect(url_for('main'))

@app.route("/novo_produto")
def novo_produto():
    if usuario_logado:
        return render_template("novo_produto.html", nome=usuario_logado['nome'])
    else:
        return redirect(url_for('main'))
    
@app.route("/salvar_produto", methods=["POST"])
def salvar_produto():
    if usuario_logado:
        codigo = request.form.get("codigo")
        codigo_alternativo = request.form.get("codigo_alternativo")
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        categoria = request.form.get("categoria")
        unidade_medida = request.form.get("unidade_medida")
        preco = request.form.get("preco", "0")
        estoque_minimo = request.form.get("estoque_minimo")
        aplicacao_veicular = request.form.get("aplicacao_veicular")

        cadastrar_produto(codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, float(preco), estoque_minimo, 0, aplicacao_veicular)

        return redirect(url_for('cadastro_produto'))

    else:
        return redirect(url_for('main'))

if __name__ == "__main__":
    app.run(debug=True)
