# ChargeGrid Assistant — ChatCore
## Chatbot Inteligente para Gestão de Eletropostos GoodWe

---

## Integrantes

| Nome | RM |
|---|---|
| Ana Julia Yumi | 569430 |
| Maria Fernanda | 569999 |
| Julia Nunes | 569858 |
| Rafael Rebello | 570642 |

---

## Problema Abordado

A GoodWe possui uma solução consolidada de carregamento veicular para uso residencial individual. O desafio proposto pelo **EV Challenge FIAP + GoodWe 2026** é transformar essa solução em algo **inteligente e escalável** para ambientes **comerciais e coletivos** — como estacionamentos, frotas corporativas e postos de recarga públicos.

Os principais problemas identificados nesse contexto são:

- Ausência de gerenciamento inteligente de potência elétrica entre múltiplos eletropostos
- Falta de controle centralizado de sessões de recarga
- Dificuldade de cobrança individualizada por usuário ou veículo
- Inexistência de monitoramento em tempo real dos equipamentos
- Necessidade de interface simples para usuários, operadores e técnicos
- Ausência de relatórios de consumo e faturamento consolidados

---

## Proposta do Chatbot

O **ChatCore** é um assistente virtual inteligente desenvolvido para operar como interface conversacional da infraestrutura de eletropostos GoodWe em ambientes **comerciais**.

O chatbot atende três perfis de usuário:

**Usuário final (motorista):**
- Consultar status da recarga em andamento
- Verificar tempo restante para conclusão
- Consultar valor da sessão atual e histórico de pagamentos
- Verificar disponibilidade de carregadores

**Administrador / Operador:**
- Visualizar alertas ativos de sobrecarga
- Monitorar falhas nos eletropostos
- Acompanhar status de cada eletroposto em tempo real
- Consultar relatórios de uso e energia

**Técnico:**
- Diagnosticar falhas registradas no sistema
- Verificar status operacional dos equipamentos
- Monitorar conectividade e funcionamento geral

---

## Tecnologias Selecionadas

| Tecnologia | Função | Justificativa |
|---|---|---|
| **Python 3.11+** | Linguagem principal | Ecossistema rico para IA e APIs, alta legibilidade |
| **OpenAI API (GPT-4o-mini)** | Modelo de linguagem | Excelente custo-benefício, suporte nativo a function calling, baixa latência |
| **Function Calling (Tools)** | Integração com dados reais | Permite ao modelo chamar funções do sistema sem inventar dados |
| **python-dotenv** | Gerenciamento de variáveis | Segurança para credenciais sensíveis como a API Key |

## Justificativa Técnica

O **GPT-4o-mini** foi escolhido por oferecer suporte nativo a **function calling** (Tools), recurso essencial para que o chatbot consulte dados reais do sistema — como status de carregadores, histórico de pagamentos e alertas — sem inventar informações. Isso garante precisão operacional, um requisito crítico para um assistente de uso real em eletropostos.

A arquitetura com **Tools** permite uma separação clara entre a lógica de negócio (funções Python com dados simulados) e a inteligência conversacional (LLM), tornando o sistema facilmente expansível para integração com APIs e bancos de dados reais no futuro.

---

## Fluxo de Funcionamento

O fluxo completo do chatbot pode ser resumido em:

```
Usuário digita mensagem
        ↓
Mensagem adicionada ao histórico
        ↓
Chamada à OpenAI API (com histórico + tools disponíveis)
        ↓
Modelo decide se precisa usar uma ferramenta?
   ├── SIM → Executa a função Python correspondente
   │          → Resultado adicionado ao histórico
   │          → Nova chamada à API com o resultado
   │          → Resposta final gerada
   └── NÃO → Resposta gerada diretamente
        ↓
Resposta exibida ao usuário
        ↓
Histórico atualizado para manter contexto
```

> O fluxograma visual completo está disponível no repositório (arquivo `fluxograma.svg`).

---

# Modelo de Teste

## Perguntas Esperadas e Respostas Ideais

**1. Status de recarga**
- **Pergunta:** "Como está minha recarga?"
- **Resposta ideal:** "Status atual da recarga: 75% — Tempo estimado para conclusão: 20 minutos."

**2. Informações de pagamento**
- **Pergunta:** "Quanto vou pagar por essa sessão?"
- **Resposta ideal:** "Cobrança da sessão atual: R$ 40,00. Histórico: Abril: R$ 55,00 | Maio: R$ 40,00."

**3. Disponibilidade de carregadores**
- **Pergunta:** "Tem carregador disponível?"
- **Resposta ideal:** "[OK] Carregadores disponíveis no momento: 2. Localize o mais próximo pelo mapa do aplicativo."

**4. Alertas de sobrecarga (administrador)**
- **Pergunta:** "Existe algum alerta ativo no sistema?"
- **Resposta ideal:** "Alertas ativos: [ALERTA] SOBRECARGA NO ELETROPOSTO 05."

**5. Relatório dos eletropostos (administrador)**
- **Pergunta:** "Me dá um relatório dos eletropostos."
- **Resposta ideal:**
  ```
  Relatorio dos eletropostos:
  [EM USO]      ELETROPOSTO_01: EM USO
  [VAZIO]       ELETROPOSTO_02: VAZIO
  [FINALIZANDO] ELETROPOSTO_03: FINALIZANDO PAGAMENTO
  [ERRO]        ELETROPOSTO_04: FALHA
  [ERRO]        ELETROPOSTO_05: SOBRECARGA
  ```

**6. Falhas registradas (técnico)**
- **Pergunta:** "Quais falhas estão registradas?"
- **Resposta ideal:** "Falhas registradas: [FALHA] FALHA NO PAGAMENTO — CLIENTE_X | ELETROPOSTO_04."

**7. Pergunta fora do escopo**
- **Pergunta:** "Qual a previsão do tempo para amanhã?"
- **Resposta ideal:** "Desculpe, posso ajudar apenas com informações relacionadas ao carregamento de veículos elétricos e à infraestrutura GoodWe. Para previsão do tempo, recomendo consultar um serviço especializado."

---

## System Prompt

O system prompt completo utilizado para condicionar o modelo está disponível no arquivo `system_prompt.txt` deste repositório.

---

## Estrutura do Repositório

```
/
├── README.md              ← Documentação completa do projeto
├── system_prompt.txt      ← Prompt base do chatbot
├── fluxograma.png         ← Fluxograma visual do funcionamento
└── chatbot.py             ← Protótipo inicial (desenvolvimento completo previsto para a Sprint 2)
```

---

*Projeto desenvolvido para o EV Challenge FIAP + GoodWe 2026 — Sprint 1*
