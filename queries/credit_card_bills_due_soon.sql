/*
Consulta muito útil para o dia a dia, permitindo ao usuário se planejar para pagar as faturas do cartão de crédito que estão prestes a vencer.

O que ela faz:

Seleciona informações de cartões de crédito.

Filtra os cartões cuja fatura vence no mês atual (Julho de 2025, de acordo com a data do sistema).

Junta os dados com a tabela de usuário para mostrar a quem pertence o cartão.

Exibe o nome do titular, o saldo atual da fatura, o limite de crédito e a data de vencimento.
*/


SELECT
    u.first_name,
    u.last_name,
    cc.current_balance,
    cc.credit_limit,
    cc.invoice_due_date
FROM
    credit_card cc
JOIN
    card c ON cc.id = c.id
JOIN
    account a ON c.account_id = a.id
JOIN
    app_user u ON a.user_id = u.cpf
WHERE
    TO_CHAR(cc.invoice_due_date, 'YYYY-MM') = TO_CHAR(CURRENT_DATE, 'YYYY-MM') -- modify the date to the desired month and year
ORDER BY
    cc.invoice_due_date ASC;