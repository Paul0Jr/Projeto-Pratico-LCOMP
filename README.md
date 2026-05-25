## Sobre o Projeto

Este projeto implementa um sistema completo para análise de consequência lógica em lógica proposicional, combinando:

- **Z3 SMT Solver**: Verificação rigorosa de consequência lógica usando SAT solving
- **LEAN 3**: Geração de provas formais usando natural deduction
- **Google Gemini**: Geração inteligente de provas e contra-exemplos

### Fundamentos Teóricos

Uma conclusão **C** é **consequência lógica** de premissas **P₁, P₂, ..., Pₙ** se:

> Não existe nenhuma interpretação (atribuição de valores verdade) que torna todas as premissas verdadeiras e a conclusão falsa.

Equivalentemente, em termos de SAT solving: **(P₁ ∧ P₂ ∧ ... ∧ Pₙ ∧ ¬C)** é **insatisfazível**.

**Referência teórica**: [Natural Deduction for Propositional Logic](https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html)

## Arquitetura

```
Projeto-Pratico-LCOMP/
├── src/
│   ├── __init__.py          # Metadados do projeto
│   ├── config.py            # Configurações e constantes
│   ├── logic.py             # Verificador de lógica proposicional
│   ├── lean_prover.py       # Gerador de provas LEAN
│   ├── solver.py            # Solver principal
│   └── validator.py         # Validação de provas
├── main.py                  # Entry point principal
├── requirements.txt         # Dependências Python
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Orquestração
├── README.md                # Este arquivo
└── docs/                    # Documentação acadêmica
```

## Pré-requisitos

- Python 3.11+
- Docker e Docker Compose (opcional)
- Chave da API Google Gemini: [obter aqui](https://aistudio.google.com/apikey)

## Instalação

### Sem Docker

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/Projeto-Pratico-LCOMP.git
cd Projeto-Pratico-LCOMP

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a chave API
export GEMINI_API_KEY='sua-chave-aqui'

# 5. Execute
python main.py
```

### Com Docker

```bash
# Build e executa com Docker Compose
export GEMINI_API_KEY='sua-chave-aqui'
docker-compose up --build
```

## Exemplo de Uso

```python
from src.solver import LogicalConsequenceSolver
from src.logic import LogicalArgument

# Define um argumento
argumento = LogicalArgument(
    propositions=["p", "q"],
    premises=["p", "p → q"],
    conclusion="q"
)

# Resolve
solver = LogicalConsequenceSolver()
resultado = solver.solve(argumento)

print(f"É consequência lógica? {resultado.is_valid}")
print(f"Prova: {resultado.proof}")
```

## Exemplos Inclusos

O projeto implementa os seguintes argumentos clássicos:

### Argumentos Válidos

1. **Modus Ponens**: `p, p → q ⊢ q`
2. **Modus Tollens**: `p → q, ¬q ⊢ ¬p`
3. **Silogismo Disjuntivo**: `p ∨ q, ¬p ⊢ q`
4. **Silogismo Hipotético**: `p → q, q → r ⊢ p → r`
5. **Dilema Destrutivo**: `p → q, r → s, ¬q ∨ ¬s ⊢ ¬p ∨ ¬r`

### Argumentos Inválidos (Falácias)

1. **Afirmação do Consequente**: `p → q, q ⊢ p` (INVÁLIDO)
2. **Negação do Antecedente**: `p → q, ¬p ⊢ ¬q` (INVÁLIDO)



## Como Funciona

### 1. Verificação com Z3

```
Entrada: Premissas e Conclusão
         ↓
    Cria fórmula: P₁ ∧ P₂ ∧ ... ∧ ¬C
         ↓
    Verifica satisfazibilidade com Z3
         ↓
    UNSAT → Consequência lógica ✓
    SAT  → Não é consequência (contra-exemplo) ✗
```

### 2. Geração de Provas LEAN

Para argumentos válidos, o Gemini gera uma prova formal em LEAN 3:

```lean
theorem modus_ponens (p q : Prop) (hp : p) (hpq : p → q) : q := by
  exact hpq hp
```

### 3. Geração de Contra-exemplos

Para argumentos inválidos, o Gemini gera um contra-exemplo:

```
Contra-exemplo:
p = false
q = true

Verificação:
- Premissa 1 (p → q): false → true = true ✓
- Premissa 2 (q): true ✓
- Conclusão (p): false ✗
```


## Módulos Principais

### `src.logic` - Lógica Proposicional
Implementa verificação de consequência lógica usando Z3.

**Classes principais**:
- `PropositionalLogicVerifier`: Verificador com SAT solving

**Métodos**:
- `verify_consequence(premises, conclusion)`: Verifica validade
- `parse_formula(formula)`: Parse de fórmulas lógicas

### `src.lean_prover` - Geração de Provas
Comunica com API Gemini para gerar provas e contra-exemplos.

**Classes principais**:
- `LeanProofGenerator`: Gerador de provas LEAN

**Métodos**:
- `generate_proof(...)`: Gera prova para argumento válido
- `generate_counterexample(...)`: Gera contra-exemplo para argumento inválido

### `src.validator` - Validação
Realiza análises estruturais e sintáticas de provas.

**Classes principais**:
- `LeanProofValidator`: Validador de sintaxe e estrutura

**Métodos**:
- `validate_syntax(proof)`: Valida sintaxe LEAN
- `validate_structure(proof)`: Analisa estrutura lógica

## Configuração

### Variáveis de Ambiente

- `GEMINI_API_KEY`: Chave de API do Google Gemini (obrigatória para geração de provas)

### Arquivo `.env`

```env
GEMINI_API_KEY=sua-chave-aqui
```
