import uuid

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QMessageBox,
    QFrame
)

from modelos import Usuario


class TelaLogin(QWidget):

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

            QLineEdit {
                background: white;
                border: 2px solid #e5cfa1;
                border-radius: 8px;
                padding: 10px;
                font-size: 15px;
            }

            QPushButton {
                background: #f5ae00;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton:hover {
                background: #ffc52b;
            }
        """)

        layout_principal = QVBoxLayout()
        layout_principal.setContentsMargins(
            300, 80, 300, 80
        )

        titulo = QLabel(
            "ACESSO AO SISTEMA"
        )

        titulo.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout_principal.addWidget(titulo)

        subtitulo = QLabel(
            "Escolha como deseja entrar"
        )

        subtitulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout_principal.addWidget(subtitulo)

        # ==========================
        # ÁREA DO CLIENTE
        # ==========================

        cliente_frame = QFrame()

        cliente_layout = QVBoxLayout()

        cliente_titulo = QLabel(
            " CLIENTE"
        )

        cliente_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        cliente_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        cliente_layout.addWidget(
            cliente_titulo
        )

        btn_cliente = QPushButton(
            "ENTRAR COMO CLIENTE"
        )

        btn_cliente.clicked.connect(
            self.entrar_cliente
        )

        cliente_layout.addWidget(
            btn_cliente
        )

        cliente_frame.setLayout(
            cliente_layout
        )

        layout_principal.addWidget(
            cliente_frame
        )

        # ==========================
        # ÁREA DO ADMINISTRADOR
        # ==========================

        admin_frame = QFrame()

        admin_layout = QVBoxLayout()

        admin_titulo = QLabel(
            " ADMINISTRADOR"
        )

        admin_titulo.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        admin_titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        admin_layout.addWidget(
            admin_titulo
        )

        self.email = QLineEdit()
        self.email.setPlaceholderText(
            "E-mail do administrador"
        )

        admin_layout.addWidget(
            self.email
        )

        self.senha = QLineEdit()
        self.senha.setPlaceholderText(
            "Senha"
        )

        self.senha.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        admin_layout.addWidget(
            self.senha
        )

        btn_admin = QPushButton(
            "ENTRAR COMO ADMINISTRADOR"
        )

        btn_admin.clicked.connect(
            self.entrar_admin
        )

        admin_layout.addWidget(
            btn_admin
        )

        admin_frame.setLayout(
            admin_layout
        )

        layout_principal.addWidget(
            admin_frame
        )

        layout_principal.addStretch()

        self.setLayout(
            layout_principal
        )

    def entrar_cliente(self):

        self.app.usuario = {
            "nome": "Cliente",
            "tipo": "cliente"
        }

        self.app.cliente_sessao = (
            uuid.uuid4().hex
        )

        self.app.carrinho = []
        self.app.pedido_atual_id = None

        self.app.mostrar("inicio")

    def entrar_admin(self):

        email = self.email.text().strip()
        senha = self.senha.text().strip()

        if not email or not senha:

            QMessageBox.warning(
                self,
                "Atenção",
                "Digite o e-mail e a senha."
            )

            return

        usuario = Usuario.buscar_usuario(
            email,
            senha
        )

        if not usuario:

            QMessageBox.warning(
                self,
                "Erro",
                "E-mail ou senha incorretos."
            )

            return

        if usuario["tipo"] != "gestor":

            QMessageBox.warning(
                self,
                "Acesso",
                "Este usuário não é administrador."
            )

            return

        self.app.usuario = usuario
        self.app.cliente_sessao = None
        self.app.carrinho = []
        self.app.pedido_atual_id = None

        self.app.mostrar("dashboard")