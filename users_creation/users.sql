-- Criar o usuário admin_user
CREATE USER admin_user WITH PASSWORD 'admin123';

-- Conceder acesso total
GRANT CONNECT ON DATABASE personal_finance TO admin_user;

-- Conceder permissões em todas as tabelas, sequences e funções
GRANT USAGE ON SCHEMA public TO admin_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO admin_user;

-- Tornar permissões futuras automáticas
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin_user;

-- Criar o usuário read_user
CREATE USER read_user WITH PASSWORD 'read123';

-- Conceder acesso somente de leitura
GRANT CONNECT ON DATABASE personal_finance TO read_user;
GRANT USAGE ON SCHEMA public TO read_user;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO read_user;

-- Tornar SELECT padrão para novas tabelas
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO read_user;