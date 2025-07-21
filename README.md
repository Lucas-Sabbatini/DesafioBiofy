# Desafio BiofyTech: Análise de Contratos com IA

Este projeto consiste em uma API desenvolvida em FastAPI para upload, processamento e consulta de contratos, utilizando inteligência artificial para extrair informações relevantes dos documentos. A aplicação é conteinerizada com Docker e possui um front-end para interação.


### O código deste projeto foi construído pensando em:

- **Boas práticas de programação**, padrões de projeto e ***legibilidade*** do código.
- **Performance & Escalabilidade**: FastAPI e uma arquitetura conteinerizada com Docker visam garantir a alta performance e a escalabilidade da aplicação.
- **Desenvolvimento Completo (Full-Cycle)**: Testes unitários e de integração com pytest, um sistema de migrations com Alembic e uma interface de front-end.

---

## Configuração do Projeto

### 1. Clone o repositório
```bash
git clone https://github.com/Lucas-Sabbatini/DesafioBiofy
cd DesafioBiofy
```

### 2. Crie o arquivo de ambiente `.env`
O projeto utiliza um arquivo `.env` para gerenciar as variáveis de ambiente. Crie um novo arquivo na raiz do projeto com o seguinte conteúdo:

```env
SECRET_KEY=""               # Secret Key utilizada para geração de tokens JWT
GEMINI_API_KEY=""           # Sua chave da API do Gemini
ADMIN_USERNAME=""           # Usuário inicial da API
ADMIN_PASSWORD=""           # Senha inicial da API

POSTGRES_USER =""           # Usuário do banco de dados
POSTGRES_PASSWORD = ""      # Senha do banco de dados
POSTGRES_DB = ""            # Nome do banco de dados
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
```

### 3. Construa e inicie os contêineres
Na raiz do projeto, execute:

```bash
docker compose up --build
```

Esse comando irá:
1. Construir a imagem da aplicação (app) via Dockerfile.
2. Iniciar o banco de dados PostgreSQL (db) e aguardar sua prontidão.
3. Iniciar a aplicação (app), que depende do banco de dados.
4. Executar as migrações do banco com Alembic.
5. Iniciar o servidor Uvicorn (FastAPI) na porta 8000, com hot-reloading.

### 4. Acesse a aplicação
- **Front-end:** [http://localhost:8000](http://localhost:8000)
- **Swagger (API Docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Executando os testes
Para rodar os testes unitários e de integração:

```bash
pytest
```

---

## Endpoints da API

### 1. Autenticação
#### `POST /api/v1/token`
Envie suas credenciais para receber o token JWT.

- **Request body** (`x-www-form-urlencoded`):
  - `grant_type`: password
  - `username` *(obrigatório)*
  - `password` *(obrigatório)*

- **Exemplo de resposta 200:**
```json
{
  "access_token": "token",
  "token_type": "bearer"
}
```

- **Erros comuns:**
  - `401 Unauthorized`
    ```json
    { "detail": "Incorrect username or password" }
    ```
  - `422 Unprocessable Entity`
    ```json
    {
      "detail": [
        { "type": "missing", "loc": ["body", "username"], "msg": "Field required", "input": null },
        { "type": "missing", "loc": ["body", "password"], "msg": "Field required", "input": null }
      ]
    }
    ```

---

### 2. Upload e Extração de Contrato
#### `POST /api/v1/contracts/upload`
Extrai dados cruciais de um contrato enviado.

- **Headers:**
  - `Authorization: Bearer {token}`
- **Request body:** (`form-data`)
  - `file` *(obrigatório, form-data, binário)*

- **Exemplo de resposta 200:**
```json
{
  "file_name": "contrato-prestacao.pdf",
  "id": 2,
  "uploaded_at": "2025-07-20T20:49:00.852068",
  "contract_data": {
    "parties": ["str"],
    "monetary_values": ["str"],
    "main_obligations": ["str"],
    "additional_data": {
      "tipo_contrato": "",
      "objeto": "",
      "vigencia": "",
      "data_assinatura": "",
      "local_assinatura": "",
      "inicio_servicos": ""
      // ...
    },
    "termination_clause": ""
  }
}
```

- **Erros comuns:**
  - `400 Bad Request`
    ```json
    { "detail": "Could not extract text from the document." }
    ```
  - `500 Internal Server Error`
    ```json
    { "detail": "AI returned a malformed JSON." }
    ```

---

### 3. Consulta de Contrato Específico
#### `GET /api/v1/contracts/{contract_name}`
Recupera dados de um contrato específico pelo nome.
**Importante**: A extensão do arquivo (.pdf ou .docx) faz parte do contract_name!

- **Headers:**
  - `Authorization: Bearer {token}`
- **Request body:**
  - *nenhum*

- **Exemplo de resposta 200:**
```json
{
  "file_name": "contrato-prestacao.pdf",
  "id": 2,
  "uploaded_at": "2025-07-20T20:49:00.852068",
  "contract_data": {
    "parties": ["str"],
    "monetary_values": ["str"],
    "main_obligations": ["str"],
    "additional_data": {
      "tipo_contrato": "",
      "objeto": "",
      "vigencia": "",
      "data_assinatura": "",
      "local_assinatura": "",
      "inicio_servicos": ""
      // ...
    },
    "termination_clause": ""
  }
}
```

- **Erro 404:**
  ```json
  { "detail": "Contract 'contrato-prestacao.pasd' not found." }
  ```



---

<p align="center">
  <b>Desenvolvido por Lucas Sabbatini para o Desafio BiofyTech</b>
</p>
