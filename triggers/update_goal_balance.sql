-- atualiza o saldo da meta automaticamente sempre que uma transação for vinculada a ela

-- funcao do gatilho
CREATE OR REPLACE FUNCTION update_goal_balance()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.type = 'income' AND NEW.goal_id IS NOT NULL THEN
        UPDATE goal
        SET balance = balance + NEW.value
        WHERE id = NEW.goal_id;
    ELSIF NEW.type = 'expense' AND NEW.goal_id IS NOT NULL THEN
        UPDATE goal
        SET balance = balance - NEW.value
        WHERE id = NEW.goal_id;
    END IF;

    RETURN NEW;
END;
$$;

-- criacao do gatilho
CREATE TRIGGER trg_update_goal_balance
AFTER INSERT ON app_transaction
FOR EACH ROW
EXECUTE FUNCTION update_goal_balance();
