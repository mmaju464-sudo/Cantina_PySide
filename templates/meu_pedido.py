from PySide6.QtCore import Qt, QTimer

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem
)

from modelos import Pedido


class TelaMeuPedido(QWidget):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setStyleSheet("""
            QWidget {
                background: #fff4d6;
                font-family: Arial;
            }

            QLabel {
                color: #222;
            }

            QListWidget {
                background: white;
                border: 2px solid #ead2a0;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
            }

            QPushButton {
                background: #f5ae00;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }

            QPushButton:hover {
                background: #ffc52b;
            }
        """)

        layout = QVBoxLayout()

        # ==================================================
        # TÍTULO
        # ==================================================

        self.titulo = QLabel(
            " MEUS PEDIDOS"
        )

        self.titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        layout.addWidget(
            self.titulo
        )

        # ==================================================
        # LISTA DE TODOS OS PEDIDOS
        # ==================================================

        self.lista_pedidos = QListWidget()

        self.lista_pedidos.itemClicked.connect(
            self.selecionar_pedido
        )

        layout.addWidget(
            self.lista_pedidos
        )

        # ==================================================
        # DETALHES DO PEDIDO SELECIONADO
        # ==================================================

        self.detalhes = QLabel(
            "Selecione um pedido acima para ver os detalhes."
        )

        self.detalhes.setWordWrap(True)

        self.detalhes.setStyleSheet("""
            background: white;
            border: 2px solid #ead2a0;
            border-radius: 10px;
            padding: 15px;
            font-size: 18px;
        """)

        layout.addWidget(
            self.detalhes
        )

        # ==================================================
        # ITENS DO PEDIDO
        # ==================================================

        self.lista_itens = QListWidget()

        layout.addWidget(
            self.lista_itens
        )

        # ==================================================
        # BOTÕES
        # ==================================================

        botoes = QHBoxLayout()

        voltar = QPushButton(
            "← VOLTAR PARA O MENU"
        )

        voltar.clicked.connect(
            lambda: self.app.mostrar("inicio")
        )

        botoes.addWidget(
            voltar
        )

        atualizar = QPushButton(
            " ATUALIZAR"
        )

        atualizar.clicked.connect(
            self.atualizar
        )

        botoes.addWidget(
            atualizar
        )

        sair = QPushButton(
            "SAIR"
        )

        sair.clicked.connect(
            self.app.sair
        )

        botoes.addWidget(
            sair
        )

        layout.addLayout(
            botoes
        )

        self.setLayout(layout)

        # ==================================================
        # ATUALIZA AUTOMATICAMENTE
        # ==================================================

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.atualizar
        )

        self.timer.start(3000)

    # ======================================================
    # ATUALIZA A LISTA DE PEDIDOS
    # ======================================================

    def atualizar(self):

        if not self.app.cliente_sessao:
            return

        pedidos = Pedido.listar_do_cliente(
            self.app.cliente_sessao
        )

        pedido_selecionado = (
            self.app.pedido_atual_id
        )

        self.lista_pedidos.clear()

        # --------------------------------------------------
        # NENHUM PEDIDO
        # --------------------------------------------------

        if not pedidos:

            item = QListWidgetItem(
                "Você ainda não fez nenhum pedido."
            )

            self.lista_pedidos.addItem(
                item
            )

            self.detalhes.setText(
                "Você ainda não possui pedidos."
            )

            self.lista_itens.clear()

            return

        # --------------------------------------------------
        # MOSTRA TODOS OS PEDIDOS
        # --------------------------------------------------

        for pedido in pedidos:

            texto = (
                f"Pedido #{pedido['codigo']}  |  "
                f"Status: {pedido['status']}  |  "
                f"R$ {pedido['total']:.2f}  |  "
                f"{pedido['criado_em']}"
            )

            item = QListWidgetItem(
                texto
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                pedido["id"]
            )

            self.lista_pedidos.addItem(
                item
            )

            # Seleciona automaticamente o pedido atual
            if (
                pedido_selecionado
                and pedido["id"]
                == pedido_selecionado
            ):

                self.lista_pedidos.setCurrentItem(
                    item
                )

        # --------------------------------------------------
        # SE NÃO TEM PEDIDO SELECIONADO,
        # MOSTRA O PRIMEIRO
        # --------------------------------------------------

        if not pedido_selecionado:

            primeiro = (
                self.lista_pedidos.item(0)
            )

            if primeiro:

                self.lista_pedidos.setCurrentItem(
                    primeiro
                )

                self.selecionar_pedido(
                    primeiro
                )

        else:

            pedido = Pedido.buscar_do_cliente(
                pedido_selecionado,
                self.app.cliente_sessao
            )

            if pedido:

                self.mostrar_detalhes(
                    pedido
                )

    # ======================================================
    # QUANDO CLICA EM UM PEDIDO
    # ======================================================

    def selecionar_pedido(self, item):

        pedido_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not pedido_id:
            return

        self.app.pedido_atual_id = pedido_id

        pedido = Pedido.buscar_do_cliente(
            pedido_id,
            self.app.cliente_sessao
        )

        if not pedido:
            return

        self.mostrar_detalhes(
            pedido
        )

    # ======================================================
    # MOSTRA OS DETALHES
    # ======================================================

    def mostrar_detalhes(self, pedido):

        self.detalhes.setText(
            f"""
            <b> Pedido #{pedido['codigo']}</b><br><br>

            <b>Status:</b> {pedido['status']}<br>

            <b>Pagamento:</b> {pedido['pagamento']}<br>

            <b>Tipo:</b> {pedido['tipo']}<br>

            <b>Data:</b> {pedido['criado_em']}<br>

            <b>Total:</b> R$ {pedido['total']:.2f}
            """
        )

        self.lista_itens.clear()

        itens = Pedido.itens(
            pedido["id"]
        )

        for item in itens:

            texto = (
                f"{item['quantidade']}x "
                f"{item['nome_produto']}"
            )

            if item.get("sabor"):

                texto += (
                    f" | Sabor: {item['sabor']}"
                )

            subtotal = (
                item["preco"]
                * item["quantidade"]
            )

            texto += (
                f" | R$ {subtotal:.2f}"
            )

            self.lista_itens.addItem(
                texto
            )