from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)


class TelaCarrinho(QWidget):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setStyleSheet("""
            QWidget {
                background: #fff4d6;
                font-family: Arial;
            }

            QPushButton {
                background: #f5ae00;
                border: none;
                border-radius: 10px;
                padding: 11px;
                font-weight: bold;
            }

            QListWidget {
                background: white;
                border: 2px solid #ead2a0;
                border-radius: 10px;
                padding: 8px;
            }
        """)

        layout = QVBoxLayout()

        titulo = QLabel(
            " MEU CARRINHO"
        )

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        layout.addWidget(titulo)

        self.lista = QListWidget()

        layout.addWidget(
            self.lista
        )

        self.total = QLabel()

        self.total.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
        """)

        layout.addWidget(
            self.total
        )

        botoes = QHBoxLayout()

        voltar = QPushButton(
            "← VOLTAR"
        )

        voltar.clicked.connect(
            lambda: self.app.mostrar(
                "inicio"
            )
        )

        botoes.addWidget(
            voltar
        )

        finalizar = QPushButton(
            "IR PARA PAGAMENTO →"
        )

        finalizar.clicked.connect(
            self.finalizar
        )

        botoes.addWidget(
            finalizar
        )

        layout.addLayout(
            botoes
        )

        self.setLayout(layout)

    def showEvent(self, event):

        self.atualizar()

        super().showEvent(event)

    def atualizar(self):

        self.lista.clear()

        total = 0

        for indice, item in enumerate(
            self.app.carrinho
        ):

            subtotal = (
                item["preco"]
                * item["quantidade"]
            )

            total += subtotal

            texto = (
                f"{item['nome']}"
                f" | Quantidade: {item['quantidade']}"
            )

            if item.get("sabor"):

                texto += (
                    f" | Sabor: {item['sabor']}"
                )

            texto += (
                f" | R$ {subtotal:.2f}"
            )

            lista_item = QListWidgetItem(
                texto
            )

            lista_item.setData(
                32,
                indice
            )

            self.lista.addItem(
                lista_item
            )

        self.total.setText(
            f"TOTAL: R$ {total:.2f}"
        )

    def finalizar(self):

        if not self.app.carrinho:

            QMessageBox.warning(
                self,
                "Carrinho vazio",
                "Adicione algum produto antes."
            )

            return

        self.app.mostrar(
            "pagamento"
        )