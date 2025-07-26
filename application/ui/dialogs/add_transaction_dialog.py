from PySide6.QtWidgets import (QDialog, QFormLayout, QComboBox, QDialogButtonBox, 
                               QVBoxLayout, QDoubleSpinBox, QDateEdit, QCheckBox)
from PySide6.QtCore import QDate
from database.connection import get_db_connection
import database.generic_operations as db

class AddTransactionDialog(QDialog):
    def __init__(self, user_cpf, parent=None):
        super().__init__(parent)
        self.user_cpf = user_cpf
        self.setWindowTitle("Adicionar Nova Transação")
        
        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        self.source_type_combo = QComboBox(); self.source_type_combo.addItems(["Conta", "Cartão"])
        self.source_combo = QComboBox()
        self.value_spin = QDoubleSpinBox(); self.value_spin.setRange(0.01, 999999999)
        self.type_combo = QComboBox(); self.type_combo.addItems(["expense", "income"])
        self.category_combo = QComboBox()
        self.goal_combo = QComboBox()
        self.installments_check = QCheckBox()
        self.date_edit = QDateEdit(QDate.currentDate()); self.date_edit.setCalendarPopup(True)

        form_layout.addRow("Origem da Transação*:", self.source_type_combo)
        form_layout.addRow("Conta/Cartão de Origem*:", self.source_combo)
        form_layout.addRow("Valor*:", self.value_spin)
        form_layout.addRow("Tipo*:", self.type_combo)
        form_layout.addRow("Categoria:", self.category_combo)
        form_layout.addRow("Meta Associada:", self.goal_combo)
        form_layout.addRow("Parcelado?", self.installments_check)
        form_layout.addRow("Data*:", self.date_edit)
        
        layout.addLayout(form_layout)
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.source_type_combo.currentIndexChanged.connect(self.update_source_combo)
        self.load_combos()

    def load_combos(self):
        conn = get_db_connection()
        if not conn: return
        try:
            self.accounts = db.get_accounts_for_user(conn, self.user_cpf)
            self.cards = []
            for acc in self.accounts:
                self.cards.extend(db.get_cards_for_account(conn, acc['id']))
            
            categories = db.get_all(conn, "category", ["id", "name"])
            self.category_combo.addItem("Nenhuma", None)
            for cat in categories: self.category_combo.addItem(cat['name'], cat['id'])
            
            goals = db.get_goals_by_user(conn, self.user_cpf)
            self.goal_combo.addItem("Nenhuma", None)
            for goal in goals: self.goal_combo.addItem(goal['name'], goal['id'])

        finally: conn.close()
        self.update_source_combo()

    def update_source_combo(self):
        self.source_combo.clear()
        source_type = self.source_type_combo.currentText()
        if source_type == 'Conta':
            for acc in self.accounts: self.source_combo.addItem(f"Conta ID {acc['id']} ({acc['type']})", acc['id'])
        elif source_type == 'Cartão':
            for card in self.cards: self.source_combo.addItem(f"Cartão Final {card['number'][-4:]} ({card['type']})", card['id'])

    def get_data(self):
        return {
            "source_type": self.source_type_combo.currentText(),
            "source_id": self.source_combo.currentData(),
            "value": self.value_spin.value(),
            "type": self.type_combo.currentText(),
            "category_id": self.category_combo.currentData(),
            "goal_id": self.goal_combo.currentData(),
            "installments": self.installments_check.isChecked(),
            "date": self.date_edit.date().toString("yyyy-MM-dd")
        }