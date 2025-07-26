from PySide6.QtWidgets import (QDialog, QFormLayout, QComboBox, QDialogButtonBox, 
                               QVBoxLayout, QDoubleSpinBox, QDateEdit, QWidget, QLineEdit)
from PySide6.QtCore import QDate

class AddCardDialog(QDialog):
    def __init__(self, parent=None, item_data=None):
        super().__init__(parent)
        self.item_data = item_data
        title = "Editar Cartão" if item_data else "Adicionar Novo Cartão"
        self.setWindowTitle(title)
        
        self.main_layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()


        self.type_combo = QComboBox()
        self.type_combo.addItems(["Crédito", "Débito"])
        self.number = QLineEdit()
        self.expiration_date = QLineEdit(); self.expiration_date.setPlaceholderText("MM/AA")
        self.security_code = QLineEdit()
        self.bank_origin = QLineEdit()
        self.form_layout.addRow("Tipo de Cartão:", self.type_combo)
        self.form_layout.addRow("Número:", self.number)
        self.form_layout.addRow("Data de Expiração:", self.expiration_date)
        self.form_layout.addRow("Cód. Segurança:", self.security_code)
        self.form_layout.addRow("Banco de Origem:", self.bank_origin)

        self.credit_group = QWidget()
        credit_layout = QFormLayout(self.credit_group); credit_layout.setContentsMargins(0,0,0,0)
        self.current_balance = QDoubleSpinBox(); self.current_balance.setRange(0, 9999999)
        self.credit_limit = QDoubleSpinBox(); self.credit_limit.setRange(0, 9999999)
        self.invoice_due_date = QDateEdit(QDate.currentDate()); self.invoice_due_date.setCalendarPopup(True)
        credit_layout.addRow("Saldo Atual:", self.current_balance)
        credit_layout.addRow("Limite de Crédito:", self.credit_limit)
        credit_layout.addRow("Vencimento da Fatura:", self.invoice_due_date)
        self.form_layout.addRow(self.credit_group)

        self.debit_group = QWidget()
        debit_layout = QFormLayout(self.debit_group); debit_layout.setContentsMargins(0,0,0,0)
        self.daily_limit = QDoubleSpinBox(); self.daily_limit.setRange(0, 9999999)
        debit_layout.addRow("Limite Diário:", self.daily_limit)
        self.form_layout.addRow(self.debit_group)
        
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
        self.type_combo.setEnabled(False)
        self.number.setText(self.item_data['number'])
        self.expiration_date.setText(self.item_data['expiration_date'])
        self.security_code.setText(self.item_data['security_code'])
        self.bank_origin.setText(self.item_data['bank_origin'])

        if self.item_data['type'] == 'Crédito':
            self.current_balance.setValue(float(self.item_data['current_balance']))
            self.credit_limit.setValue(float(self.item_data['credit_limit']))
            self.invoice_due_date.setDate(self.item_data['invoice_due_date'])
        else:
            self.daily_limit.setValue(float(self.item_data['daily_limit']))
        self.update_visible_fields()

    def update_visible_fields(self):
        card_type = self.type_combo.currentText()
        self.credit_group.setVisible(card_type == "Crédito")
        self.debit_group.setVisible(card_type == "Débito")

    def get_data(self):
        data = { "type": self.type_combo.currentText(), "number": self.number.text(), "expiration_date": self.expiration_date.text(), "security_code": self.security_code.text(), "bank_origin": self.bank_origin.text() }
        if data['type'] == 'Crédito':
            data.update({ "current_balance": self.current_balance.value(), "credit_limit": self.credit_limit.value(), "invoice_due_date": self.invoice_due_date.date().toString("yyyy-MM-dd") })
        else:
            data.update({ "daily_limit": self.daily_limit.value() })
        return data