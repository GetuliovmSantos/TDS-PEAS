from flaskext.mysql import MySQL
from werkzeug.security import check_password_hash
import pymysql

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
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM Usuario WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        user_data = cursor.fetchone()
        
        if user_data and user_data['senha'] == senha:
            return {
                'id': user_data['idUsuario'],
                'nome': user_data['nome'],
                'usuario': user_data['usuario']
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
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM Produto"
        cursor.execute(sql)
        produtos = cursor.fetchall()
        return produtos
    
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return []
    
    finally:
        close_db_connection(connection)

def buscar_produtos_por_nome(nome):
    connection = get_db_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql = "SELECT * FROM Produto WHERE nome LIKE %s"
        cursor.execute(sql, (f"%{nome}%",))
        produtos = cursor.fetchall()
        return produtos
    
    except Exception as e:
        print(f"Erro ao buscar produtos por nome: {e}")
        return []
    
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