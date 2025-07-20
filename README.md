# Desafio BiofyTech: Análise de Contratos com IA

Este projeto consiste em uma API desenvolvida em FastAPI para upload, processamento e consulta de contratos, utilizando inteligência artificial para extrair informações relevantes dos documentos. A aplicação é conteinerizada com Docker e possui um front-end para interação.

O código deste projeto foi construído pensando em: 
1. Boas práticas de programação, padrões de projeto e ***legibilidade*** do código.
2. Performance & Escalabilidade: FastAPI e uma arquitetura conteinerizada com Docker visam garantir a alta performance e a escalabilidade da aplicação.
3. Desenvolvimento Completo (Full-Cycle): Testes unitários e de integração com pytest, um sistema de migrations com Alembic e uma interface de front-end.

## Configurações:

### 1. Clone o repositório do projeto:
```bash
git clone https://github.com/Lucas-Sabbatini/DesafioBiofy
cd DesafioBiofy
```

### 2. Crie o arquivo de ambiente
O projeto utiliza um arquivo .env para gerenciar as variáveis de ambiente. Crie um novo arquivo .env na raiz do projeto com o seguinte conteúdo:
```env
SECRET_KEY=""               # Secret Key utilizada para geração de tokens JWT
GEMINI_API_KEY=""           # Sua chave da API do Gemini
ADMIN_USERNAME=""           # Credenciais de acesso iniciais do primeiro usuário da API
ADMIN_PASSWORD=""

POSTGRES_USER =""            # Credenciais do banco de dados.
POSTGRES_PASSWORD = ""
POSTGRES_DB = ""
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@db:5432/${POSTGRES_DB}"
```

### 3. Construa e inicie os contêineres:
No terminal, na raiz do projeto, execute o seguinte comando:
```bash
docker-compose up --build
```
Este comando irá:
1. Construirá a imagem do serviço da aplicação (app) com base no Dockerfile.


2. Iniciará o contêiner do banco de dados PostgreSQL (db) e aguardará até que ele esteja pronto para aceitar conexões.


3. Iniciará o contêiner da aplicação (app), que depende do banco de dados.


4. Executará as migrações do banco de dados com o Alembic.


5. Iniciará o servidor Uvicorn para servir a aplicação FastAPI na porta 8000, com hot-reloading ativado.

### 4. Acesse a aplicação
Após a inicialização completa, você pode acessar a aplicação e a documentação da API nos seguintes endereços:

- ***Front-end***: http://localhost:8000
- Documentação Interativa da API (Swagger): http://localhost:8000/docs


## Endpoints: 

### 1. POST api/v1/token
Endpoint de autenticação, enviar suas credenciais e recebe o token utilizado no header das outras requisições.
- Request body  x-www-form-urlencoded
```
grant_type -- password
string 

username *required
string
	
password *required
string($password)
	
```
- Responses:
1. 200 Successful Response
```json
{
    "access_token": "token",
    "token_type": "bearer"
}
```
2. 401 Unauthorized
```json
{
    "detail": "Incorrect username or password"
}
```
3. 422 Unprocessable Entity
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "username"
            ],
            "msg": "Field required",
            "input": null
        },
        {
            "type": "missing",
            "loc": [
                "body",
                "password"
            ],
            "msg": "Field required",
            "input": null
        }
    ]
}
```

## 2. POST /api/v1/contracts/upload
Endpoint para extrair dados cruciais de um contrato.
- Headers:<br/>
`Authorization`: `Bearer ${token}`,


- Request body  form-data
```
file *required
string($binary)
```

- Responses:
1. 200 Successful Response
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
            "inicio_servicos": "",
            ...
        },
        "termination_clause": ""
    }
}
```
2. 400 Bad Request 
```json
{
    "detail": "Could not extract text from the document."
}
```
3. 500 Internal Server Error
```json
{
    "detail": "AI returned a malformed JSON."
}
```

## 3. GET /api/v1/contracts/{contract_name}
Endpoint para recuperar dados de um contrato específico.
- Headers:<br/>
`Authorization`: `Bearer ${token}`,


- Request body  none



- Responses:
1. 200 Successful Response
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
            "inicio_servicos": "",
            ...
        },
        "termination_clause": ""
    }
}
```
2. 404 Not Found
```json
{
    "detail": "Contract 'contrato-prestacao.pasd' not found."
}
```