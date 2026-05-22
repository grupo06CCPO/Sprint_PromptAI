"""
╔══════════════════════════════════════════════════════════════════╗
║              ChatCore — ChargeGrid Assistant (GoodWe)            ║
║         EV Challenge FIAP + GoodWe 2026 — Sprint 1/2             ║
╠══════════════════════════════════════════════════════════════════╣
║  Integrantes:                                                    ║
║    Ana Julia Yumi      — RM 569430                               ║
║    Maria Fernanda      — RM 569999                               ║
║    Julia Nunes         — RM 569858                               ║
║    Rafael Rebello      — RM 570642                               ║
╚══════════════════════════════════════════════════════════════════╝
"""

# ──────────────────────────────────────────────
# IMPORTAÇÕES
# ──────────────────────────────────────────────

from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega as variáveis do arquivo .env (onde fica a chave da API)
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


# ──────────────────────────────────────────────
# BASE DE DADOS SIMULADA
# Representa os dados que viriam de um sistema
# real integrado aos eletropostos GoodWe
# ──────────────────────────────────────────────

# Dados do usuário final (motorista)
dados_usuario = {
    "status_recarga": "75%",
    "tempo_restante": "20 minutos",
    "pagamento_atual": "R$ 40,00",
    "historico_pagamentos": {
        "abril": "R$ 55,00",
        "maio": "R$ 40,00",
    },
}

# Dados administrativos e operacionais
dados_admin = {
    "carregadores_disponiveis": 2,
    "alertas": ["SOBRECARGA NO ELETROPOSTO 05"],
    "falhas": ["FALHA NO PAGAMENTO — CLIENTE_X | ELETROPOSTO_04"],
    "monitoramento_energetico": "STATUS GERAL: NORMAL",
    "relatorio_eletropostos": {
        "ELETROPOSTO_01": "EM USO",
        "ELETROPOSTO_02": "VAZIO",
        "ELETROPOSTO_03": "FINALIZANDO PAGAMENTO",
        "ELETROPOSTO_04": "FALHA",
        "ELETROPOSTO_05": "SOBRECARGA",
    },
}


# ──────────────────────────────────────────────
# FUNÇÕES DE FERRAMENTA (TOOLS)
# Cada função busca um tipo de informação do sistema
# O modelo decide qual função chamar com base
# na pergunta do usuário
# ──────────────────────────────────────────────

def status_recarga() -> str:
    """Retorna o status atual da recarga e o tempo restante."""
    return (
        f"🔋 Status atual da recarga: {dados_usuario['status_recarga']}\n"
        f"⏱️  Tempo estimado para conclusão: {dados_usuario['tempo_restante']}"
    )


def info_pagamento() -> str:
    """Retorna o valor da sessão atual e o histórico de pagamentos."""
    historico = "\n".join(
        f"   • {mes.capitalize()}: {valor}"
        for mes, valor in dados_usuario["historico_pagamentos"].items()
    )
    return (
        f"💳 Cobrança da sessão atual: {dados_usuario['pagamento_atual']}\n"
        f"📋 Histórico de pagamentos:\n{historico}"
    )


def carregadores_disponiveis() -> str:
    """Informa quantos carregadores estão disponíveis no momento."""
    qtd = dados_admin["carregadores_disponiveis"]
    emoji = "✅" if qtd > 0 else "❌"
    return (
        f"{emoji} Carregadores disponíveis no momento: {qtd}\n"
        f"   Localize o mais próximo pelo mapa do aplicativo."
    )


def listar_alertas() -> str:
    """Lista todos os alertas ativos no sistema."""
    if dados_admin["alertas"]:
        lista = "\n".join(f"   ⚠️  {a}" for a in dados_admin["alertas"])
        return f"🚨 Alertas ativos:\n{lista}"
    return "✅ Nenhum alerta ativo no momento."


def listar_falhas() -> str:
    """Lista todas as falhas registradas nos eletropostos."""
    if dados_admin["falhas"]:
        lista = "\n".join(f"   ❌ {f}" for f in dados_admin["falhas"])
        return f"🔧 Falhas registradas:\n{lista}"
    return "✅ Nenhuma falha registrada no momento."


def monitoramento_energetico() -> str:
    """Retorna o status geral do monitoramento energético."""
    return f"⚡ Monitoramento energético:\n   {dados_admin['monitoramento_energetico']}"


def relatorio_eletropostos() -> str:
    """Exibe o relatório completo com o status de cada eletroposto."""
    def icone(status):
        if status == "EM USO":
            return "🟢"
        if status == "VAZIO":
            return "⚫"
        if "FINAL" in status:
            return "🟡"
        return "🔴"

    linhas = "\n".join(
        f"   {icone(s)} {ep}: {s}"
        for ep, s in dados_admin["relatorio_eletropostos"].items()
    )
    return f"📊 Relatório dos eletropostos:\n{linhas}"


# ──────────────────────────────────────────────
# MAPA DE FERRAMENTAS
# Liga o nome da função (string) à função real
# O modelo retorna o nome em texto, e aqui
# encontramos a função correspondente para executar
# ──────────────────────────────────────────────

FERRAMENTAS_DISPONIVEIS = {
    "status_recarga":           status_recarga,
    "info_pagamento":           info_pagamento,
    "carregadores_disponiveis": carregadores_disponiveis,
    "listar_alertas":           listar_alertas,
    "listar_falhas":            listar_falhas,
    "monitoramento_energetico": monitoramento_energetico,
    "relatorio_eletropostos":   relatorio_eletropostos,
}


# ──────────────────────────────────────────────
# DEFINIÇÃO DAS TOOLS PARA A API
# Descreve para o modelo quais ferramentas
# existem e quando ele deve usá-las
# ──────────────────────────────────────────────

def criar_tool(nome: str, descricao: str) -> dict:
    """Monta o formato de tool esperado pela OpenAI API."""
    return {
        "type": "function",
        "function": {
            "name": nome,
            "description": descricao,
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }


tools = [
    criar_tool("status_recarga",
               "Retorna o status atual da recarga do veículo e o tempo restante."),
    criar_tool("info_pagamento",
               "Retorna o valor da sessão atual e o histórico de pagamentos do usuário."),
    criar_tool("carregadores_disponiveis",
               "Informa quantos carregadores estão disponíveis no momento."),
    criar_tool("listar_alertas",
               "Lista todos os alertas ativos no sistema (sobrecargas, emergências)."),
    criar_tool("listar_falhas",
               "Lista todas as falhas registradas nos eletropostos."),
    criar_tool("monitoramento_energetico",
               "Retorna o status geral do monitoramento energético da rede."),
    criar_tool("relatorio_eletropostos",
               "Exibe o relatório completo com o status de cada eletroposto."),
]


# ──────────────────────────────────────────────
# SYSTEM PROMPT
# Define o comportamento, personalidade e
# limitações do ChatCore
# ──────────────────────────────────────────────

SYSTEM_PROMPT = """
Você é o ChatCore, assistente virtual da ChargeGrid — solução inteligente de gestão de eletropostos da GoodWe.

Seu papel é operar como interface conversacional para ambientes comerciais de carregamento de veículos elétricos, atendendo três perfis de usuários: motoristas (usuários finais), administradores/operadores e técnicos.

PERSONAS E CAPACIDADES:

Para USUÁRIOS FINAIS (motoristas) você pode:
  - Consultar o status da recarga em andamento (ferramenta: status_recarga)
  - Informar o valor da sessão atual e histórico de pagamentos (ferramenta: info_pagamento)
  - Verificar quantos carregadores estão disponíveis (ferramenta: carregadores_disponiveis)

Para ADMINISTRADORES / OPERADORES você pode:
  - Listar todos os alertas ativos no sistema (ferramenta: listar_alertas)
  - Listar falhas registradas nos eletropostos (ferramenta: listar_falhas)
  - Exibir o monitoramento energético geral (ferramenta: monitoramento_energetico)
  - Gerar relatório completo dos eletropostos (ferramenta: relatorio_eletropostos)

Para TÉCNICOS você pode:
  - Diagnosticar falhas nos equipamentos (ferramenta: listar_falhas)
  - Verificar status operacional de cada eletroposto (ferramenta: relatorio_eletropostos)
  - Consultar o monitoramento energético (ferramenta: monitoramento_energetico)

REGRAS DE COMPORTAMENTO:

SEMPRE:
  - Use as ferramentas disponíveis para buscar dados reais antes de responder
  - Responda em português, de forma clara e objetiva
  - Solicite mais informações caso a pergunta seja ambígua

NUNCA:
  - Invente dados, valores, status ou informações técnicas
  - Responda perguntas fora do contexto de mobilidade elétrica e gestão de eletropostos GoodWe

TOM:
  - Profissional e direto para operadores e técnicos
  - Simples e acessível para usuários finais
  - Use emojis com moderação para facilitar leitura de status
"""


# ──────────────────────────────────────────────
# PROCESSAMENTO DA MENSAGEM
# Aqui acontece a lógica principal:
# 1. Envia histórico + tools para a API
# 2. Se o modelo quiser usar uma tool, executa
# 3. Devolve o resultado para o modelo
# 4. Retorna a resposta final
# ──────────────────────────────────────────────

def processar_mensagem(historico: list) -> str:
    """
    Recebe o histórico completo da conversa e retorna
    a resposta final do ChatCore como string.
    """

    # Primeira chamada: modelo decide se usa uma ferramenta ou responde direto
    resposta = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico,
        tools=tools,
        temperature=0,
        max_tokens=1000,
    )

    mensagem = resposta.choices[0].message

    # Se o modelo não precisou de nenhuma ferramenta, retorna direto
    if not mensagem.tool_calls:
        return mensagem.content

    # Se precisou de ferramenta, adiciona a decisão do modelo ao histórico
    historico.append(mensagem)

    # Executa cada ferramenta que o modelo solicitou
    for tool_call in mensagem.tool_calls:
        nome_funcao = tool_call.function.name
        funcao = FERRAMENTAS_DISPONIVEIS.get(nome_funcao)

        if funcao:
            resultado = funcao()
        else:
            resultado = f"Ferramenta '{nome_funcao}' não encontrada."

        # Adiciona o resultado da ferramenta ao histórico
        historico.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": resultado,
        })

    # Segunda chamada: modelo lê o resultado da ferramenta e gera resposta final
    resposta_final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=historico,
        tools=tools,
        temperature=0,
        max_tokens=1000,
    )

    return resposta_final.choices[0].message.content


# ──────────────────────────────────────────────
# LOOP PRINCIPAL
# Interface de conversa no terminal
# ──────────────────────────────────────────────

def iniciar_chatbot():
    banner = """
╔══════════════════════════════════════════════════╗
║        ChatCore — ChargeGrid Assistant           ║
║      Assistente Virtual GoodWe (OpenAI API)      ║
║      Digite 'sair' ou 'tchau' para encerrar      ║
╚══════════════════════════════════════════════════╝
    """
    print(banner)

    # Histórico começa com o system prompt
    historico = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Palavras que encerram a conversa
    DESPEDIDAS = ("tchau", "até", "ate", "bye", "sair", "exit", "fim", "encerrar")

    while True:
        try:
            entrada = input("Você: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nChatCore: Sessão encerrada. Até logo! ⚡")
            break

        if not entrada:
            continue

        if any(d in entrada.lower() for d in DESPEDIDAS):
            print("\nChatCore: 👋 Até logo! Qualquer dúvida é só chamar. Boa recarga! ⚡\n")
            break

        # Adiciona a mensagem do usuário ao histórico
        historico.append({"role": "user", "content": entrada})

        # Processa e obtém a resposta
        resposta = processar_mensagem(historico)

        # Adiciona a resposta do assistente ao histórico
        historico.append({"role": "assistant", "content": resposta})

        print(f"\nChatCore: {resposta}\n")


# ──────────────────────────────────────────────
# INÍCIO DO PROGRAMA
# ──────────────────────────────────────────────

if __name__ == "__main__":
    iniciar_chatbot()
