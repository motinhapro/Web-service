from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from cryptography.fernet import Fernet
import xmltodict

app = FastAPI(
    title="Middleware Criptografia",
    description="API segura com autenticação Bearer para comunicação XML.",
    version="1.0.0"
)

# Chave de Criptografia
CHAVE_SECRETA = Fernet.generate_key()
cipher_suite = Fernet(CHAVE_SECRETA)

# Token de Autenticação
API_TOKEN = "token-secreto-123"

# Isso cria o botão de cadeado no Swagger automaticamente
security_scheme = HTTPBearer()

def criptografar(texto: str) -> str:
    if not texto: return ""
    return cipher_suite.encrypt(texto.encode()).decode()

def descriptografar(texto_cripto: str) -> str:
    if not texto_cripto: return ""
    return cipher_suite.decrypt(texto_cripto.encode()).decode()

async def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """
    Valida o token automaticamente. 
    O usuário só digita o token, o FastAPI cuida do 'Bearer'.
    """
    token = credenciais.credentials
    if token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Token inválido")
    return token

class SistemaLegadoSimulado:
    def enviar_xml(self, xml_string: str):
        print(f"\n[LEGADO] Recebi XML Criptografado:\n{xml_string}")
        return """<resposta><status>SUCESSO</status><id>998877</id></resposta>"""

    def buscar_xml(self, id_cliente: str):
        cpf_fake = "123.456.789-00"
        return f"""
        <cliente>
            <id>{id_cliente}</id>
            <nome>Maria da Silva</nome>
            <cpf_s>{criptografar(cpf_fake)}</cpf_s>
        </cliente>
        """

legado = SistemaLegadoSimulado()

class ClienteInput(BaseModel):
    nome: str
    cpf: str
    email: str
    
    class Config:
        schema_extra = {
            "example": {
                "nome": "João Teste",
                "cpf": "111.222.333-44",
                "email": "joao@email.com"
            }
        }

@app.post("/api/clientes", status_code=201)
async def criar_cliente(cliente: ClienteInput, token: str = Depends(verificar_token)):
    # 1. Criptografar
    cpf_seguro = criptografar(cliente.cpf)
    
    # 2. Converter para XML
    dados = cliente.dict()
    dados['cpf'] = cpf_seguro
    xml_body = xmltodict.unparse({"cadastro": dados}, pretty=True)
    
    # 3. Enviar ao legado
    resposta_xml = legado.enviar_xml(xml_body)
    
    # 4. Retornar JSON
    return xmltodict.parse(resposta_xml)

@app.get("/api/clientes/{id_cliente}")
async def consultar_cliente(id_cliente: str, token: str = Depends(verificar_token)):
    # 1. Buscar XML
    xml_recebido = legado.buscar_xml(id_cliente)
    
    # 2. Converter e Descriptografar
    dados = xmltodict.parse(xml_recebido)
    cpf_cripto = dados['cliente']['cpf_s']
    
    dados['cliente']['cpf_real'] = descriptografar(cpf_cripto)
    del dados['cliente']['cpf_s'] # Remove o dado sujo
    
    return dados