/*
Permite a um usuário visualizar rapidamente suas últimas movimentações financeiras.

O que ela faz:

Utiliza a visão user_transaction_details para simplificar a consulta.

Filtra as transações para um usuário específico (neste caso, 'Luara Costa').

Ordena as transações pela data, da mais recente para a mais antiga.

Limita o resultado às 10 transações mais recentes.
*/

SELECT
    full_name,
    transaction_date,
    category_name,
    transaction_type,
    value
FROM
    user_transaction_details
WHERE
    full_name = 'Luara Costa'
ORDER BY
    transaction_date DESC
LIMIT 10;