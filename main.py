import sys
import uuid

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStackedWidget,
    QMessageBox
)

from banco import criar_banco

from templates.login import TelaLogin
from templates.inicio import TelaInicio
from templates.carrinho import TelaCarrinho
from templates.pagamento import TelaPagamento
from templates.meu_pedido import TelaMeuPedido
from templates.pedidos import TelaPedidos
from templates.entregas import TelaEntregas
from templates.dashboard import TelaDashboard


class Aplicacao(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Cantina - Sistema de Pedidos"
        )

        self.resize(1200, 750)

        self.usuario = None
        self.carrinho = []
        self.pedido_atual_id = None
        self.cliente_sessao = None

        self.stack = QStackedWidget()

        self.setCentralWidget(self.stack)

        self.telas = {}

        self.telas["login"] = TelaLogin(self)
        self.telas["inicio"] = TelaInicio(self)
        self.telas["carrinho"] = TelaCarrinho(self)
        self.telas["pagamento"] = TelaPagamento(self)
        self.telas["meu_pedido"] = TelaMeuPedido(self)

        self.telas["pedidos"] = TelaPedidos(self)
        self.telas["entregas"] = TelaEntregas(self)
        self.telas["dashboard"] = TelaDashboard(self)

        for tela in self.telas.values():
            self.stack.addWidget(tela)

        self.mostrar("login")

    def mostrar(self, nome):

        telas_gestor = [
            "dashboard",
            "pedidos",
            "entregas"
        ]

        telas_cliente = [
            "inicio",
            "carrinho",
            "pagamento",
            "meu_pedido"
        ]

        if nome in telas_gestor:

            if (
                not self.usuario
                or self.usuario.get("tipo") != "gestor"
            ):
                QMessageBox.warning(
                    self,
                    "Acesso",
                    "Entre como administrador para acessar essa área."
                )
                return

        if nome in telas_cliente:

            if (
                not self.usuario
                or self.usuario.get("tipo") != "cliente"
            ):
                QMessageBox.warning(
                    self,
                    "Acesso",
                    "Entre como cliente para acessar essa área."
                )
                return

        if nome == "meu_pedido":
            self.telas["meu_pedido"].atualizar()

        

        if nome == "pedidos":
            self.telas["pedidos"].atualizar()

        if nome == "entregas":
            self.telas["entregas"].atualizar()

        if nome == "dashboard":
            self.telas["dashboard"].atualizar()

        self.stack.setCurrentWidget(
            self.telas[nome]
        )

    def sair(self):

        self.usuario = None
        self.carrinho = []
        self.pedido_atual_id = None
        self.cliente_sessao = None

        self.mostrar("login")


if __name__ == "__main__":

    criar_banco()

    app = QApplication(sys.argv)

    janela = Aplicacao()
    janela.show()

    sys.exit(app.exec())