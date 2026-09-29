from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QMessageBox,
    QComboBox
)

from modelos import Pedido


class TelaPedidos(QWidget):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setStyleSheet("""
            QWidget {
                background: #fff4d6;
                font-family: Arial;
            }

            QListWidget {
                background: white;
                border: 2px solid #ead2a0;
                border-radius: 10px;
                font-size: 16px;
                padding: 10px;
            }

            QComboBox {
                background: white;
                border: 2px solid #dfc18b;
                border-radius: 8px;
                padding: 10px;
            }

            QPushButton {
                background: #f5ae00;
                border: none;
                border-radius: 10px;
                padding: 11px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()

        titulo = QLabel(
            "👨‍🍳 FILA DE PEDIDOS"
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

        controles = QHBoxLayout()

        self.status = QComboBox()

        self.status.addItems([
            "Recebido",
            "Em preparo",
            "Pronto",
            "Entregue",
            "Cancelado"
        ])

        controles.addWidget(
            self.status
        )

        alterar = QPushButton(
            "ALTERAR STATUS"
        )

        alterar.clicked.connect(
            self.alterar_status
        )

        controles.addWidget(
            alterar
        )

        layout.addLayout(
            controles
        )

        voltar = QPushButton(
            "← VOLTAR AO PAINEL"
        )

        voltar.clicked.connect(
            lambda: self.app.mostrar(
                "dashboard"
            )
        )

        layout.addWidget(
            voltar
        )

        self.setLayout(layout)

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.atualizar
        )

        self.timer.start(3000)

    def atualizar(self):

        self.lista.clear()

        pedidos = Pedido.listar()

        for pedido in pedidos:

            texto = (
                f"#{pedido['codigo']} | "
                f"{pedido['status']} | "
                f"R$ {pedido['total']:.2f} | "
                f"{pedido['pagamento']} | "
                f"{pedido['criado_em']}"
            )

            self.lista.addItem(texto)

            item = self.lista.item(
                self.lista.count() - 1
            )

            item.setData(
                32,
                pedido["id"]
            )

    def alterar_status(self):

        item = self.lista.currentItem()

        if not item:

            QMessageBox.warning(
                self,
                "Atenção",
                "Selecione um pedido."
            )

            return

        pedido_id = item.data(32)

        novo_status = (
            self.status.currentText()
        )

        Pedido.alterar_status(
            pedido_id,
            novo_status
        )

        self.atualizar()

        QMessageBox.information(
            self,
            "Sucesso",
            "Status atualizado."
        )