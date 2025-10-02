# TDS-PEAS - Sistema de Controle de Estoque

Sistema web simples para controle de estoque desenvolvido em Flask e MySQL.

## Funcionalidades

- Cadastro, edição e exclusão de produtos
- Controle de entrada e saída de estoque
- Busca de produtos por nome
- Alertas visuais para estoque baixo
- Sistema de login de usuários

## Estrutura do Projeto

```
TDS-PEAS/
├── templates/        # Páginas HTML
├── static/           # Arquivos CSS
├── docs/             # Documentação e scripts SQL
├── app.py            # Aplicação principal
├── bd.py             # Funções do banco de dados
└── requirements.txt  # Dependências
```

## Banco de Dados

O sistema usa MySQL com 3 tabelas principais:
- **Usuario**: Dados dos usuários do sistema
- **Produto**: Informações dos produtos
- **Movimentacao**: Histórico de entradas e saídas

## Como usar

### Pré-requisitos
- Python 3.8+
- MySQL 8.0+

### Instalação

1. **Clone o projeto**
```bash
git clone https://github.com/GetuliovmSantos/TDS-PEAS.git
cd TDS-PEAS
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```


## Tecnologias

- Python + Flask
- MySQL
- HTML/CSS
- Jinja2

## Desenvolvedor

**Getulio Vagner Miranda Santos**
- GitHub: [@GetuliovmSantos](https://github.com/GetuliovmSantos)

---

*Projeto desenvolvido para o TDS - Técnico em Desenvolvimento de Sistemas*