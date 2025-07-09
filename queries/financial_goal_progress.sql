/*Esta consulta motivacional mostra o quão perto os usuários estão de alcançar suas metas financeiras.

O que ela faz:

Calcula a porcentagem do valor da meta que já foi alcançada.

Junta informações da meta com os dados do usuário para identificação.

Exibe o nome do usuário, o nome da meta, o valor atual, o valor alvo e a porcentagem de conclusão da meta.
*/


SELECT
    u.first_name,
    u.last_name,
    g.name AS goal_name,
    g.balance AS current_value,
    g.target_value,
    round((g.balance / g.target_value) * 100, 2) AS progress_percentage
FROM
    goal g
JOIN
    account a ON g.account_id = a.id
JOIN
    app_user u ON a.user_id = u.cpf
ORDER BY
    progress_percentage DESC;