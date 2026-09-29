from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QListWidget
)

from modelos import Pedido


class TelaEntregas(QWidget):

    def __init__(self, app):

        super().__init__()

        self.app = app

        self.setStyleSheet("""
            QWidget {
                background: #fff4d6;
                font-family: Arial;
            }

            QLabel {
                font-size: 20px;
            }

            QListWidget {
                background: white;
                border: 2px solid #ead2a0;
                border-radius: 10px;
                font-size: 30px;
                padding: 15px;
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
            " PEDIDOS PRONTOS"
        )

        titulo.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
        """)

        layout.addWidget(titulo)

        self.lista = QListWidget()

        layout.addWidget(
            self.lista
        )

        voltar = QPushButton(
            "← VOLTAR"
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

            if pedido["status"] == "Pronto":

                self.lista.addItem(
                    f" PEDIDO #{pedido['codigo']}"
                )