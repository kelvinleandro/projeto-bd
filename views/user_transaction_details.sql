/*
Esta visão foi criada para consolidar as informações de transações, usuários e categorias em um só lugar, 
facilitando a criação de consultas sobre os detalhes das transações sem a necessidade de realizar junções complexas todas as vezes.

O que ela faz:

Junta as tabelas app_user, account, transaction_account, app_transaction, e category.

Cria uma visão que exibe o nome completo do usuário, o tipo de conta, o valor e tipo da transação,
 e o nome da categoria para cada transação registrada em uma conta.
*/

CREATE VIEW user_transaction_details AS
SELECT
    u.first_name || ' ' || u.last_name AS full_name,
    a.id AS account_id,
    CASE
        WHEN ca.id IS NOT NULL THEN 'Corrente'
        WHEN sa.id IS NOT NULL THEN 'Poupança'
        ELSE 'Não especificada'
    END AS account_type,
    t.value,
    t.type AS transaction_type,
    c.name AS category_name,
    ta.date AS transaction_date
FROM
    app_user u
JOIN
    account a ON u.cpf = a.user_id
JOIN
    transaction_account ta ON a.id = ta.account_id
JOIN
    app_transaction t ON ta.transaction_id = t.id
JOIN
    category c ON t.category_id = c.id
LEFT JOIN
    current_account ca ON a.id = ca.id
LEFT JOIN
    savings_account sa ON a.id = sa.id;


-- Queries
/*


SELECT * FROM user_transaction_details;



SELECT *
FROM user_transaction_details
WHERE full_name = 'Luara Costa';



SELECT *
FROM user_transaction_details
WHERE category_name = 'Health' AND transaction_type = 'expense';



SELECT
    transaction_date,
    value,
    category_name
FROM
    user_transaction_details
WHERE
    transaction_type = 'income';



SELECT
    full_name,
    SUM(value) AS total_spent
FROM
    user_transaction_details
WHERE
    transaction_type = 'expense'
GROUP BY
    full_name
ORDER BY
    total_spent DESC;

    SELECT
    category_name,
    COUNT(*) AS number_of_transactions
FROM
    user_transaction_details
GROUP BY
    category_name
ORDER BY
    number_of_transactions DESC;

    
*/