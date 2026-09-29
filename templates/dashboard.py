from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QInputDialog,
    QMessageBox
)

from modelos import Pedido, Despesa


class TelaDashboard(QWidget):

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

            QPushButton {
                background: #f5ae00;
                border: none;
                border-radius: 10px;
                padding: 13px;
                font-weight: bold;
                font-size: 15px;
            }
        """)

        layout = QVBoxLayout()

        titulo = QLabel(
            "📊 PAINEL DO ADMINISTRADOR"
        )

        titulo.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
        """)

        layout.addWidget(
            titulo
        )

        self.receita = QLabel()

        self.despesa = QLabel()

        self.resultado = QLabel()

        self.prontos = QLabel()

        for label in [
            self.receita,
            self.despesa,
            self.resultado,
            self.prontos
        ]:

            label.setStyleSheet("""
                background: white;
                border: 2px solid #ead2a0;
                border-radius: 10px;
                padding: 15px;
                font-size: 20px;
                font-weight: bold;
            """)

            layout.addWidget(label)

        pedidos = QPushButton(
            " PEDIDOS"
        )

        pedidos.clicked.connect(
            lambda: self.app.mostrar(
                "pedidos"
            )
        )

        layout.addWidget(
            pedidos
        )

        entregas = QPushButton(
            " PEDIDOS PRONTOS"
        )

        entregas.clicked.connect(
            lambda: self.app.mostrar(
                "entregas"
            )
        )

        layout.addWidget(
            entregas
        )

        adicionar_despesa = QPushButton(
            " ADICIONAR DESPESA"
        )

        adicionar_despesa.clicked.connect(
            self.nova_despesa
        )

        layout.addWidget(
            adicionar_despesa
        )

        sair = QPushButton(
            "SAIR"
        )

        sair.clicked.connect(
            self.app.sair
        )

        layout.addWidget(
            sair
        )

        layout.addStretch()

        self.setLayout(layout)

    def atualizar(self):

        receita = Pedido.faturamento()

        despesas = Despesa.total()

        resultado = (
            receita - despesas
        )

        pedidos = Pedido.listar()

        quantidade_prontos = sum(
            1
            for p in pedidos
            if p["status"] == "Pronto"
        )

        self.receita.setText(
            f" RECEITAS: R$ {receita:.2f}"
        )

        self.despesa.setText(
            f" DESPESAS: R$ {despesas:.2f}"
        )

        self.resultado.setText(
            f" RESULTADO: R$ {resultado:.2f}"
        )

        self.prontos.setText(
            f" PEDIDOS PRONTOS: "
            f"{quantidade_prontos}"
        )

    def nova_despesa(self):

        descricao, ok = QInputDialog.getText(
            self,
            "Nova despesa",
            "Descrição:"
        )

        if not ok or not descricao:
            return

        valor, ok = QInputDialog.getDouble(
            self,
            "Nova despesa",
            "Valor:",
            0,
            0,
            999999,
            2
        )

        if not ok:
            return

        Despesa.adicionar(
            descricao,
            valor
        )

        self.atualizar()

        QMessageBox.information(
            self,
            "Sucesso",
            "Despesa adicionada."
        )