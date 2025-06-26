1. inicializar

    ```sh
    docker compose up -d
    ```

2. no navegador:

    ```sh
    http://localhost:5050
    ```

3. usar as credenciais do pgAdmin (do docker-compose) no login

4. (1ª vez) criar novo server e BD

    4.1 Botão do mouse direito em servers -> Register -> Server...

    4.2 General -> Name = `projeto_bd`

    4.3 General -> Host Name = `postgres` (nome do serviço)

    4.4 General -> Port = `5432`
    
    4.5 General -> Username e Password do postgres (do docker-compose)

    4.6 Botão do mouse direito em `projeto_bd` -> Create -> Database

    4.7 Database = `personal_finance`
