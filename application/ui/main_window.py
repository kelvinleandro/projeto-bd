from PySide6.QtWidgets import QMainWindow, QTabWidget
from schema_definition import TABLE_SCHEMAS
from ui.components.generic_crud_widget import GenericCrudWidget
from ui.widgets.account_and_card_widget import AccountAndCardWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gerência Financeira Pessoal")
        self.setGeometry(100, 100, 1366, 768)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.account_card_tab = AccountAndCardWidget()
        self.tabs.addTab(self.account_card_tab, "Contas e Cartões")

        self.create_generic_tabs()

    def create_generic_tabs(self):
        for table_name, schema in TABLE_SCHEMAS.items():
            if schema.get("generic_tab", False):
                crud_widget = GenericCrudWidget(table_name, schema)
                self.tabs.addTab(crud_widget, schema['label'])