
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.file_generation import FileGenerationTools

CONTEXT = """

Exemplo de output esperado:

{"kipper.dev": "indeterminado", 
"joao": "homem", 
"maria: "mulher", 
"beatriz": "mulher", 
"lucasluc25": "homem", ...}

"""

def criar_agent(model_id: str) -> Agent:
    return Agent(
        model=Groq(id=model_id),
        name="Agente sumarizador",
        description="Você é especialista em identificar gênero com base em username de rede social.",
        instructions=[
            "identifique reconhecendo apenas pelo username.",
            "não perca nenhum item da lista.",
            "No formato do context: " + CONTEXT
        ],
        debug_mode=True,
        telemetry=False
    )
