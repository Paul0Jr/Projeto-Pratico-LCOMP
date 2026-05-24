Projeto-Pratico-LCOMP
Repositório voltado para entrega do projeto prático proposto na disciplina de Lógica para Computação.

# Proposta

Avaliar raciocínio de LLM com e sem demonstrações em LEAN. Gerar premissas e conclusao diretamente com formulas em logica proposicional.

Usar Z3 pra saber se é consequência lógica. Pedir para a LLM apresentar a prova usando a linguagem LEAN. Checar se a demonstracão está correta. Caso nao seja consequencia logica, pedir para a LLM dar um contra exemplo. Checar o contra exemplo. Comparar se acerta mais quando pedimos pra fornecer a demonstracao.

Usar o seguinte material sobre LEAN: https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html

---

# 🚀 Como Executar

## Pré-requisitos - Docker e Docker Compose instalados - Chave da API Google Gemini - obter aqui

## Opção 1: Docker Compose (Recomendado)

### 1. Configure a chave da API bash<span data-diff-end="22"></span> <span data-diff-start="23"></span>export GEMINI_API_KEY='sua-chave-aqui'<span data-diff-end="23"></span> <span data-diff-start="24"></span>

### 2. Execute o projeto bash<span data-diff-end="27"></span> <span data-diff-start="28"></span>docker-compose up<span data-diff-end="28"></span> <span data-diff-start="29"></span>

## Opção 2: Com arquivo .env

### 1. Crie um arquivo .env na raiz do projeto bash<span data-diff-end="34"></span> <span data-diff-start="35"></span>cp .env.example .env<span data-diff-end="35"></span> <span data-diff-start="36"></span># Edite .env e adicione sua chave GEMINI_API_KEY<span data-diff-end="36"></span> <span data-diff-start="37"></span>

### 2. Execute bash<span data-diff-end="40"></span> <span data-diff-start="41"></span>docker-compose up<span data-diff-end="41"></span> <span data-diff-start="42"></span>

## Opção 3: Shell interativo bash<span data-diff-end="45"></span> <span data-diff-start="46"></span>export GEMINI_API_KEY='sua-chave-aqui'<span data-diff-end="46"></span> <span data-diff-start="47"></span>docker-compose run --rm solver bash<span data-diff-end="47"></span> <span data-diff-start="48"></span>python solver.py<span data-diff-end="48"></span> <span data-diff-start="49"></span>

## Opção 4: Usando Makefile bash<span data-diff-end="52"></span> <span data-diff-start="53"></span>make build<span data-diff-end="53"></span> <span data-diff-start="54"></span>export GEMINI_API_KEY='sua-chave-aqui'<span data-diff-end="54"></span> <span data-diff-start="55"></span>make run<span data-diff-end="55"></span> <span data-diff-start="56"></span>

---

# 📚 Estrutura do Projeto

<span data-diff-end="62"></span> <span data-diff-start="63"></span>├── solver.py # Main - executa os exemplos com Z3 + Gemini<span data-diff-end="63"></span> <span data-diff-start="64"></span>├── lean_prover.py # Integração com Gemini API para gerar provas LEAN<span data-diff-end="64"></span> <span data-diff-start="65"></span>├── requirements.txt # Dependências Python<span data-diff-end="65"></span> <span data-diff-start="66"></span>├── Dockerfile # Configuração Docker<span data-diff-end="66"></span> <span data-diff-start="67"></span>├── docker-compose.yml # Orquestração de containers<span data-diff-end="67"></span> <span data-diff-start="68"></span>├── Makefile # Atalhos para comandos comuns<span data-diff-end="68"></span> <span data-diff-start="69"></span>└── README.md # Este arquivo<span data-diff-end="69"></span> <span data-diff-start="70"></span>

---

# 🔍 O que o projeto faz

## 1️⃣ Verifica consequência lógica com Z3 - Dado um conjunto de premissas e uma conclusão - Z3 verifica se é logicamente válido - Usa SAT solving (insatisfiabilidade)

## 2️⃣ Gera provas em LEAN (Gemini) - Se é consequência: pede prova formal em LEAN 3 - Baseado em natural deduction (dedução natural) - Segue o material: https://leanprover.github.io/logic_and_proof_lean3/

## 3️⃣ Gera contra-exemplos (Gemini) - Se NÃO é consequência: gera atribuição de valores - Mostra proposições que falsificam o argumento

---

# 📋 Exemplos Inclusos

1. Modus Ponens - Argumento válido clássico - Premissas: p, p → q - Conclusão: q - Resultado: ✓ Válido

2. Silogismo Disjuntivo - Outro argumento válido - Premissas: p ∨ q, ¬p - Conclusão: q - Resultado: ✓ Válido

3. Falácia da Afirmação do Consequente - Argumento inválido - Premissas: p → q, q - Conclusão: p - Resultado: ✗ Inválido (com contra-exemplo)

4. Raciocínio Complexo - Múltiplas proposições - Demonstra capacidade com 3+ proposições - Z3 + Gemini trabalham juntos

---

# 🛠️ Estrutura do Código

### solver.py - verificar_consequencia(): Usa Z3 para validar - exemplo_X_com_prova(): Executa exemplo + Gemini - Trata erros de API graciosamente

### lean_prover.py - gerar_prova_lean(): Gemini gera prova LEAN - gerar_contra_exemplo(): Gemini gera contra-exemplo - validar_prova_lean(): Validação básica de sintaxe - conversa_interativa(): Chat com Gemini (futuro)

---

# ⚙️ Variáveis de Ambiente

| Variável | Obrigatória | Padrão | |----------|---|---| | GEMINI_API_KEY | ✅ Sim | - | | PYTHONUNBUFFERED | ❌ Não | 1 |

---

# 🤖 Modelos e Parâmetros

- Modelo Gemini: gemini-pro (modelo padrão para provas LEAN) - Sistema prompt: Especializado em lógica proposicional + LEAN

---

# 📝 Próximas Funcionalidades

- [ ] Validação de provas LEAN via compilação real - [ ] Comparação: LLM com vs sem demonstrações - [ ] Benchmark: taxa de acerto por tipo de argumento - [ ] Interface web para explorar provas interativamente - [ ] Suporte a quantificadores (FOL - First Order Logic)

---

# 🐛 Troubleshooting

### "GEMINI_API_KEY not configured" bash<span data-diff-end="159"></span> <span data-diff-start="160"></span>export GEMINI_API_KEY='sua-chave'<span data-diff-end="160"></span> <span data-diff-start="161"></span>docker-compose up<span data-diff-end="161"></span> <span data-diff-start="162"></span>

### "Failed building wheel for z3-solver" Já resolvido via Docker! No container está pré-compilado.

### "Connection timeout" ao chamar Gemini - Verifique sua chave de API - Verifique sua conexão com internet - Tente novamente

---

# 📄 Licença

Projeto educacional para disciplina de Lógica para Computação.