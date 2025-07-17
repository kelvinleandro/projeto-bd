-- essa stored procedure transfere saldo entre duas contas, registrando a transação

CREATE OR REPLACE PROCEDURE transfer(
    p_source_account INTEGER,
    p_target_account INTEGER,
    p_amount DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_amount <= 0 THEN
        RAISE EXCEPTION 'O valor da transferência deve ser positivo';
    END IF;

    -- Verifica se há saldo suficiente
    IF (SELECT balance FROM account WHERE id = p_source_account) < p_amount THEN
        RAISE EXCEPTION 'Saldo insuficiente para a transferência';
    END IF;

    -- Debita da conta de origem
    UPDATE account
    SET balance = balance - p_amount
    WHERE id = p_source_account;

    -- Credita na conta de destino
    UPDATE account
    SET balance = balance + p_amount
    WHERE id = p_target_account;

    -- Insere a transação de débito
    INSERT INTO app_transaction (value, type)
    VALUES (p_amount, 'expense');

    INSERT INTO transaction_account (transaction_id, account_id, date)
    VALUES (
        currval('app_transaction_id_seq'),
        p_source_account,
        CURRENT_DATE
    );

    -- Insere a transação de crédito
    INSERT INTO app_transaction (value, type)
    VALUES (p_amount, 'income');

    INSERT INTO transaction_account (transaction_id, account_id, date)
    VALUES (
        currval('app_transaction_id_seq'),
        p_target_account,
        CURRENT_DATE
    );
END;
$$;
