# ui/dialogs/add_account_dialog.py
from PySide6.QtWidgets import (QDialog, QFormLayout, QComboBox, QDialogButtonBox, 
                               QVBoxLayout, QDoubleSpinBox, QDateEdit, QWidget)
from PySide6.QtCore import QDate

class AddAccountDialog(QDialog):
    def __init__(self, parent=None, item_data=None):
        super().__init__(parent)
        self.item_data = item_data
        title = "Editar Conta" if item_data else "Adicionar Nova Conta"
        self.setWindowTitle(title)
        
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        self.type_combo = QComboBox()
        self.type_combo.addItems(["Corrente", "Poupança"])
        self.balance_spin = QDoubleSpinBox(); self.balance_spin.setRange(-9999999, 9999999)
        self.form_layout.addRow("Tipo de Conta:", self.type_combo)
        self.form_layout.addRow("Saldo:", self.balance_spin)

        self.current_account_group = QWidget()
        current_layout = QFormLayout(self.current_account_group); current_layout.setContentsMargins(0,0,0,0)
        self.monthly_income = QDoubleSpinBox(); self.monthly_income.setRange(0, 9999999)
        self.overdraft_limit = QDoubleSpinBox(); self.overdraft_limit.setRange(0, 9999999)
        current_layout.addRow("Renda Mensal:", self.monthly_income)
        current_layout.addRow("Limite Cheque Especial:", self.overdraft_limit)
        self.form_layout.addRow(self.current_account_group)

        self.savings_account_group = QWidget()
        savings_layout = QFormLayout(self.savings_account_group); savings_layout.setContentsMargins(0,0,0,0)
        self.interest_rate = QDoubleSpinBox(); self.interest_rate.setDecimals(3); self.interest_rate.setRange(0, 100)
        self.anniversary_date = QDateEdit(QDate.currentDate()); self.anniversary_date.setCalendarPopup(True)
        savings_layout.addRow("Taxa de Juros (%):", self.interest_rate)
        savings_layout.addRow("Data de Aniversário:", self.anniversary_date)
        self.form_layout.addRow(self.savings_account_group)
        
        self.main_layout.addLayout(self.form_layout)
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.main_layout.addWidget(self.buttons)

        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.type_combo.currentIndexChanged.connect(self.update_visible_fields)
        
        if self.item_data:
            self.populate_form()
        else:
            self.update_visible_fields()

    def populate_form(self):
        self.type_combo.setCurrentText(self.item_data['type'])
        self.type_combo.setEnabled(False) # Não pode mudar o tipo de uma conta existente
        self.balance_spin.setValue(float(self.item_data['balance']))

        if self.item_data['type'] == 'Corrente':
            self.monthly_income.setValue(float(self.item_data['monthly_income']))
            self.overdraft_limit.setValue(float(self.item_data['overdraft_limit']))
        else:
            self.interest_rate.setValue(float(self.item_data['interest_rate']))
            self.anniversary_date.setDate(self.item_data['anniversary_date'])
        self.update_visible_fields()

    def update_visible_fields(self):
        account_type = self.type_combo.currentText()
        self.current_account_group.setVisible(account_type == "Corrente")
        self.savings_account_group.setVisible(account_type == "Poupança")

    def get_data(self):
        data = { "type": self.type_combo.currentText(), "balance": self.balance_spin.value() }
        if data['type'] == 'Corrente':
            data.update({
                "monthly_income": self.monthly_income.value(),
                "overdraft_limit": self.overdraft_limit.value()
            })
        else:
            data.update({
                "interest_rate": self.interest_rate.value(),
                "anniversary_date": self.anniversary_date.date().toString("yyyy-MM-dd")
            })
        return data