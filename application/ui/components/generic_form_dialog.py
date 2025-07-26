from PySide6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QVBoxLayout, 
                               QDateEdit, QDoubleSpinBox, QComboBox, QCheckBox, QMessageBox)
from PySide6.QtCore import QDate
from database.connection import get_db_connection
from database.generic_operations import get_all

class GenericFormDialog(QDialog):
    def __init__(self, schema, parent=None, item_data=None):
        super().__init__(parent)
        self.schema = schema
        self.item_data = item_data
        self.setWindowTitle(f"{'Editar' if item_data else 'Adicionar'} {schema['label']}")
        
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()
        self.widgets = {}

        self.conn = get_db_connection()
        self.create_form()
        self.layout.addLayout(self.form_layout)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)
        if self.conn: self.conn.close()

    def create_form(self):
        for field_name, props in self.schema['fields'].items():
            if props.get("readonly"): continue

            label = props['label']
            field_type = props['type']
            widget = None

            if field_type == 'str':
                widget = QLineEdit()
                if props.get("placeholder"): widget.setPlaceholderText(props.get("placeholder"))
            elif field_type == 'int':
                widget = QDoubleSpinBox(); widget.setDecimals(0)
                widget.setRange(0, 999999999)
            elif field_type == 'float':
                widget = QDoubleSpinBox(); widget.setDecimals(2)
                widget.setRange(0, 999999999.99) 
            elif field_type == 'date':
                widget = QDateEdit(QDate.currentDate()); widget.setCalendarPopup(True)
            elif field_type == 'bool':
                widget = QCheckBox()
            elif field_type == 'combo':
                widget = QComboBox()
                widget.addItems(props['options'])
            elif field_type == 'fk':
                widget = QComboBox()
                widget.addItem("Selecione...", None)
                fk_table = props['fk_table']
                fk_label_field = props['fk_label']
                fk_pk = self.get_pk_for_table(fk_table)
                if self.conn:
                    items = get_all(self.conn, fk_table, [fk_pk, fk_label_field])
                    for item in items:
                        widget.addItem(str(item[fk_label_field]), item[fk_pk])

            if widget:
                self.form_layout.addRow(label, widget)
                self.widgets[field_name] = widget
        
        if self.item_data: self.populate_form()

    def populate_form(self):
        for field_name, widget in self.widgets.items():
            value = self.item_data.get(field_name)
            if value is None: continue

            if isinstance(widget, QLineEdit): widget.setText(str(value))
            elif isinstance(widget, QDoubleSpinBox): widget.setValue(float(value))
            elif isinstance(widget, QDateEdit): widget.setDate(QDate.fromString(str(value), "yyyy-MM-dd"))
            elif isinstance(widget, QCheckBox): widget.setChecked(bool(value))
            elif isinstance(widget, QComboBox):
                index = widget.findData(value) if self.schema['fields'][field_name]['type'] == 'fk' else widget.findText(str(value))
                if index != -1: widget.setCurrentIndex(index)

    def get_data(self):
        data = {}
        for field_name, widget in self.widgets.items():
            props = self.schema['fields'][field_name]
            value = None
            if isinstance(widget, QLineEdit): value = widget.text()
            elif isinstance(widget, QDoubleSpinBox): value = widget.value()
            elif isinstance(widget, QDateEdit): value = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QCheckBox): value = widget.isChecked()
            elif isinstance(widget, QComboBox):
                value = widget.currentData() if props['type'] == 'fk' else widget.currentText()
            
            if props.get("required") and (value is None or value == ""):
                QMessageBox.warning(self, "Campo Obrigatório", f"O campo '{props['label']}' é obrigatório.")
                return None
            
            if value != "": data[field_name] = value
        return data

    def get_pk_for_table(self, table_name):
        from schema_definition import TABLE_SCHEMAS
        return TABLE_SCHEMAS[table_name]['pk']