import sqlite3
import random
from datetime import datetime

from banco import conectar


class Produto:

    @staticmethod
    def listar():
        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM produtos
            ORDER BY categoria, nome
        """)

        produtos = [dict(row) for row in cursor.fetchall()]

        conn.close()

        return produtos


class Usuario:

    @staticmethod
    def buscar_usuario(email, senha):

        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM usuarios
            WHERE email = ?
            AND senha = ?
            """,
            (email, senha)
        )

        usuario = cursor.fetchone()

        conn.close()

        if usuario:
            return dict(usuario)

        return None


class Pedido:

    @staticmethod
    def gerar_codigo():

        conn = conectar()
        cursor = conn.cursor()

        while True:

            codigo = str(random.randint(1000, 9999))

            cursor.execute(
                "SELECT id FROM pedidos WHERE codigo = ?",
                (codigo,)
            )

            if not cursor.fetchone():
                conn.close()
                return codigo

    @staticmethod
    def criar(
        carrinho,
        pagamento,
        cliente_sessao,
        tipo="Retirada"
    ):

        conn = conectar()
        cursor = conn.cursor()

        codigo = Pedido.gerar_codigo()

        total = 0

        for item in carrinho:
            total += (
                float(item["preco"]) *
                int(item["quantidade"])
            )

        criado_em = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )

        cursor.execute(
            """
            INSERT INTO pedidos
            (
                codigo,
                total,
                pagamento,
                status,
                tipo,
                criado_em,
                cliente_sessao
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                codigo,
                total,
                pagamento,
                "Recebido",
                tipo,
                criado_em,
                cliente_sessao
            )
        )

        pedido_id = cursor.lastrowid

        for item in carrinho:

            cursor.execute(
                """
                INSERT INTO itens_pedido
                (
                    pedido_id,
                    produto_id,
                    nome_produto,
                    quantidade,
                    preco,
                    sabor
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    pedido_id,
                    item["id"],
                    item["nome"],
                    item["quantidade"],
                    item["preco"],
                    item.get("sabor", "")
                )
            )

        conn.commit()
        conn.close()

        return pedido_id, codigo, total

    @staticmethod
    def listar():

        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM pedidos
            ORDER BY id DESC
        """)

        pedidos = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return pedidos

    @staticmethod
    def listar_do_cliente(cliente_sessao):

        if not cliente_sessao:
            return []

        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM pedidos
            WHERE cliente_sessao = ?
            ORDER BY id DESC
            """,
            (cliente_sessao,)
        )

        pedidos = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return pedidos

    @staticmethod
    def buscar_do_cliente(
        pedido_id,
        cliente_sessao
    ):

        if not cliente_sessao:
            return None

        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM pedidos
            WHERE id = ?
            AND cliente_sessao = ?
            """,
            (
                pedido_id,
                cliente_sessao
            )
        )

        pedido = cursor.fetchone()

        conn.close()

        if pedido:
            return dict(pedido)

        return None

    @staticmethod
    def itens(pedido_id):

        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM itens_pedido
            WHERE pedido_id = ?
            ORDER BY id
            """,
            (pedido_id,)
        )

        itens = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return itens

    @staticmethod
    def alterar_status(
        pedido_id,
        status
    ):

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE pedidos
            SET status = ?
            WHERE id = ?
            """,
            (
                status,
                pedido_id
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def faturamento():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(total), 0)
            FROM pedidos
            WHERE status != 'Cancelado'
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total


class Despesa:

    @staticmethod
    def adicionar(descricao, valor):

        conn = conectar()
        cursor = conn.cursor()

        data = datetime.now().strftime(
            "%d/%m/%Y"
        )

        cursor.execute(
            """
            INSERT INTO despesas
            (descricao, valor, data)
            VALUES (?, ?, ?)
            """,
            (
                descricao,
                valor,
                data
            )
        )

        conn.commit()
        conn.close()

    @staticmethod
    def listar():

        conn = conectar()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM despesas
            ORDER BY id DESC
        """)

        despesas = [
            dict(row)
            for row in cursor.fetchall()
        ]

        conn.close()

        return despesas

    @staticmethod
    def total():

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COALESCE(SUM(valor), 0)
            FROM despesas
        """)

        total = cursor.fetchone()[0]

        conn.close()

        return total