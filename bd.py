from flaskext.mysql import MySQL

# Instância global do MySQL para Flask - reutilizada em todas as operações
mysql = MySQL()

def init_db(app):
    """
    Inicializa a configuração do banco de dados MySQL
    Esta função deve ser chamada uma vez na inicialização da aplicação Flask
    """
    # Configurações do banco de dados - definidas no objeto app do Flask
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'        # Servidor local MySQL
    app.config['MYSQL_DATABASE_USER'] = 'root'             # Usuário do banco
    app.config['MYSQL_DATABASE_PASSWORD'] = '284637'       # Senha do usuário (altere conforme necessário)
    app.config['MYSQL_DATABASE_DB'] = 'saep_db'            # Nome do banco de dados
    app.config['MYSQL_DATABASE_PORT'] = 3306               # Porta padrão do MySQL
    
    # Vincula a instância MySQL à aplicação Flask
    mysql.init_app(app)

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL
    Retorna None se houver falha na conexão
    """
    try:
        # Estabelece conexão usando as configurações definidas em init_db()
        connection = mysql.connect()
        return connection
    except Exception as e:
        # Log do erro para debug - problemas comuns: senha incorreta, banco não encontrado
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

def close_db_connection(connection):
    """
    Fecha a conexão com o banco de dados de forma segura
    Sempre chame esta função no bloco finally das operações
    """
    if connection:
        connection.close()

# ==========================================
# FUNÇÕES DE USUÁRIO / LOGIN
# ==========================================

def validar_usuario(usuario, senha):
    """
    Valida as credenciais do usuário no sistema
    Retorna um dicionário com dados do usuário se válido, None caso contrário
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        # Busca usuário pelo nome de login (proteção contra SQL injection com %s)
        sql = "SELECT * FROM Usuario WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        user_data = cursor.fetchone()  # Retorna tupla ou None
        
        # Verifica se usuário existe e se a senha confere
        # IMPORTANTE: Em produção, use hash da senha (bcrypt/pbkdf2)
        if user_data and user_data[3] == senha:  # senha é a 4ª coluna (índice 3)
            # Retorna dados estruturados do usuário para sessão
            return {
                'id': user_data[0],      # idUsuario - chave primária
                'nome': user_data[1],    # nome completo do usuário
                'usuario': user_data[2]  # login/username
            }
        return None  # Credenciais inválidas
    
    except Exception as e:
        print(f"Erro ao validar usuário: {e}")
        return None
    
    finally:
        # CRÍTICO: Sempre fechar conexão para evitar memory leak
        close_db_connection(connection)

# ==========================================
# FUNÇÕES DE BUSCA DE PRODUTOS
# ==========================================

def buscar_produtos():
    """
    Busca todos os produtos cadastrados no banco de dados
    Retorna lista de tuplas com dados dos produtos, [] se erro ou vazio
    """
    connection = get_db_connection()
    if not connection:
        return []  # Retorna lista vazia se não conseguir conectar
    
    try:
        cursor = connection.cursor()
        # Seleciona todos os campos de todos os produtos
        sql = "SELECT * FROM Produto"
        cursor.execute(sql)
        produtos = cursor.fetchall()  # Retorna lista de tuplas
        
        # Estrutura da tupla produto (por índice):
        # [0]=idProduto, [1]=codigo, [2]=codigo_alternativo, [3]=nome,
        # [4]=descricao, [5]=categoria, [6]=unidade_medida, [7]=preco,
        # [8]=estoque_minimo, [9]=estoque_atual, [10]=aplicacao_veicular
        return produtos
    
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []  # Lista vazia em caso de erro
    
    finally:
        close_db_connection(connection)

def buscar_produto_por_nome(nome):
    """
    Busca produtos que contenham o nome especificado (busca parcial)
    Usa LIKE para permitir busca por parte do nome
    """
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        # LIKE permite busca parcial - adicione % antes e depois para busca completa
        sql = "SELECT * FROM Produto WHERE nome LIKE %s"
        cursor.execute(sql, (nome,))  # Parâmetro nome deve incluir % se necessário
        produtos = cursor.fetchall()
        return produtos
    
    except Exception as e:
        print(f"Erro ao buscar produto por nome '{nome}': {e}")
        return []
    
    finally:
        close_db_connection(connection)

def buscar_produto_por_id(produto_id):
    """
    Busca um produto específico pelo ID (chave primária)
    Retorna tupla com dados do produto ou None se não encontrado
    """
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        # Busca exata por ID - mais eficiente que busca por nome
        sql = "SELECT * FROM Produto WHERE idProduto = %s"
        cursor.execute(sql, (produto_id,))
        produto = cursor.fetchone()  # Retorna apenas um registro ou None
        return produto
    
    except Exception as e:
        print(f"Erro ao buscar produto por ID {produto_id}: {e}")
        return None
    
    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÕES DE CADASTRO DE PRODUTOS
# ==========================================

def cadastrar_produto(codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, preco, estoque_minimo, estoque_atual, aplicacao_veicular):
    """
    Cadastra um novo produto no sistema
    Returns:
        bool: True se cadastrado com sucesso, False se erro
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        # INSERT com todos os campos da tabela Produto
        # ATENÇÃO: idProduto é AUTO_INCREMENT, não incluir no INSERT
        sql = """
            INSERT INTO Produto (codigo, codigo_alternativo, nome, descricao, categoria, 
                               unidade_medida, preco, estoque_minimo, estoque_atual, aplicacao_veicular)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (codigo, codigo_alternativo, nome, descricao, categoria, 
                           unidade_medida, preco, estoque_minimo, estoque_atual, aplicacao_veicular))
        connection.commit()  # Confirma a inserção no banco
        return True

    except Exception as e:
        print(f"Erro ao cadastrar produto '{nome}': {e}")
        return False

    finally:
        close_db_connection(connection)


# ==========================================
# FUNÇÕES DE DELEÇÃO DE PRODUTOS
# ==========================================   

def deletar_produto(produto_id):
    """
    Remove um produto do sistema pelo ID
    ATENÇÃO: Operação irreversível! 
    Devido ao CASCADE, também remove movimentações relacionadas
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        # DELETE por ID - CASCADE remove movimentações automaticamente
        sql = "DELETE FROM Produto WHERE idProduto = %s"
        cursor.execute(sql, (produto_id,))
        connection.commit()  # Efetiva a remoção
        return True

    except Exception as e:
        print(f"Erro ao deletar produto ID {produto_id}: {e}")
        return False

    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÕES DE ATUALIZAÇÃO DE PRODUTOS
# ==========================================

def atualizacao_produto(codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, preco, estoque_minimo, aplicacao_veicular, produto_id):
    """
    Atualiza os dados de um produto existente
    IMPORTANTE: NÃO atualiza o estoque_atual - use movimentacao_estoque() para isso
    
    Returns:
        bool: True se produto foi encontrado e atualizado, False caso contrário
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        # UPDATE de todos os campos editáveis, EXCETO estoque_atual e idProduto
        sql = """
            UPDATE Produto 
            SET codigo = %s, codigo_alternativo = %s, nome = %s, descricao = %s, 
                categoria = %s, unidade_medida = %s, preco = %s, estoque_minimo = %s, 
                aplicacao_veicular = %s
            WHERE idProduto = %s
        """
        cursor.execute(sql, (codigo, codigo_alternativo, nome, descricao, categoria, 
                           unidade_medida, preco, estoque_minimo, aplicacao_veicular, produto_id))
        connection.commit()
        
        # Verifica se alguma linha foi realmente alterada (produto existe?)
        return cursor.rowcount > 0

    except Exception as e:
        print(f"Erro ao atualizar produto ID {produto_id}: {e}")
        connection.rollback()  # Reverter mudanças em caso de erro
        return False

    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÃO DE MOVIMENTAÇÃO DE ESTOQUE
# ==========================================

def movimentacao_estoque(produto_id, quantidade, tipo_movimentacao, id_usuario):
    """
    Realiza movimentação de estoque (entrada ou saída)
    Atualiza o estoque atual e registra no histórico de movimentações
    
    Args:
        produto_id (int): ID do produto a ser movimentado
        quantidade (int): Quantidade a ser movimentada
        tipo_movimentacao (str): 'entrada' ou 'saida'
        id_usuario (int): ID do usuário que fez a movimentação
    
    Returns:
        bool: True se sucesso, False se erro ou estoque insuficiente
    """
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Define a operação SQL baseada no tipo de movimentação
        if tipo_movimentacao == 'entrada':
            # Entrada: SOMA a quantidade ao estoque atual
            sql_update = "UPDATE Produto SET estoque_atual = estoque_atual + %s WHERE idProduto = %s"
        elif tipo_movimentacao == 'saida':
            # Saída: Primeiro verifica se há estoque suficiente
            quantidade_atual = buscar_produto_por_id(produto_id)[9]  # índice 9 = estoque_atual

            # VALIDAÇÃO CRÍTICA: Impede estoque negativo
            if quantidade > quantidade_atual:
                print(f"Estoque insuficiente. Atual: {quantidade_atual}, Solicitado: {quantidade}")
                return False
            
            # Saída: SUBTRAI a quantidade do estoque atual
            sql_update = "UPDATE Produto SET estoque_atual = estoque_atual - %s WHERE idProduto = %s"
        else:
            # Tipo de movimentação inválido
            print(f"Tipo de movimentação inválido: {tipo_movimentacao}")
            return False

        # Executa a atualização do estoque
        cursor.execute(sql_update, (quantidade, produto_id))

        # AUDITORIA: Registra a movimentação no histórico para rastreabilidade
        sql_insert = """
            INSERT INTO Movimentacao (idProduto, quantidade, tipo_movimentacao, data_movimentacao, idUsuario)
            VALUES (%s, %s, %s, NOW(), %s)
        """
        cursor.execute(sql_insert, (produto_id, quantidade, tipo_movimentacao, id_usuario))

        # TRANSAÇÃO: Confirma ambas as operações (update + insert) atomicamente
        connection.commit()
        return True

    except Exception as e:
        print(f"Erro ao movimentar estoque - Produto ID {produto_id}, Tipo: {tipo_movimentacao}, Quantidade: {quantidade}: {e}")
        # ROLLBACK: Desfaz todas as alterações em caso de erro
        connection.rollback()
        return False

    finally:
        close_db_connection(connection)


# ==========================================
# FUNÇÃO DE TESTE DE CONEXÃO
# ==========================================

def testar_conexao():
    """
    Testa se a conexão com o banco de dados está funcionando
    Útil para diagnóstico de problemas de conectividade
    
    Returns:
        bool: True se conseguiu conectar e desconectar, False caso contrário
    """
    try:
        # Tenta estabelecer conexão
        connection = get_db_connection()
        if connection:
            # Se conectou, fecha imediatamente (apenas teste)
            close_db_connection(connection)
            return True
        else:
            return False  # Falha na conexão
    except Exception as e:
        print(f"Erro ao testar conexão com o banco: {e}")
        return False