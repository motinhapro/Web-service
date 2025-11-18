# Middleware Web Service - Integração Legado com Criptografia

Este projeto implementa um Middleware Web Service RESTful desenvolvido como requisito da disciplina. O sistema atua como uma ponte segura entre Clientes Externos (que comunicam via JSON) e um Sistema Legado Simulado (que comunica via XML), garantindo a confidencialidade dos dados sensíveis através de criptografia.

---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** FastAPI (API REST e documentação automática via Swagger UI)
* **Servidor:** Uvicorn (Servidor ASGI)
* **Criptografia:** Biblioteca `cryptography` (Implementação do algoritmo Fernet/AES)
* **Parser:** Biblioteca `xmltodict` (Conversão bidirecional JSON <-> XML)

---

## 🚀 Como Executar o Projeto

### 1. Clonar e Configurar o Ambiente
Este projeto utiliza um ambiente virtual para garantir o isolamento das dependências. Siga os passos abaixo no seu terminal:

```bash
# 1. Clone o repositório (caso tenha baixado via git)
git clone [https://github.com/motinhapro/Web-service/settings]
cd NOME-DO-REPO

# 2. Crie o ambiente virtual
python -m venv venv

# 3. Ative o ambiente virtual
# No Windows (PowerShell ou CMD):
venv\Scripts\activate
# No Linux ou Mac:
source venv/bin/activate

# 4. Instale as dependências necessárias
pip install -r requirements.txt
```

### 2. Rodar a Aplicação
Com o ambiente virtual ativado, inicie o servidor executando o comando abaixo na raiz do projeto:

```bash
uvicorn main:app --reload
```

O servidor estará rodando localmente em: `http://127.0.0.1:8000`

### 3. Testar a API (Documentação Interativa)
O projeto utiliza o Swagger UI para facilitar os testes sem a necessidade de ferramentas externas.

1.  Acesse **http://127.0.0.1:8000/docs** no seu navegador.
2.  Clique no botão **Authorize** (ícone de cadeado 🔒) no canto superior direito.
3.  Insira o token de autenticação (fixo para fins acadêmicos):
    * **Value:** `token-secreto-123`
4.  Clique em **Authorize** e depois em **Close**.
5.  Agora você pode utilizar os botões **"Try it out"** e **"Execute"** nos endpoints listados abaixo.

---

## 🔐 Detalhes da Criptografia

Para garantir a confidencialidade dos dados sensíveis exigida no projeto, foram implementadas as seguintes medidas:

* **Algoritmo:** Foi utilizada criptografia simétrica **AES** (Advanced Encryption Standard) através da implementação **Fernet** (AES-128 em modo CBC com assinatura HMAC-SHA256 para integridade).
* **Gerenciamento de Chaves:** Uma chave simétrica é gerada na inicialização da aplicação. *Nota: Em um ambiente de produção real, esta chave seria injetada via variáveis de ambiente seguras (Secrets).*
* **Fluxo de Dados:**
    * **Envio (POST):** O middleware recebe o CPF em texto plano (JSON), criptografa-o e insere o hash resultante no XML enviado ao sistema legado.
    * **Consulta (GET):** O middleware recebe o XML do legado contendo o CPF criptografado, descriptografa a informação utilizando a chave secreta e retorna o dado legível no JSON para o cliente autenticado.

---

## 🌐 Segurança da Comunicação (HTTPS e Auth)

1.  **Autenticação:**
    * Utiliza-se o padrão **Bearer Token** no cabeçalho `Authorization`.
    * O middleware valida o token antes de processar qualquer requisição de negócio.

2.  **HTTPS (TLS):**
    * O projeto atual executa em HTTP para fins de desenvolvimento local.
    * **Em Produção:** A segurança da camada de transporte seria garantida configurando um **Proxy Reverso** (como Nginx ou Apache) ou um Load Balancer à frente da aplicação Python. Este proxy seria responsável por gerenciar os certificados SSL/TLS, terminando a conexão segura na porta 443 e repassando o tráfego para a aplicação interna.

---

## 📡 Exemplos de Requisições

### 1. Cadastro de Cliente
* **Método:** `POST`
* **Endpoint:** `/api/clientes`
* **Corpo da Requisição (JSON):**
```json
{
  "nome": "Carlos Silva",
  "cpf": "123.456.789-00",
  "email": "carlos@email.com"
}
```
* **Comportamento:** O CPF "123.456.789-00" é convertido para um hash (ex: `gAAAAABl...`) antes de ser enviado ao legado via XML.

### 2. Consulta de Cliente
* **Método:** `GET`
* **Endpoint:** `/api/clientes/{id}`
* **Retorno (JSON):**
```json
{
  "cliente": {
    "id": "1",
    "nome": "Maria da Silva",
    "situacao": "ATIVO",
    "cpf_real": "123.456.789-00"
  }
}
```
* **Comportamento:** O sistema busca o XML criptografado, descriptografa o campo `<cpf_s>` e retorna o valor original no campo `cpf_real`.

---

## 📋 Autor
Trabalho acadêmico desenvolvido para a disciplina de Web Services.