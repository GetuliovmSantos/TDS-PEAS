from flaskext.mysql import MySQL

# Instância do MySQL para Flask
mysql = MySQL()

def init_db(app):
    
    # Configurações do banco de dados
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = '284637'  # Altere conforme sua configuração
    app.config['MYSQL_DATABASE_DB'] = 'saep_db'
    app.config['MYSQL_DATABASE_PORT'] = 3306
    
    mysql.init_app(app)

def get_db_connection():
    """
    Cria e retorna uma conexão com o banco de dados MySQL
    """
    try:
        connection = mysql.connect()
        return connection
    except Exception as e:
        print(f"Erro ao conectar com o banco de dados: {e}")
        return None

def close_db_connection(connection):
    if connection:
        connection.close()

# ==========================================
# FUNÇÕES DE USUÁRIO / LOGIN
# ==========================================

def validar_usuario(usuario, senha):
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Usuario WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        user_data = cursor.fetchone()
        
        if user_data and user_data[3] == senha:  # senha é a 4ª coluna (índice 3)
            return {
                'id': user_data[0],      # idUsuario
                'nome': user_data[1],    # nome  
                'usuario': user_data[2]  # usuario
            }
        return None
    
    except Exception as e:
        print(f"Erro ao validar usuário: {e}")
        return None
    
    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÕES DE BUSCA DE PRODUTOS
# ==========================================

def buscar_produtos():
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Produto"
        cursor.execute(sql)
        produtos = cursor.fetchall()

        
        return produtos
    
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []
    
    finally:
        close_db_connection(connection)

def buscar_produto_por_nome(nome):
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Produto WHERE nome LIKE %s"
        cursor.execute(sql, (nome,))
        produtos = cursor.fetchall()
        return produtos
    
    except Exception as e:
        print(f"Erro ao buscar produtos por nome: {e}")
        return []
    
    finally:
        close_db_connection(connection)

def buscar_produto_por_id(produto_id):
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor()
        sql = "SELECT * FROM Produto WHERE idProduto = %s"
        cursor.execute(sql, (produto_id,))
        produto = cursor.fetchone()
        return produto
    
    except Exception as e:
        print(f"Erro ao buscar produto por ID: {e}")
        return None
    
    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÕES DE CADASTRO DE PRODUTOS
# ==========================================

def cadastrar_produto(codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, preco, estoque_minimo, estoque_atual, aplicacao_veicular):
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        sql = """
            INSERT INTO Produto (codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, preco, estoque_minimo, estoque_atual, aplicacao_veicular)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, preco, estoque_minimo, estoque_atual, aplicacao_veicular))
        connection.commit()
        return True

    except Exception as e:
        print(f"Erro ao cadastrar produto: {e}")
        return False

    finally:
        close_db_connection(connection)


# ==========================================
# FUNÇÕES DE DELEÇÃO DE PRODUTOS
# ==========================================   

def deletar_produto(produto_id):
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        sql = "DELETE FROM Produto WHERE idProduto = %s"
        cursor.execute(sql, (produto_id,))
        connection.commit()
        return True

    except Exception as e:
        print(f"Erro ao deletar produto: {e}")
        return False

    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÕES DE ATUALIZAÇÃO DE PRODUTOS
# ==========================================

def atualizacao_produto(codigo, codigo_alternativo, nome, descricao, categoria, unidade_medida, preco, estoque_minimo, aplicacao_veicular, produto_id):
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()
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
        return cursor.rowcount > 0  # Retorna True se alguma linha foi afetada

    except Exception as e:
        print(f"Erro ao atualizar produto: {e}")
        connection.rollback()  # Reverter mudanças em caso de erro
        return False

    finally:
        close_db_connection(connection)

# ==========================================
# FUNÇÃO DE MOVIMENTAÇÃO DE ESTOQUE
# ==========================================

def movimentacao_estoque(produto_id, quantidade, tipo_movimentacao, id_usuario):
    connection = get_db_connection()
    if not connection:
        return False

    try:
        cursor = connection.cursor()

        # Atualiza o estoque atual do produto
        if tipo_movimentacao == 'entrada':
            sql_update = "UPDATE Produto SET estoque_atual = estoque_atual + %s WHERE idProduto = %s"
        elif tipo_movimentacao == 'saida':
            quantidade_atual = buscar_produto_por_id(produto_id)[9]  

            print(quantidade_atual, quantidade)
            if quantidade > quantidade_atual:
                return False
            sql_update = "UPDATE Produto SET estoque_atual = estoque_atual - %s WHERE idProduto = %s"
        else:
            print("Tipo de movimentação inválido.")
            return False

        cursor.execute(sql_update, (quantidade, produto_id))

        # Registra a movimentação no histórico
        sql_insert = """
            INSERT INTO Movimentacao (idProduto, quantidade, tipo_movimentacao, data_movimentacao, idUsuario)
            VALUES (%s, %s, %s, NOW(), %s)
        """
        cursor.execute(sql_insert, (produto_id, quantidade, tipo_movimentacao, id_usuario))

        connection.commit()
        return True

    except Exception as e:
        print(f"Erro ao movimentar estoque: {e}")
        connection.rollback()  # Reverter mudanças em caso de erro
        return False

    finally:
        close_db_connection(connection)


# ==========================================
# FUNÇÃO DE TESTE DE CONEXÃO
# ==========================================

def testar_conexao():
    try:
        connection = get_db_connection()
        if connection:
            print("✅ Conexão com banco de dados estabelecida com sucesso!")
            close_db_connection(connection)
            return True
        else:
            print("❌ Falha ao conectar com o banco de dados!")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar conexão: {e}")
        print("Certifique-se de que a aplicação Flask foi inicializada com init_db(app)")
        return False