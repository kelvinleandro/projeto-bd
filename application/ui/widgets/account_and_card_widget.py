from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QListWidget, QListWidgetItem,
                               QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, 
                               QMessageBox, QLabel, QSplitter, QTabWidget)

from database.connection import get_db_connection
import database.generic_operations as db
from ui.dialogs.add_account_dialog import AddAccountDialog
from ui.dialogs.add_card_dialog import AddCardDialog
from ui.dialogs.add_transaction_dialog import AddTransactionDialog

class AccountAndCardWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        
        # --- Barra Superior ---
        top_bar_layout = QHBoxLayout()
        top_bar_layout.addWidget(QLabel("Selecione o Usuário:"))
        self.user_combo = QComboBox()
        top_bar_layout.addWidget(self.user_combo)
        top_bar_layout.addStretch()
        self.add_transaction_button = QPushButton(QIcon.fromTheme("document-new"), " Nova Transação")
        top_bar_layout.addWidget(self.add_transaction_button)
        self.layout.addLayout(top_bar_layout)

        # --- Painel Dividido ---
        splitter = QSplitter(self)
        self.layout.addWidget(splitter)

        # --- Painel Esquerdo (Contas) ---
        accounts_panel = QWidget()
        accounts_layout = QVBoxLayout(accounts_panel)
        accounts_layout.addWidget(QLabel("Contas do Usuário"))
        self.account_list = QListWidget()
        accounts_layout.addWidget(self.account_list)
        account_buttons_layout = QHBoxLayout()
        self.add_account_button = QPushButton(QIcon.fromTheme("list-add"), " Adicionar")
        self.edit_account_button = QPushButton(QIcon.fromTheme("document-edit"), " Editar")
        self.del_account_button = QPushButton(QIcon.fromTheme("edit-delete"), " Remover")
        account_buttons_layout.addWidget(self.add_account_button)
        account_buttons_layout.addWidget(self.edit_account_button)
        account_buttons_layout.addWidget(self.del_account_button)
        accounts_layout.addLayout(account_buttons_layout)
        splitter.addWidget(accounts_panel)

        # --- Painel Direito (Abas) ---
        right_panel_tabs = QTabWidget()
        splitter.addWidget(right_panel_tabs)

        # Aba de Cartões
        cards_panel = QWidget()
        cards_layout = QVBoxLayout(cards_panel)
        self.card_table = QTableWidget()
        self.card_table.setColumnCount(4)
        self.card_table.setHorizontalHeaderLabels(["ID", "Número", "Expiração", "Tipo"])
        self.card_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.card_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.card_table.setEditTriggers(QTableWidget.NoEditTriggers)
        cards_layout.addWidget(self.card_table)
        card_buttons_layout = QHBoxLayout()
        self.add_card_button = QPushButton(QIcon.fromTheme("list-add"), " Adicionar Cartão")
        self.edit_card_button = QPushButton(QIcon.fromTheme("document-edit"), " Editar Cartão")
        self.del_card_button = QPushButton(QIcon.fromTheme("edit-delete"), " Remover Cartão")
        card_buttons_layout.addWidget(self.add_card_button)
        card_buttons_layout.addWidget(self.edit_card_button)
        card_buttons_layout.addWidget(self.del_card_button)
        cards_layout.addLayout(card_buttons_layout)
        right_panel_tabs.addTab(cards_panel, "Cartões da Conta")

        # Aba de Transações
        transactions_panel = QWidget()
        transactions_layout = QVBoxLayout(transactions_panel)
        self.transaction_table = QTableWidget()
        self.transaction_table.setColumnCount(6) # Ajustado para 6 colunas
        self.transaction_table.setHorizontalHeaderLabels(["ID", "Data", "Categoria", "Valor", "Tipo", "Detalhes"])
        self.transaction_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.transaction_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.transaction_table.setEditTriggers(QTableWidget.NoEditTriggers)
        transactions_layout.addWidget(self.transaction_table)
        right_panel_tabs.addTab(transactions_panel, "Transações da Conta")

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)

        # --- Conexões de Sinais ---
        self.user_combo.currentIndexChanged.connect(self.on_user_changed)
        self.account_list.currentItemChanged.connect(self.on_account_changed)
        self.account_list.itemSelectionChanged.connect(self.update_button_states)
        self.card_table.itemSelectionChanged.connect(self.update_button_states)
        self.add_account_button.clicked.connect(self.add_account)
        self.edit_account_button.clicked.connect(self.edit_account)
        self.del_account_button.clicked.connect(self.delete_account)
        self.add_card_button.clicked.connect(self.add_card)
        self.edit_card_button.clicked.connect(self.edit_card)
        self.del_card_button.clicked.connect(self.delete_card)
        self.add_transaction_button.clicked.connect(self.add_transaction)

        self.load_users()
        self.update_button_states()

    # --- Lógica de Atualização da UI ---
    
    def update_button_states(self):
        user_selected = self.user_combo.currentData() is not None
        account_selected = self.account_list.currentItem() is not None
        card_selected = bool(self.card_table.selectedItems())
        
        self.add_transaction_button.setEnabled(user_selected)
        self.add_account_button.setEnabled(user_selected)
        self.edit_account_button.setEnabled(account_selected)
        self.del_account_button.setEnabled(account_selected)
        self.add_card_button.setEnabled(account_selected)
        self.edit_card_button.setEnabled(card_selected)
        self.del_card_button.setEnabled(card_selected)

    def on_user_changed(self):
        self.load_accounts()

    def on_account_changed(self):
        self.load_cards()
        self.load_transactions()

    # --- Funções de Carregamento de Dados (Refatoradas) ---

    def load_users(self):
        self._perform_db_action(
            lambda conn: db.get_all(conn, "app_user", ["cpf", "first_name", "last_name"]),
            on_success=self._populate_users_combo
        )

    def _populate_users_combo(self, users):
        self.user_combo.blockSignals(True)
        self.user_combo.clear()
        self.user_combo.addItem("Selecione...", None)
        if users:
            for user in users:
                self.user_combo.addItem(f"{user['first_name']} {user['last_name']}", user['cpf'])
        self.user_combo.blockSignals(False)
        self.on_user_changed()

    def load_accounts(self):
        self.account_list.clear()
        user_cpf = self.user_combo.currentData()
        if not user_cpf:
            self.on_account_changed()
            return
        self._perform_db_action(db.get_accounts_for_user, user_cpf, on_success=self._populate_accounts_list)

    def _populate_accounts_list(self, accounts):
        if accounts:
            for acc in accounts:
                item = QListWidgetItem(f"ID {acc['id']} ({acc['type']}) - Saldo: R$ {acc['balance']:.2f}")
                item.setData(Qt.UserRole, acc['id'])
                self.account_list.addItem(item)
        if self.account_list.count() > 0:
            self.account_list.setCurrentRow(0)
        self.on_account_changed()

    def load_cards(self):
        self.card_table.setRowCount(0)
        current_item = self.account_list.currentItem()
        if not current_item:
            self.update_button_states()
            return
        account_id = current_item.data(Qt.UserRole)
        self._perform_db_action(db.get_cards_for_account, account_id, on_success=self._populate_cards_table)

    def _populate_cards_table(self, cards):
        if not cards: return
        self.card_table.setRowCount(len(cards))
        for row, card in enumerate(cards):
            item_id = QTableWidgetItem(str(card['id']))
            item_id.setData(Qt.UserRole, card['id']) # Armazena o ID no item
            self.card_table.setItem(row, 0, item_id)
            self.card_table.setItem(row, 1, QTableWidgetItem(card['number']))
            self.card_table.setItem(row, 2, QTableWidgetItem(card['expiration_date']))
            self.card_table.setItem(row, 3, QTableWidgetItem(card['type']))
        self.update_button_states()

    def load_transactions(self):
        self.transaction_table.setRowCount(0)
        current_item = self.account_list.currentItem()
        if not current_item:
            self.update_button_states()
            return
        account_id = current_item.data(Qt.UserRole)
        self._perform_db_action(db.get_transactions_for_account, account_id, on_success=self._populate_transactions_table)
    
    def _populate_transactions_table(self, transactions):
        if not transactions: return
        self.transaction_table.setRowCount(len(transactions))
        for row, trans in enumerate(transactions):
            value_item = QTableWidgetItem(f"{trans['value']:.2f}")
            if trans['type'] == 'expense':
                value_item.setForeground(QColor('red'))
            elif trans['type'] == 'income':
                value_item.setForeground(QColor('green'))

            details_item = QTableWidgetItem(f"{trans['source']} ({trans['source_details']})")

            self.transaction_table.setItem(row, 0, QTableWidgetItem(str(trans['id'])))
            self.transaction_table.setItem(row, 1, QTableWidgetItem(str(trans['date'])))
            self.transaction_table.setItem(row, 2, QTableWidgetItem(trans['category_name']))
            self.transaction_table.setItem(row, 3, value_item)
            self.transaction_table.setItem(row, 4, QTableWidgetItem(trans['type']))
            self.transaction_table.setItem(row, 5, details_item)
        self.update_button_states()

    # --- Ações de CRUD (Adicionar, Editar, Deletar) ---

    def add_account(self):
        user_cpf = self.user_combo.currentData()
        if not user_cpf:
            QMessageBox.warning(self, "Ação Inválida", "Selecione um usuário primeiro.")
            return
        dialog = AddAccountDialog(self)
        if dialog.exec():
            self._perform_db_action(db.add_new_account, user_cpf, dialog.get_data(), on_success=self.load_accounts)

    def edit_account(self):
        current_item = self.account_list.currentItem()
        if not current_item: return
        account_id = current_item.data(Qt.UserRole)
        
        def on_data_fetched(account_data):
            if not account_data:
                QMessageBox.warning(self, "Erro", "Dados da conta não encontrados.")
                return
            dialog = AddAccountDialog(self, item_data=account_data)
            if dialog.exec():
                self._perform_db_action(db.update_account, account_id, dialog.get_data(), on_success=self.load_accounts)

        self._perform_db_action(db.get_account_details, account_id, on_success=on_data_fetched)

    def delete_account(self):
        current_item = self.account_list.currentItem()
        if not current_item: return
        account_id = current_item.data(Qt.UserRole)
        reply = QMessageBox.question(self, 'Confirmar Exclusão', 
                                     f"Tem certeza que deseja deletar a conta ID {account_id} e todos os seus dados associados (cartões, transações, etc)?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._perform_db_action(db.delete_item, "account", "id", account_id, on_success=self.load_accounts)

    def add_card(self):
        current_item = self.account_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Ação Inválida", "Selecione uma conta primeiro.")
            return
        account_id = current_item.data(Qt.UserRole)
        dialog = AddCardDialog(self)
        if dialog.exec():
            self._perform_db_action(db.add_new_card, account_id, dialog.get_data(), on_success=self.load_cards)

    def edit_card(self):
        selected_row = self.card_table.currentRow()
        if selected_row < 0: return
        card_id = self.card_table.item(selected_row, 0).data(Qt.UserRole)

        def on_data_fetched(card_data):
            if not card_data:
                QMessageBox.warning(self, "Erro", "Dados do cartão não encontrados.")
                return
            dialog = AddCardDialog(self, item_data=card_data)
            if dialog.exec():
                self._perform_db_action(db.update_card, card_id, dialog.get_data(), on_success=self.load_cards)
        
        self._perform_db_action(db.get_card_details, card_id, on_success=on_data_fetched)
            
    def delete_card(self):
        selected_row = self.card_table.currentRow()
        if selected_row < 0: return
        card_id = self.card_table.item(selected_row, 0).data(Qt.UserRole)
        reply = QMessageBox.question(self, 'Confirmar Exclusão', f"Tem certeza que deseja deletar o cartão ID {card_id}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self._perform_db_action(db.delete_item, "card", "id", card_id, on_success=self.load_cards)

    def add_transaction(self):
        user_cpf = self.user_combo.currentData()
        if not user_cpf:
            QMessageBox.warning(self, "Ação Inválida", "Selecione um usuário primeiro.")
            return
        dialog = AddTransactionDialog(user_cpf, self)
        if dialog.exec():
            # Após adicionar uma transação, é melhor recarregar as contas, o que em cascata recarregará as transações
            self._perform_db_action(db.add_transaction, dialog.get_data(), on_success=lambda result: self.load_accounts())



    def _perform_db_action(self, db_function, *args, on_success=None):
        conn = None
        try:
            conn = get_db_connection()
            if not conn:
                QMessageBox.critical(self, "Erro de Conexão", "Não foi possível conectar ao banco de dados.")
                return
            result = db_function(conn, *args)
            if on_success:
                on_success(result)
        except Exception as e:
            QMessageBox.critical(self, "Erro de Banco de Dados", f"A operação falhou:\n{e}")
        finally:
            if conn:
                conn.close()