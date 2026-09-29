from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QMessageBox
)

from modelos import Pedido


class TelaPagamento(QWidget):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setStyleSheet("""
            QWidget {
                background: #fff4d6;
                font-family: Arial;
            }

            QLabel {
                font-size: 18px;
            }

            QComboBox {
                background: white;
                border: 2px solid #dfc18b;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
            }

            QPushButton {
                background: #f5ae00;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()

        titulo = QLabel(
            "💳 PAGAMENTO"
        )

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        layout.addWidget(titulo)

        self.total = QLabel()

        layout.addWidget(
            self.total
        )

        self.pagamento = QComboBox()

        self.pagamento.addItems([
            "PIX",
            "Dinheiro",
            "Cartão de crédito",
            "Cartão de débito"
        ])

        layout.addWidget(
            QLabel("Forma de pagamento:")
        )

        layout.addWidget(
            self.pagamento
        )

        confirmar = QPushButton(
            "CONFIRMAR PEDIDO"
        )

        confirmar.clicked.connect(
            self.confirmar
        )

        layout.addWidget(
            confirmar
        )

        voltar = QPushButton(
            "← VOLTAR AO CARRINHO"
        )

        voltar.clicked.connect(
            lambda: self.app.mostrar(
                "carrinho"
            )
        )

        layout.addWidget(
            voltar
        )

        layout.addStretch()

        self.setLayout(layout)

    def showEvent(self, event):

        total = 0

        for item in self.app.carrinho:

            total += (
                item["preco"]
                * item["quantidade"]
            )

        self.total.setText(
            f"TOTAL DO PEDIDO: R$ {total:.2f}"
        )

        super().showEvent(event)

    def confirmar(self):

        if not self.app.carrinho:

            QMessageBox.warning(
                self,
                "Erro",
                "O carrinho está vazio."
            )

            return

        forma = self.pagamento.currentText()

        pedido_id, codigo, total = Pedido.criar(
            self.app.carrinho,
            forma,
            self.app.cliente_sessao
        )

        self.app.pedido_atual_id = pedido_id

        self.app.carrinho = []

        QMessageBox.information(
            self,
            "Pedido realizado!",
            (
                f"Pedido realizado com sucesso!\n\n"
                f"Seu código é:\n\n"
                f"🔢 {codigo}\n\n"
                f"Total: R$ {total:.2f}\n\n"
                f"Acompanhe o pedido em "
                f"'Meus Pedidos'."
            )
        )

        self.app.mostrar(
            "meu_pedido"
        )