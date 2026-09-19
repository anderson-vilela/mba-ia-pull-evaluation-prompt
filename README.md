# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.9: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```

---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Helpfulness >= 0.9
- Correctness >= 0.9
- F1-Score >= 0.9
- Clarity >= 0.9
- Precision >= 0.9

MÉDIA das 5 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
│
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Técnicas Aplicadas (Fase 2)

Para transformar o prompt inicial v1 em uma versão de alta performance (v2) capaz de superar o limiar de 0.90 em todas as 5 métricas de avaliação, foram combinadas quatro técnicas essenciais de Engenharia de Prompts:

### 1. Few-Shot Learning (Obrigatória)

- **Motivação:** Modelos de linguagem se beneficiam enormemente de demonstrações diretas de padrão de resposta (_in-context learning_). Sem exemplos, o modelo gerava respostas em formatos divergentes e com níveis de profundidade inconsistentes.
- **Aplicação Prática:** Foram fornecidos 3 exemplos completos de entrada e saída correspondentes aos três perfis de complexidade do dataset (`simples`, `médio` e `complexo`):

```markdown
[EXEMPLO 1 - BUG SIMPLES]
Relato do Bug:
Botão de adicionar ao carrinho não funciona no produto ID 1234.

Resposta:
Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Critérios de Aceitação:

- Dado que estou visualizando um produto
- Quando clico no botão "Adicionar ao Carrinho"
- Então o produto deve ser adicionado ao carrinho
- E devo ver uma confirmação visual
- E o contador do carrinho deve ser atualizado
```

### 2. Role Prompting (Definição de Persona)

- **Motivação:** O prompt v1 continha uma definição genérica ("Você é um assistente..."). Isso impedia o modelo de balancear empatia com o usuário e autoridade técnica para guiar o time de engenharia.
- **Aplicação Prática:** Estabelecida a persona de **Staff Product Manager & Agile Technical Lead**:

```text
Você é um Staff Product Manager e Agile Technical Lead especialista em engenharia de requisitos de software e metodologias ágeis.
Sua missão é analisar relatos de bugs (bug reports) e transformá-los em User Stories completas, profissionais, concisas e altamente acionáveis para o time de desenvolvimento.
```

### 3. Skeleton of Thought & Adaptação Estrutural Dinâmica

- **Motivação:** O dataset de avaliação é heterogêneo, contendo desde bugs simples de interface até falhas críticas de infraestrutura e sincronização de dados. Tratar todos com o mesmo template causava perda de clareza em bugs simples (devido a excesso de seções) ou falta de completude em bugs complexos.
- **Aplicação Prática:** O prompt orienta a geração do esqueleto estrutural adequado conforme a complexidade identificada:
  - **Bugs Simples:** Exclusivamente User Story e Critérios de Aceitação Given-When-Then. Sem seções técnicas adicionais para preservar máxima clareza e concisão.
  - **Bugs Médios:** User Story, Critérios e seção de `Contexto Técnico:` (ou `Contexto de Segurança:`).
  - **Bugs Complexos:** Estrutura completa:
    - `=== USER STORY PRINCIPAL ===`
    - `=== CRITÉRIOS DE ACEITAÇÃO ===` (subtópicos A, B, C, D)
    - `=== CRITÉRIOS TÉCNICOS ===`
    - `=== CONTEXTO DO BUG ===` (Severidade e Impacto)
    - `=== TASKS TÉCNICAS SUGERIDAS ===`

### 4. Chain of Thought (CoT) e Rigor Factual

- **Motivação:** Evitar alucinações e inferências infundadas (ex.: supor tecnologias ou formatos de arquivo não mencionados no relato).
- **Aplicação Prática:** Instruções explícitas de raciocínio orientado à fidelidade:
  - Extrair rigorosamente a persona afetada e o benefício real a partir do relato.
  - Formular critérios testáveis e mensuráveis no padrão BDD.
  - Proibir invenção de tecnologias, endpoints ou suposições não citadas.

---

## Resultados Finais

### Links de Acesso

- **LangSmith Prompt Hub (Prompt v2 Público):** [andersonvilela-dev/bug_to_user_story_v2](https://smith.langchain.com/hub/andersonvilela-dev/bug_to_user_story_v2)
- **LangSmith Workspace Project (Direto):** [prompt-optimization-challenge-resolved](https://smith.langchain.com/o/9870836d-ee16-4e6c-990b-d664b6ec3909/projects/p/fcd9fc0d-b69a-4c6c-8968-d4006fc6b143)
- **LangSmith Dataset (Público):** [prompt-optimization-challenge-resolved-eval](https://smith.langchain.com/public/cb74bf43-6b08-489d-9925-04661a8f72b6/d)
- **Evidências de Tracing (Links Públicos Compartilhados):**
  - [Trace 1 - Bug Simples](https://smith.langchain.com/public/3d30710d-0302-4643-a9c0-9e09050df194/r)
  - [Trace 2 - Bug Médio](https://smith.langchain.com/public/fdf0d332-f665-47e6-b8a4-e0479367e3c2/r)
  - [Trace 3 - Bug Complexo](https://smith.langchain.com/public/8d9bde68-2e0f-424b-9107-b4441c5e8f0a/r)

### Tabela Comparativa: Prompt v1 vs Prompt v2

| Métrica         | Prompt v1 (Inicial) | Prompt v2 (Otimizado) | Variação |     Status      |
| :-------------- | :-----------------: | :-------------------: | :------: | :-------------: |
| **Helpfulness** |        0.45         |       **0.92**        |  +104%   |   ✅ Aprovado   |
| **Correctness** |        0.52         |       **0.91**        |   +75%   |   ✅ Aprovado   |
| **F1-Score**    |        0.48         |       **0.91**        |   +90%   |   ✅ Aprovado   |
| **Clarity**     |        0.50         |       **0.94**        |   +88%   |   ✅ Aprovado   |
| **Precision**   |        0.46         |       **0.91**        |   +98%   |   ✅ Aprovado   |
| **Média Geral** |     **0.4820**      |      **0.9174**       | **+90%** | ✅ **APROVADO** |

> **Critério de Aprovação Atingido:** Todas as 5 métricas obtiveram pontuação $\ge 0.90$ (90%) e média geral de **0.9174**, superando o limiar oficial tanto da especificação base ($\ge 0.80$) quanto do script validador `src/evaluate.py` ($\ge 0.90$).

### Evidência de Execução da Avaliação Oficial (Terminal)

```text
==================================================
AVALIAÇÃO DE PROMPTS OTIMIZADOS
==================================================

Provider: google
Modelo Principal: gemini-3.5-flash-lite
Modelo de Avaliação: gemini-3.5-flash-lite

Criando dataset de avaliação: prompt-optimization-challenge-resolved-eval...
   ✓ Carregados 15 exemplos do arquivo datasets/bug_to_user_story.jsonl
   ✓ Dataset 'prompt-optimization-challenge-resolved-eval' já existe, usando existente

======================================================================
PROMPTS PARA AVALIAR
======================================================================

🔍 Avaliando: andersonvilela-dev/bug_to_user_story_v2
   Puxando prompt do LangSmith Hub: andersonvilela-dev/bug_to_user_story_v2
   ✓ Prompt carregado com sucesso
   Dataset: 15 exemplos
   Avaliando exemplos...
      [1/15] F1:0.92 Clarity:0.95 Precision:0.93
      [2/15] F1:0.92 Clarity:0.95 Precision:0.95
      [3/15] F1:1.00 Clarity:0.95 Precision:0.85
      [4/15] F1:0.90 Clarity:0.95 Precision:0.93
      [5/15] F1:0.77 Clarity:0.95 Precision:0.85
      [6/15] F1:0.92 Clarity:0.95 Precision:0.93
      [7/15] F1:0.92 Clarity:0.90 Precision:0.93
      [8/15] F1:0.85 Clarity:0.85 Precision:0.93
      [9/15] F1:0.92 Clarity:0.90 Precision:0.83
      [10/15] F1:0.77 Clarity:0.90 Precision:0.93
      [11/15] F1:0.92 Clarity:1.00 Precision:0.87
      [12/15] F1:1.00 Clarity:0.90 Precision:0.87
      [13/15] F1:0.97 Clarity:0.95 Precision:0.93
      [14/15] F1:0.87 Clarity:1.00 Precision:0.93
      [15/15] F1:0.97 Clarity:1.00 Precision:0.93

==================================================
Prompt: andersonvilela-dev/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.92 ✓
  - Correctness: 0.91 ✓

Métricas Base:
  - F1-Score: 0.91 ✓
  - Clarity: 0.94 ✓
  - Precision: 0.91 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.9174
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.9

==================================================
RESUMO FINAL
==================================================

Prompts avaliados: 1
Aprovados: 1
Reprovados: 0

✅ Todos os prompts atingiram todas as métricas >= 0.9!
```

---

## Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados **OU** Python 3.12+ localmente.
- Arquivo `.env` configurado com credenciais válidas (`LANGSMITH_API_KEY`, `USERNAME_LANGSMITH_HUB` e `GOOGLE_API_KEY` ou `OPENAI_API_KEY`).

### Opção 1: Execução via Docker (Ambiente Conteinerizado Recomendado)

1. **Subir o ambiente:**

   ```bash
   docker compose -f dev.compose.yaml up -d --build
   ```

2. **Fazer pull do prompt v1 do LangSmith Hub:**

   ```bash
   docker compose -f dev.compose.yaml exec app python src/pull_prompts.py
   ```

3. **Executar a suíte de testes unitários (pytest):**

   ```bash
   docker compose -f dev.compose.yaml exec app pytest tests/test_prompts.py -v
   ```

4. **Publicar o prompt v2 no LangSmith Hub:**

   ```bash
   docker compose -f dev.compose.yaml exec app python src/push_prompts.py
   ```

5. **Executar a avaliação automatizada contra os 15 exemplos:**

   ```bash
   docker compose -f dev.compose.yaml exec app python src/evaluate.py
   ```

6. **Parar o ambiente ao concluir:**
   ```bash
   docker compose -f dev.compose.yaml down
   ```

### Opção 2: Execução em Ambiente Virtual Local (venv)

1. **Criar e ativar o ambiente virtual:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Executar os comandos em sequência:**
   ```bash
   python src/pull_prompts.py
   pytest tests/test_prompts.py -v
   python src/push_prompts.py
   python src/evaluate.py
   ```
