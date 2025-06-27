CREATE DATABASE personal_finance;

\c personal_finance

CREATE TABLE IF NOT EXISTS app_user (
    cpf CHAR(11) NOT NULL PRIMARY KEY CHECK (cpf ~ '^[0-9]{11}$'),
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    birth_date DATE NOT NULL,
    email VARCHAR(50) NOT NULL,
    tel1 VARCHAR(15) NOT NULL,
    tel2 VARCHAR(15),
    street VARCHAR(100) NOT NULL,
    street_number INTEGER NOT NULL,
    complement VARCHAR(50),
    neighborhood VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    zip_code CHAR(8) NOT NULL
);

CREATE TABLE IF NOT EXISTS account(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    balance DECIMAL (12, 3) NOT NULL DEFAULT 0,
    user_id CHAR(11) NOT NULL,

    FOREIGN KEY (user_id) REFERENCES app_user(cpf) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS current_account(
    id INTEGER NOT NULL,
    monthly_income DECIMAL (12, 3) NOT NULL DEFAULT 0,
    overdraft_limit DECIMAL (12, 3) NOT NULL DEFAULT 0,    

    FOREIGN KEY (id) REFERENCES account(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS savings_account(
    id INTEGER NOT NULL,
    interest_rate DECIMAL (12, 3) NOT NULL DEFAULT 0,
    anniversary_date DATE NOT NULL,

    FOREIGN KEY (id) REFERENCES account(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS goal(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30) NOT NULL,
    balance DECIMAL (12, 3) NOT NULL DEFAULT 0,
    target_value DECIMAL (12, 3) NOT NULL DEFAULT 0,
    date DATE NOT NULL,
    account_id INTEGER NOT NULL,

    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    number CHAR(16) NOT NULL,
    expiration_date CHAR(5) NOT NULL,
    security_code VARCHAR(3) NOT NULL,
    bank_origin VARCHAR(3) NOT NULL,
    account_id INTEGER NOT NULL,

    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS credit_card(
    id INTEGER NOT NULL,
    current_balance DECIMAL (12, 3) NOT NULL DEFAULT 0,
    invoice_due_date DATE NOT NULL,
    credit_limit DECIMAL (12, 3) NOT NULL DEFAULT 0,

    FOREIGN KEY (id) REFERENCES card(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS debit_card(
    id INTEGER NOT NULL,
    daily_limit DECIMAL (12, 3) NOT NULL DEFAULT 0,

    FOREIGN KEY (id) REFERENCES card(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS category(
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(30) NOT NULL
);

CREATE TABLE IF NOT EXISTS app_transaction (
    id INTEGER PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    value DECIMAL (12, 3) NOT NULL DEFAULT 0,
    type VARCHAR(10) CHECK (type IN ('income', 'expense')) NOT NULL,
    installments BOOLEAN NOT NULL DEFAULT FALSE,
    goal_id INTEGER,
    category_id INTEGER,

    FOREIGN KEY (goal_id) REFERENCES goal(id) ON DELETE SET NULL,
    FOREIGN KEY (category_id) REFERENCES category(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS transaction_card(
    transaction_id INTEGER NOT NULL,
    card_id INTEGER NOT NULL,
    date DATE NOT NULL,

    PRIMARY KEY (transaction_id, card_id),
    FOREIGN KEY (transaction_id) REFERENCES app_transaction(id) ON DELETE CASCADE,
    FOREIGN KEY (card_id) REFERENCES card(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transaction_account(
    transaction_id INTEGER NOT NULL,
    account_id INTEGER NOT NULL,
    date DATE NOT NULL,

    PRIMARY KEY (transaction_id, account_id),
    FOREIGN KEY (transaction_id) REFERENCES app_transaction(id) ON DELETE CASCADE,
    FOREIGN KEY (account_id) REFERENCES account(id) ON DELETE CASCADE
);

-- Índices para buscas por CPF
CREATE INDEX idx_account_user_id ON account(user_id);

-- Índices para relacionamentos comuns com JOINs
CREATE INDEX idx_goal_account_id ON goal(account_id);
CREATE INDEX idx_card_account_id ON card(account_id);

-- Índices para acesso rápido a cartões por número
CREATE INDEX idx_card_number ON card(number);

-- Índices nas tabelas de herança
CREATE INDEX idx_current_account_id ON current_account(id);
CREATE INDEX idx_savings_account_id ON savings_account(id);
CREATE INDEX idx_credit_card_id ON credit_card(id);
CREATE INDEX idx_debit_card_id ON debit_card(id);

-- Índices para filtros por data
CREATE INDEX idx_transaction_card_date ON transaction_card(date);
CREATE INDEX idx_transaction_account_date ON transaction_account(date);
CREATE INDEX idx_goal_date ON goal(date);

-- Índices para acelerar filtros por tipo de transação
CREATE INDEX idx_app_transaction_type ON app_transaction(type);

-- Índices para facilitar filtros por categoria
CREATE INDEX idx_app_transaction_category ON app_transaction(category_id);