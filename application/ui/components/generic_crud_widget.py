from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox, QMenu
from PySide6.QtCore import Qt
from database.connection import get_db_connection
import database.generic_operations as db
from ui.components.generic_form_dialog import GenericFormDialog

class GenericCrudWidget(QWidget):
    def __init__(self, table_name, schema, parent=None):
        super().__init__(parent)
        self.table_name = table_name
        self.schema = schema
        self.pk_name = schema['pk']
        
        self.layout = QVBoxLayout(self)
        
        self.add_button = QPushButton(f"Adicionar Novo(a) {schema['label'][:-1]}")
        self.add_button.clicked.connect(self.add_item)
        
        self.table = QTableWidget()
        self.table.setColumnCount(len(schema['fields']))
        self.table.setHorizontalHeaderLabels([props['label'] for props in schema['fields'].values()])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_menu)
        
        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.table)
        self.refresh_data()

    def refresh_data(self):
        conn = get_db_connection()
        try:
            items = db.get_all(conn, self.table_name, list(self.schema['fields'].keys()))
            self.table.setRowCount(len(items))
            for row, item_data in enumerate(items):
                for col, field_name in enumerate(self.schema['fields'].keys()):
                    self.table.setItem(row, col, QTableWidgetItem(str(item_data[field_name])))
        finally:
            conn.close()

    def add_item(self):
        dialog = GenericFormDialog(self.schema, self)
        if dialog.exec():
            data = dialog.get_data()
            if data is None: return
            conn = get_db_connection()
            try:
                db.add_item(conn, self.table_name, data)
                self.refresh_data()
            finally:
                conn.close()

    def edit_item(self):
        selected_row = self.table.currentRow()
        if selected_row < 0: return
        pk_value = self.table.item(selected_row, list(self.schema['fields'].keys()).index(self.pk_name)).text()
        
        conn = get_db_connection()
        try:
            item_data = db.get_by_id(conn, self.table_name, self.pk_name, pk_value)
            dialog = GenericFormDialog(self.schema, self, item_data=item_data)
            if dialog.exec():
                data = dialog.get_data()
                if data is None: return
                db.update_item(conn, self.table_name, self.pk_name, pk_value, data)
                self.refresh_data()
        finally:
            conn.close()

    def delete_item(self):
        selected_row = self.table.currentRow()
        if selected_row < 0: return
        pk_value = self.table.item(selected_row, list(self.schema['fields'].keys()).index(self.pk_name)).text()

        reply = QMessageBox.question(self, 'Confirmar Deleção', f"Tem certeza que deseja deletar o item com ID {pk_value}?")
        if reply == QMessageBox.Yes:
            conn = get_db_connection()
            try:
                db.delete_item(conn, self.table_name, self.pk_name, pk_value)
                self.refresh_data()
            finally:
                conn.close()

    def open_menu(self, position):
        menu = QMenu()
        edit_action = menu.addAction("Editar")
        delete_action = menu.addAction("Deletar")
        action = menu.exec(self.table.mapToGlobal(position))
        if action == edit_action: self.edit_item()
        elif action == delete_action: self.delete_item()