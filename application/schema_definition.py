# schema_definition.py
TABLE_SCHEMAS = {
    "account": {
        "label": "Contas", "pk": "id", "generic_tab": False,
        "fields": { "id": {"label": "ID", "type": "int", "readonly": True}, "balance": {"label": "Saldo", "type": "float", "required": True, "default": 0}, "user_id": {"label": "Usuário", "type": "fk", "required": True, "fk_table": "app_user", "fk_label": "first_name"}, }
    },
    "card": {
        "label": "Cartões", "pk": "id", "generic_tab": False,
        "fields": { "id": {"label": "ID", "type": "int", "readonly": True}, "number": {"label": "Número", "type": "str", "required": True, "max_length": 16}, "expiration_date": {"label": "Expiração", "type": "str", "required": True, "placeholder": "MM/AA", "max_length": 5}, "security_code": {"label": "CVV", "type": "str", "required": True, "max_length": 3}, "bank_origin": {"label": "Banco", "type": "str", "required": True, "max_length": 3}, "account_id": {"label": "Conta Associada", "type": "fk", "required": True, "fk_table": "account", "fk_label": "id"}, }
    },
    "app_user": {
        "label": "Usuários", "pk": "cpf", "generic_tab": True,
        "fields": {
            "cpf": {"label": "CPF", "type": "str", "required": True, "max_length": 11},
            "first_name": {"label": "Nome", "type": "str", "required": True, "max_length": 30},
            "last_name": {"label": "Sobrenome", "type": "str", "required": True, "max_length": 30},
            "birth_date": {"label": "Data de Nasc.", "type": "date", "required": True},
            "email": {"label": "Email", "type": "str", "required": True, "max_length": 50},
            "tel1": {"label": "Telefone 1", "type": "str", "required": True, "max_length": 15},
            "tel2": {"label": "Telefone 2", "type": "str", "max_length": 15},
            "street": {"label": "Rua", "type": "str", "required": True, "max_length": 100},
            "street_number": {"label": "Número", "type": "int", "required": True},
            "complement": {"label": "Complemento", "type": "str", "max_length": 50},
            "neighborhood": {"label": "Bairro", "type": "str", "required": True, "max_length": 50},
            "city": {"label": "Cidade", "type": "str", "required": True, "max_length": 50},
            "state": {"label": "Estado", "type": "str", "required": True, "max_length": 2},
            "zip_code": {"label": "CEP", "type": "str", "required": True, "max_length": 8},
        }
    },
    "category": {
        "label": "Categorias", "pk": "id", "generic_tab": True,
        "fields": { "id": {"label": "ID", "type": "int", "readonly": True}, "name": {"label": "Nome", "type": "str", "required": True, "max_length": 30}, }
    },
    "goal": {
        "label": "Metas", "pk": "id", "generic_tab": True,
        "fields": {
            "id": {"label": "ID", "type": "int", "readonly": True},
            "name": {"label": "Nome da Meta", "type": "str", "required": True, "max_length": 30},
            "balance": {"label": "Valor Atual", "type": "float", "required": True, "default": 0},
            "target_value": {"label": "Valor Alvo", "type": "float", "required": True, "default": 0},
            "date": {"label": "Data Alvo", "type": "date", "required": True},
            "account_id": {"label": "Conta Associada", "type": "fk", "required": True, "fk_table": "account", "fk_label": "id"},
        }
    }
}