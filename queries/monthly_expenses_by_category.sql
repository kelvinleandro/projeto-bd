/*
Essa consulta ajuda o usuário a entender para onde seu dinheiro está indo, detalhando os gastos por categoria em um determinado mês.

O que ela faz:

Filtra as transações de um usuário específico (neste caso, 'Luigi Guerra').

Seleciona apenas as transações de 'despesa' (expense) que ocorreram em um mês e ano específicos.

Agrupa os gastos por categoria e soma os valores, mostrando onde o usuário mais gastou.
*/

SELECT
    c.name AS category,
    SUM(t.value) AS total_spent
FROM
    app_transaction t
JOIN
    category c ON t.category_id = c.id
JOIN
    transaction_account ta ON t.id = ta.transaction_id
JOIN
    account a ON ta.account_id = a.id
JOIN
    app_user u ON a.user_id = u.cpf
WHERE
    u.first_name = 'Luigi' AND u.last_name = 'Guerra'
    AND t.type = 'expense'
    AND TO_CHAR(ta.date, 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM') -- modify the date to the desired month and year
GROUP BY
    c.name
ORDER BY
    total_spent DESC;