
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.file_generation import FileGenerationTools

CONTEXT = """

Exemplo de output esperado:

[
    { "username": "kipper.dev", "link": "https://www.instagram.com/kipper.dev/", "sexo": "indeterminado" },
    { "username": "lucasluc25", "link": "https://www.instagram.com/lucasluc25/", "sexo": "homem" },
    { "username": "ramon.pelle", "link": "https://www.instagram.com/ramon.pelle/", "sexo": "homem" },
    { "username": "legitimoth", "link": "https://www.instagram.com/legitimoth/", "sexo": "indeterminado" },
]

"""

agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    name="Agente sumarizador",
    description="Você é especialista em identificar gênero com base em username de rede social.",
    instructions=[
        "identifique reconhecendo apenas pelo username.",
        "não perca nenhum item da lista.",
        "No fim não explique nada responda nesse formato apenas: " + CONTEXT,
        "deixa a lista em ordem ascendente pelo sexo: mulheres, homens, indeterminado."
    ],
    debug_mode=True,
    telemetry=False
)
