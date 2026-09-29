import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
INSTANCE_DIR = BASE_DIR / "instance"
DB_PATH = INSTANCE_DIR / "cantina.db"


def conectar():
    INSTANCE_DIR.mkdir(exist_ok=True)
    return sqlite3.connect(DB_PATH)


def adicionar_coluna_se_faltar(cursor, tabela, coluna, tipo):
    cursor.execute(f"PRAGMA table_info({tabela})")
    colunas = [linha[1] for linha in cursor.fetchall()]

    if coluna not in colunas:
        cursor.execute(
            f"ALTER TABLE {tabela} ADD COLUMN {coluna} {tipo}"
        )


def sincronizar_produtos(cursor):
    produtos = [

        (
            "Croissant de presunto e queijo",
            "Salgado",
            7.00,
            ""
        ),

        (
            "Risole de 4 queijos",
            "Salgado",
            5.50,
            ""
        ),

        (
            "Risole de carne",
            "Salgado",
            5.50,
            ""
        ),

        (
            "Croissant 3 queijos",
            "Salgado",
            6.50,
            ""
        ),

        (
            "Croissant de Chocolate",
            "Doce",
            6.50,
            ""
        ),

        (
            "Hambúrguer com cheddar",
            "Lanche",
            7.00,
            ""
        ),

        (
            "Enroladinho de bauru",
            "Salgado",
            7.00,
            ""
        ),

        (
            "Pão de batata com calabresa",
            "Salgado",
            6.50,
            ""
        ),

        (
            "Pão de batata de frango",
            "Salgado",
            6.50,
            ""
        ),

        (
            "Esfiha de carne",
            "Salgado",
            7.00,
            ""
        ),

        (
            "Coxinha",
            "Salgado",
            5.50,
            ""
        ),

        (
            "Pão de queijo",
            "Salgado",
            3.50,
            ""
        ),

        (
            "Caldo",
            "Caldo",
            20.00,
            "mandioca,abóbora,verde,feijão"
        ),

        (
            "Espeto",
            "Espeto",
            9.00,
            "carne,medalhão,coração"
        ),

        (
            "Guaraná 350ml",
            "Bebida",
            5.50,
            ""
        ),

        (
            "Fanta uva 350ml",
            "Bebida",
            5.50,
            ""
        ),

        (
            "Fanta laranja 350ml",
            "Bebida",
            5.50,
            ""
        ),

        (
            "Coca-Cola sem açúcar 350ml",
            "Bebida",
            5.50,
            ""
        ),

        (
            "Coca-Cola 350ml",
            "Bebida",
            5.50,
            ""
        ),

        (
            "Suco tropical 480ml",
            "Bebida",
            8.00,
            "uva,manga,abacaxi,açaí,goiaba"
        ),

        (
            "Suco Kmais 300ml",
            "Bebida",
            7.50,
            "goiaba,laranja,uva,maracujá"
        ),

        (
            "Refrigerante caçula 200ml",
            "Bebida",
            5.00,
            "Coca-Cola,Pepsi,Fanta uva,Coca-Cola sem açúcar"
        ),
    ]

    for nome, categoria, preco, sabores in produtos:

        cursor.execute(
            "SELECT id FROM produtos WHERE nome = ?",
            (nome,)
        )

        existente = cursor.fetchone()

        if existente:

            cursor.execute(
                """
                UPDATE produtos
                SET categoria = ?,
                    preco = ?,
                    sabores = ?
                WHERE nome = ?
                """,
                (
                    categoria,
                    preco,
                    sabores,
                    nome
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO produtos
                (nome, categoria, preco, imagem, sabores)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    nome,
                    categoria,
                    preco,
                    "",
                    sabores
                )
            )


def criar_banco():

    conn = conectar()
    cursor = conn.cursor()

    # ==========================
    # PRODUTOS
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            preco REAL NOT NULL,
            imagem TEXT,
            sabores TEXT
        )
    """)

    adicionar_coluna_se_faltar(
        cursor,
        "produtos",
        "imagem",
        "TEXT"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "produtos",
        "sabores",
        "TEXT"
    )

    # ==========================
    # PEDIDOS
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            total REAL NOT NULL,
            pagamento TEXT NOT NULL,
            status TEXT NOT NULL,
            tipo TEXT NOT NULL,
            criado_em TEXT NOT NULL,
            cliente_sessao TEXT
        )
    """)

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "codigo",
        "TEXT"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "total",
        "REAL"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "pagamento",
        "TEXT"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "status",
        "TEXT"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "tipo",
        "TEXT"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "criado_em",
        "TEXT"
    )

    adicionar_coluna_se_faltar(
        cursor,
        "pedidos",
        "cliente_sessao",
        "TEXT"
    )

    # ==========================
    # ITENS DO PEDIDO
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            nome_produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL,
            sabor TEXT
        )
    """)

    adicionar_coluna_se_faltar(
        cursor,
        "itens_pedido",
        "sabor",
        "TEXT"
    )

    # ==========================
    # DESPESAS
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            data TEXT NOT NULL
        )
    """)

    # ==========================
    # USUÁRIOS
    # ==========================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            tipo TEXT NOT NULL
        )
    """)

    # ==========================
    # ADMINISTRADOR
    # ==========================

    cursor.execute(
        "SELECT id FROM usuarios WHERE email = ?",
        ("admin@cantina.com",)
    )

    admin = cursor.fetchone()

    if not admin:
        cursor.execute(
            """
            INSERT INTO usuarios
            (nome, email, senha, tipo)
            VALUES (?, ?, ?, ?)
            """,
            (
                "Administrador",
                "admin@cantina.com",
                "1234",
                "gestor"
            )
        )

    # ==========================
    # SINCRONIZA PRODUTOS
    # ==========================

    sincronizar_produtos(cursor)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    criar_banco()
    print("Banco criado/atualizado com sucesso!")
    print(f"Local: {DB_PATH}")