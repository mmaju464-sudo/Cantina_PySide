from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QSpinBox,
    QComboBox,
    QMessageBox,
    QFrame,
    QScrollArea
)

from modelos import Produto


class TelaInicio(QWidget):

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

            QFrame {
                background: white;
                border: 2px solid #ead2a0;
                border-radius: 12px;
            }

            QPushButton {
                background: #f5ae00;
                color: #222;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #ffc52b;
            }

            QComboBox {
                background: white;
                color: #222;
                border: 2px solid #dfc18b;
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
                min-height: 20px;
            }

            QComboBox:hover {
                border: 2px solid #f5ae00;
            }

            QComboBox:focus {
                border: 2px solid #f5ae00;
            }

            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            QComboBox QAbstractItemView {
                background: white;
                color: #222;
                border: 2px solid #dfc18b;
                selection-background-color: #f5ae00;
                selection-color: #222;
            }

            QSpinBox {
                background: white;
                color: #222;
                border: 2px solid #dfc18b;
                border-radius: 8px;
                padding: 8px;
            }
        """)

        principal = QVBoxLayout()

        # ==================================================
        # TOPO
        # ==================================================

        topo = QHBoxLayout()

        titulo = QLabel(
            " CANTINA - FAÇA SEU PEDIDO"
        )

        titulo.setStyleSheet("""
            font-size: 25px;
            font-weight: bold;
            background: transparent;
            border: none;
        """)

        topo.addWidget(titulo)

        topo.addStretch()

        btn_meus = QPushButton(
            " MEUS PEDIDOS"
        )

        btn_meus.clicked.connect(
            lambda: self.app.mostrar("meu_pedido")
        )

        topo.addWidget(btn_meus)

        btn_carrinho = QPushButton(
            " CARRINHO"
        )

        btn_carrinho.clicked.connect(
            lambda: self.app.mostrar("carrinho")
        )

        topo.addWidget(btn_carrinho)

        btn_sair = QPushButton(
            "SAIR"
        )

        btn_sair.clicked.connect(
            self.app.sair
        )

        topo.addWidget(btn_sair)

        principal.addLayout(topo)

        # ==================================================
        # ÁREA DOS PRODUTOS
        # ==================================================

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.container = QWidget()

        self.grade = QGridLayout(
            self.container
        )

        self.grade.setSpacing(15)

        self.scroll.setWidget(
            self.container
        )

        principal.addWidget(
            self.scroll
        )

        self.setLayout(principal)

        self.carregar_produtos()

    # ======================================================
    # LIMPA OS CARDS
    # ======================================================

    def limpar_grade(self):

        while self.grade.count():

            item = self.grade.takeAt(0)

            widget = item.widget()

            if widget:
                widget.deleteLater()

    # ======================================================
    # CARREGA PRODUTOS
    # ======================================================

    def carregar_produtos(self):

        self.limpar_grade()

        produtos = Produto.listar()

        print("\n===== PRODUTOS CARREGADOS =====")

        for produto in produtos:
            print(
                produto["nome"],
                "-> sabores:",
                produto.get("sabores")
            )

        print("===============================\n")

        colunas = 4

        for indice, produto in enumerate(produtos):

            card = QFrame()

            layout = QVBoxLayout(card)

            # ==================================================
            # NOME
            # ==================================================

            nome = QLabel(
                produto["nome"]
            )

            nome.setWordWrap(True)

            nome.setStyleSheet("""
                font-size: 17px;
                font-weight: bold;
                background: transparent;
                border: none;
            """)

            layout.addWidget(nome)

            # ==================================================
            # CATEGORIA
            # ==================================================

            categoria = QLabel(
                f"Categoria: {produto['categoria']}"
            )

            categoria.setStyleSheet("""
                background: transparent;
                border: none;
            """)

            layout.addWidget(categoria)

            # ==================================================
            # PREÇO
            # ==================================================

            preco = QLabel(
                f"R$ {float(produto['preco']):.2f}"
            )

            preco.setStyleSheet("""
                font-size: 16px;
                font-weight: bold;
                background: transparent;
                border: none;
            """)

            layout.addWidget(preco)

            # ==================================================
            # SABORES
            # ==================================================

            combo_sabor = None

            sabores = produto.get("sabores")

            # Converte para texto e remove espaços
            if sabores is not None:

                sabores = str(sabores).strip()

            # Se houver sabores
            if sabores:

                label_sabor = QLabel(
                    "Escolha o sabor:"
                )

                label_sabor.setStyleSheet("""
                    font-size: 13px;
                    font-weight: bold;
                    color: #333;
                    background: transparent;
                    border: none;
                """)

                layout.addWidget(
                    label_sabor
                )

                combo_sabor = QComboBox()

                combo_sabor.setMinimumHeight(38)

                combo_sabor.addItem(
                    "Selecione o sabor..."
                )

                lista_sabores = [
                    sabor.strip()
                    for sabor in sabores.split(",")
                    if sabor.strip()
                ]

                combo_sabor.addItems(
                    lista_sabores
                )

                layout.addWidget(
                    combo_sabor
                )

            # ==================================================
            # QUANTIDADE
            # ==================================================

            label_quantidade = QLabel(
                "Quantidade:"
            )

            label_quantidade.setStyleSheet("""
                background: transparent;
                border: none;
            """)

            layout.addWidget(
                label_quantidade
            )

            quantidade = QSpinBox()

            quantidade.setMinimum(1)
            quantidade.setMaximum(99)
            quantidade.setValue(1)

            layout.addWidget(
                quantidade
            )

            # ==================================================
            # BOTÃO
            # ==================================================

            botao = QPushButton(
                " ADICIONAR"
            )

            botao.clicked.connect(
                lambda checked=False,
                p=produto,
                q=quantidade,
                c=combo_sabor:
                self.adicionar(
                    p,
                    q,
                    c
                )
            )

            layout.addWidget(
                botao
            )

            # ==================================================
            # ADICIONA CARD NA GRADE
            # ==================================================

            linha = indice // colunas
            coluna = indice % colunas

            self.grade.addWidget(
                card,
                linha,
                coluna
            )

    # ======================================================
    # ADICIONAR AO CARRINHO
    # ======================================================

    def adicionar(
        self,
        produto,
        quantidade,
        combo_sabor
    ):

        sabor = ""

        # Se o produto tem sabores
        if combo_sabor is not None:

            # Verifica se o cliente escolheu
            if combo_sabor.currentIndex() == 0:

                QMessageBox.warning(
                    self,
                    "Escolha o sabor",
                    (
                        f"Escolha um sabor para "
                        f"{produto['nome']} antes de adicionar."
                    )
                )

                return

            sabor = combo_sabor.currentText()

        item = {
            "id": produto["id"],
            "nome": produto["nome"],
            "preco": float(produto["preco"]),
            "quantidade": quantidade.value(),
            "sabor": sabor
        }

        # ==================================================
        # VERIFICA SE JÁ EXISTE O MESMO PRODUTO + SABOR
        # ==================================================

        encontrou = False

        for item_existente in self.app.carrinho:

            if (
                item_existente["id"] == item["id"]
                and item_existente.get("sabor", "") == sabor
            ):

                item_existente["quantidade"] += (
                    item["quantidade"]
                )

                encontrou = True

                break

        if not encontrou:

            self.app.carrinho.append(
                item
            )

        mensagem = (
            f"{produto['nome']}\n"
            f"Quantidade: {quantidade.value()}"
        )

        if sabor:

            mensagem += (
                f"\nSabor: {sabor}"
            )

        mensagem += (
            "\n\nAdicionado ao carrinho!"
        )

        QMessageBox.information(
            self,
            "Produto adicionado",
            mensagem
        )