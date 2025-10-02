# Imports do Flask para criação da aplicação web
from flask import Flask, render_template, redirect, url_for, request
# Imports das funções de banco de dados personalizadas
from bd import init_db, validar_usuario, buscar_produtos, buscar_produto_por_nome, buscar_produto_por_id, cadastrar_produto, deletar_produto, atualizacao_produto, movimentacao_estoque

# Criação da instância principal do Flask
app = Flask(__name__)
# Inicialização da configuração do banco de dados MySQL
init_db(app)

# SESSÃO GLOBAL: Armazena dados do usuário logado
usuario_logado = None

# ROTA PRINCIPAL: Página de login do sistema
@app.route("/")
@app.route("/main")
def main():
    """Exibe a página inicial de login"""
    return render_template("index.html", mensagem=None)


# AUTENTICAÇÃO: Processa dados do formulário de login  
@app.route("/login", methods=["POST"])
def login():
    """Valida credenciais e inicia sessão do usuário"""
    # Extrai dados do formulário HTML
    usuario = request.form.get("usuario")
    senha = request.form.get("senha")

    # Acessa variável global de sessão
    global usuario_logado
    # Valida credenciais no banco de dados
    usuario_logado = validar_usuario(usuario, senha)

    if usuario_logado == None:
        # Credenciais inválidas: retorna à tela de login com erro
        return render_template("index.html", mensagem="Usuário ou senha inválidos!")
    else:
        # Login bem-sucedido: redireciona para página principal
        return redirect(url_for('home'))
    
# LOGOUT: Encerra a sessão do usuário
@app.route("/logout")
def logout():
    """Limpa a sessão e retorna à tela de login"""
    global usuario_logado
    usuario_logado = None  # Remove dados da sessão
    return redirect(url_for('main'))
    
# PÁGINA PRINCIPAL: Dashboard após login
@app.route("/home")
def home():
    """Página principal do sistema - requer autenticação"""
    # MIDDLEWARE DE AUTENTICAÇÃO: Verifica se usuário está logado
    if usuario_logado:
        # Usuário autenticado: exibe dashboard com nome personalizado
        return render_template("home.html", nome=usuario_logado['nome'])
    else:
        # Usuário não autenticado: redireciona para login
        return redirect(url_for('main'))

# LISTAGEM DE PRODUTOS: Exibe todos os produtos com opção de busca
@app.route("/cadastro_produto", methods=["GET", "POST"])
def cadastro_produto():
    """Lista produtos com funcionalidade de busca por nome"""
    if usuario_logado:
        # Captura termo de pesquisa do formulário (se houver)
        pesquisa = request.form.get("pesquisa", None)

        if pesquisa:
            # Busca filtrada por nome do produto
            produtos = buscar_produto_por_nome(pesquisa)
        else:
            # Busca todos os produtos cadastrados
            produtos = buscar_produtos()

        # Renderiza página com lista de produtos encontrados
        return render_template("cadastro_produto.html", nome=usuario_logado['nome'], produtos=produtos)
    else:
        # Middleware de autenticação
        return redirect(url_for('main'))
    
# DELETE: Remove produto do sistema
@app.route("/delete_produto/<int:produto_id>")
def delete_produto(produto_id):
    """Exclui produto pelo ID - OPERAÇÃO IRREVERSÍVEL"""
    if usuario_logado:
        # Executa exclusão do produto no banco de dados
        # CASCADE remove automaticamente movimentações relacionadas
        resultado = deletar_produto(produto_id)
        
        # Log do resultado da operação para debug
        if resultado:
            print(f"Produto ID {produto_id} deletado com sucesso")
        else:
            print(f"Erro ao deletar produto ID {produto_id}")
            
        return redirect(url_for('cadastro_produto'))
    else:
        return redirect(url_for('main'))

# EDIÇÃO: Carrega formulário de edição com dados atuais
@app.route("/editar_produto/<int:produto_id>")
def editar_produto(produto_id):
    """Exibe formulário de edição preenchido com dados do produto"""
    if usuario_logado:
        # Busca dados atuais do produto no banco
        produto = buscar_produto_por_id(produto_id)
        
        if produto:
            # Produto encontrado: carrega formulário de edição
            return render_template("editar_produto.html", nome=usuario_logado['nome'], produto=produto)
        else:
            # Produto não encontrado: volta para listagem
            return redirect(url_for('cadastro_produto'))
    else:
        return redirect(url_for('main'))
    
# UPDATE: Processa dados do formulário de edição
@app.route("/atualizar_produto/<int:produto_id>", methods=["POST"])
def atualizar_produto(produto_id):
    """Atualiza dados do produto com informações do formulário"""
    if usuario_logado:
        # Extrai todos os campos do formulário de edição
        codigo = request.form.get("codigo")
        codigo_alternativo = request.form.get("codigo_alternativo")
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        categoria = request.form.get("categoria")
        unidade_medida = request.form.get("unidade_medida")
        preco = request.form.get("preco", "0")  # Default "0" se campo vazio
        estoque_minimo = request.form.get("estoque_minimo")
        aplicacao_veicular = request.form.get("aplicacao_veicular")

        # Chama função do banco para atualizar o produto
        # IMPORTANTE: Converte preço para float antes de salvar
        atualizacao_produto(codigo, codigo_alternativo, nome, descricao, categoria, 
                          unidade_medida, float(preco), estoque_minimo, aplicacao_veicular, produto_id)

        # Retorna para listagem após atualização
        return redirect(url_for('cadastro_produto'))
    else:
        return redirect(url_for('main'))

# FORMULÁRIO: Exibe tela de cadastro de novo produto
@app.route("/novo_produto")
def novo_produto():
    """Carrega formulário em branco para cadastro de produto"""
    if usuario_logado:
        return render_template("novo_produto.html", nome=usuario_logado['nome'])
    else:
        return redirect(url_for('main'))
    
# CREATE: Processa dados do formulário de novo produto
@app.route("/salvar_produto", methods=["POST"])
def salvar_produto():
    """Cadastra novo produto no sistema"""
    if usuario_logado:
        # Extrai dados do formulário de cadastro
        codigo = request.form.get("codigo")
        codigo_alternativo = request.form.get("codigo_alternativo")
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        categoria = request.form.get("categoria")
        unidade_medida = request.form.get("unidade_medida")
        preco = request.form.get("preco", "0")
        estoque_minimo = request.form.get("estoque_minimo")
        aplicacao_veicular = request.form.get("aplicacao_veicular")

        # Cadastra produto no banco com estoque inicial = 0
        # IMPORTANTE: Estoque atual inicia zerado, use movimentação para adicionar
        cadastrar_produto(codigo, codigo_alternativo, nome, descricao, categoria, 
                        unidade_medida, float(preco), estoque_minimo, 0, aplicacao_veicular)

        # Redireciona para listagem após cadastro
        return redirect(url_for('cadastro_produto'))
    else:
        return redirect(url_for('main'))


# GESTÃO DE ESTOQUE: Interface para movimentação de produtos
@app.route("/gestao_estoque")
def gestao_estoque():
    """Exibe lista de produtos com controles de entrada/saída de estoque"""
    if usuario_logado:
        # Busca todos os produtos do sistema
        produtos = buscar_produtos()

        # ORDENAÇÃO: Organiza produtos por nome em ordem alfabética
        # lambda x: x[3].lower() -> x[3] é o campo 'nome' na tupla do produto
        produtos = sorted(produtos, key=lambda x: x[3].lower())

        # Renderiza interface com alertas visuais de estoque baixo
        return render_template("gestao_estoque.html", nome=usuario_logado['nome'], produtos=produtos)
    else:
        return redirect(url_for('main'))

# MOVIMENTAÇÃO: Processa entrada ou saída de estoque
@app.route("/movimentar_estoque/<int:produto_id>", methods=["POST"])
def movimentar_estoque(produto_id):
    """Executa movimentação de estoque (entrada/saída) e registra histórico"""
    if usuario_logado:
        # Extrai dados do formulário de movimentação
        quantidade = request.form.get("quantidade_produto")
        tipo_movimento = request.form.get("tipo_movimento")  # 'entrada' ou 'saida'

        # Executa movimentação no banco de dados
        # IMPORTANTE: Função valida estoque suficiente para saídas
        # Registra movimento na tabela de auditoria
        movimentacao_estoque(produto_id, int(quantidade), tipo_movimento, usuario_logado['id'])

        # Retorna para interface de gestão com dados atualizados
        return redirect(url_for('gestao_estoque'))
    else:
        return redirect(url_for('main'))

# INICIALIZAÇÃO: Executa aplicação Flask apenas se arquivo for executado diretamente
if __name__ == "__main__":
    # Modo DEBUG ativado para desenvolvimento
    app.run(debug=True)
