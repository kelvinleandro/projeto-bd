/*
Saldo Consolidado por Usuário

Esta é uma consulta essencial para obter uma visão geral da saúde financeira de cada usuário.

O que ela faz:

Agrupa as contas por usuário.

Soma o saldo de todas as contas (corrente e poupança) de cada usuário.

Exibe o nome do usuário e seu saldo total consolidado, ordenado do mais rico para o mais pobre.
*/

SELECT
    u.first_name,
    u.last_name,
    SUM(a.balance) AS total_balance
FROM
    app_user u
JOIN
    account a ON u.cpf = a.user_id
GROUP BY
    u.first_name, u.last_name
ORDER BY
    total_balance DESC;