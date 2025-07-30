from psycopg2.extras import DictCursor

def get_all(conn, table_name, fields):
    field_str = ", ".join(fields); sql = f"SELECT {field_str} FROM {table_name} ORDER BY 1"
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql); return cur.fetchall()
def get_by_id(conn, table_name, pk_name, pk_value):
    sql = f"SELECT * FROM {table_name} WHERE {pk_name} = %s"
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql, (pk_value,)); return cur.fetchone()
def add_item(conn, table_name, data):
    columns = ", ".join(data.keys()); placeholders = ", ".join(["%s"] * len(data)); sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    with conn.cursor() as cur: cur.execute(sql, list(data.values())); conn.commit()
def update_item(conn, table_name, pk_name, pk_value, data):
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()]); sql = f"UPDATE {table_name} SET {set_clause} WHERE {pk_name} = %s"
    with conn.cursor() as cur: cur.execute(sql, list(data.values()) + [pk_value]); conn.commit()
def delete_item(conn, table_name, pk_name, pk_value):
    with conn.cursor() as cur: cur.execute(f"DELETE FROM {table_name} WHERE {pk_name} = %s", (pk_value,)); conn.commit()

def get_accounts_for_user(conn, user_cpf):
    sql = "SELECT a.id, a.balance, CASE WHEN ca.id IS NOT NULL THEN 'Corrente' WHEN sa.id IS NOT NULL THEN 'Poupança' ELSE 'Indefinido' END as type FROM account a LEFT JOIN current_account ca ON a.id = ca.id LEFT JOIN savings_account sa ON a.id = sa.id WHERE a.user_id = %s ORDER BY a.id"
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql, (user_cpf,)); return cur.fetchall()
def get_account_details(conn, account_id):
    sql = "SELECT a.*, ca.*, sa.*, CASE WHEN ca.id IS NOT NULL THEN 'Corrente' WHEN sa.id IS NOT NULL THEN 'Poupança' END as type FROM account a LEFT JOIN current_account ca ON a.id = ca.id LEFT JOIN savings_account sa ON a.id = sa.id WHERE a.id = %s"
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql, (account_id,)); return cur.fetchone()
def add_new_account(conn, user_cpf, data):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO account (user_id, balance) VALUES (%s, %s) RETURNING id", (user_cpf, data['balance'])); account_id = cur.fetchone()[0]
        if data['type'] == 'Corrente': cur.execute("INSERT INTO current_account (id, monthly_income, overdraft_limit) VALUES (%s, %s, %s)", (account_id, data['monthly_income'], data['overdraft_limit']))
        elif data['type'] == 'Poupança': cur.execute("INSERT INTO savings_account (id, interest_rate, anniversary_date) VALUES (%s, %s, %s)", (account_id, data['interest_rate'], data['anniversary_date']))
        conn.commit()
def update_account(conn, account_id, data):
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE account SET balance = %s WHERE id = %s", (data['balance'], account_id))
            if data['type'] == 'Corrente': cur.execute("UPDATE current_account SET monthly_income = %s, overdraft_limit = %s WHERE id = %s", (data['monthly_income'], data['overdraft_limit'], account_id))
            elif data['type'] == 'Poupança': cur.execute("UPDATE savings_account SET interest_rate = %s, anniversary_date = %s WHERE id = %s", (data['interest_rate'], data['anniversary_date'], account_id))
            conn.commit()
        except Exception as e: conn.rollback(); raise e
def get_cards_for_account(conn, account_id):
    sql = "SELECT c.id, c.number, c.expiration_date, CASE WHEN cc.id IS NOT NULL THEN 'Crédito' WHEN dc.id IS NOT NULL THEN 'Débito' ELSE 'Indefinido' END as type FROM card c LEFT JOIN credit_card cc ON c.id = cc.id LEFT JOIN debit_card dc ON c.id = dc.id WHERE c.account_id = %s ORDER BY c.id"
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql, (account_id,)); return cur.fetchall()
def get_card_details(conn, card_id):
    sql = "SELECT c.*, cc.*, dc.*, CASE WHEN cc.id IS NOT NULL THEN 'Crédito' WHEN dc.id IS NOT NULL THEN 'Débito' END as type FROM card c LEFT JOIN credit_card cc ON c.id = cc.id LEFT JOIN debit_card dc ON c.id = dc.id WHERE c.id = %s"
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql, (card_id,)); return cur.fetchone()
def add_new_card(conn, account_id, data):
    with conn.cursor() as cur:
        cur.execute("INSERT INTO card (number, expiration_date, security_code, bank_origin, account_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", (data['number'], data['expiration_date'], data['security_code'], data['bank_origin'], account_id)); card_id = cur.fetchone()[0]
        if data['type'] == 'Crédito': cur.execute("INSERT INTO credit_card (id, current_balance, invoice_due_date, credit_limit) VALUES (%s, %s, %s, %s)", (card_id, data['current_balance'], data['invoice_due_date'], data['credit_limit']))
        elif data['type'] == 'Débito': cur.execute("INSERT INTO debit_card (id, daily_limit) VALUES (%s, %s)", (card_id, data['daily_limit']))
        conn.commit()
def update_card(conn, card_id, data):
    with conn.cursor() as cur:
        try:
            cur.execute("UPDATE card SET number = %s, expiration_date = %s, security_code = %s, bank_origin = %s WHERE id = %s", (data['number'], data['expiration_date'], data['security_code'], data['bank_origin'], card_id))
            if data['type'] == 'Crédito': cur.execute("UPDATE credit_card SET current_balance = %s, credit_limit = %s, invoice_due_date = %s WHERE id = %s", (data['current_balance'], data['credit_limit'], data['invoice_due_date'], card_id))
            elif data['type'] == 'Débito': cur.execute("UPDATE debit_card SET daily_limit = %s WHERE id = %s", (data['daily_limit'], card_id))
            conn.commit()
        except Exception as e: conn.rollback(); raise e
def get_transactions_for_account(conn, account_id):
    sql = "SELECT t.id, ta.date, c.name as category_name, t.value, t.type FROM app_transaction t JOIN transaction_account ta ON t.id = ta.transaction_id LEFT JOIN category c ON t.category_id = c.id WHERE ta.account_id = %s ORDER BY ta.date DESC, t.id DESC"
    sql = """
        -- Seleciona transações que saíram diretamente da conta
        SELECT
            t.id,
            ta.date,
            c.name AS category_name,
            t.value,
            t.type,
            'Conta' AS source,
            -- Detalhes: ID da conta de origem
            CAST(a.id AS VARCHAR) AS source_details
        FROM
            app_transaction t
        JOIN
            transaction_account ta ON t.id = ta.transaction_id
        JOIN
            account a ON ta.account_id = a.id
        LEFT JOIN
            category c ON t.category_id = c.id
        WHERE
            ta.account_id = %s

        UNION ALL

        -- Seleciona transações feitas com um cartão associado à conta
        SELECT
            t.id,
            tc.date,
            c.name AS category_name,
            t.value,
            t.type,
            'Cartão' AS source,
            -- Detalhes: 'Final' mais os 4 últimos dígitos do cartão
            CONCAT('', RIGHT(card.number, 4)) AS source_details
        FROM
            app_transaction t
        JOIN
            transaction_card tc ON t.id = tc.transaction_id
        JOIN
            card ON tc.card_id = card.id
        LEFT JOIN
            category c ON t.category_id = c.id
        WHERE
            card.account_id = %s

        ORDER BY
            date DESC, id DESC;
        """
    with conn.cursor(cursor_factory=DictCursor) as cur: cur.execute(sql, (account_id,account_id)); return cur.fetchall()
def add_transaction(conn, data):
    with conn.cursor() as cur:
        try:
            cur.execute("INSERT INTO app_transaction (value, type, installments, goal_id, category_id) VALUES (%s, %s, %s, %s, %s) RETURNING id", (data['value'], data['type'], data['installments'], data['goal_id'], data['category_id'])); transaction_id = cur.fetchone()[0]
            if data['source_type'] == 'Conta':
                cur.execute("INSERT INTO transaction_account (transaction_id, account_id, date) VALUES (%s, %s, %s)", (transaction_id, data['source_id'], data['date']))
                operator = '-' if data['type'] == 'expense' else '+'
                cur.execute(f"UPDATE account SET balance = balance {operator} %s WHERE id = %s", (data['value'], data['source_id']))
            elif data['source_type'] == 'Cartão':
                print("Adding transaction for card (%s, %s, %s)", (transaction_id, data['source_id'], data['date']))
                cur.execute("INSERT INTO transaction_card (transaction_id, card_id, date) VALUES (%s, %s, %s)", (transaction_id, data['source_id'], data['date']))
            conn.commit()
        except Exception as e: conn.rollback(); raise e

def get_goals_by_user(conn, user_cpf):
    """Busca todas as metas de um usuário específico."""
    sql = "SELECT g.id, g.name FROM goal g JOIN account a ON g.account_id = a.id WHERE a.user_id = %s ORDER BY g.name"
    with conn.cursor(cursor_factory=DictCursor) as cur:
        cur.execute(sql, (user_cpf,))
        return cur.fetchall()