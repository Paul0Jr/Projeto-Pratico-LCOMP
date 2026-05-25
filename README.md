# Projeto-Pratico-LCOMP
Repositório voltado para entrega do projeto prático proposto na disciplina de Lógica para Computação.

# Proposta

Avaliar raciocínio de LLM com e sem demonstrações em LEAN. **Gerar premissas e conclusão diretamente com formulas em logica proposicional** (→, ∧, ∨, ¬, ↔).

Usar Z3 pra saber se é consequência lógica. Pedir para a LLM apresentar a prova usando a linguagem LEAN. Checar se a demonstração está correta. 
Caso não seja consequência lógica, pedir para a LLM dar um contra-exemplo. **Checar o contra-exemplo COM E SEM GUIDANCE**. Comparar se acerta mais quando pedimos pra fornecer a demonstração.

Usar o seguinte material sobre LEAN: https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html

---

# Pré-requisitos
- Docker e Docker Compose instalados
- Chave da API Google Gemini - [obter aqui](https://aistudio.google.com/apikey)


# Estrutura do Projeto

```
├── solver.py
├── lean_prover.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## Como usar

### Configuração da API Gemini
Defina sua chave da API como variável de ambiente:
```bash
export GEMINI_API_KEY='sua-chave-aqui'
```

Ou no Docker:
```bash
GEMINI_API_KEY='sua-chave-aqui' make docker-run
```

---

## Recursos da Avaliação

### Fórmulas em Lógica Proposicional
- **Implicação**: `p → q`
- **Conjunção**: `p ∧ q`
- **Disjunção**: `p ∨ q`
- **Negação**: `¬p`
- **Bicondicional**: `p ↔ q`

As premissas e conclusões são expressas diretamente nestes símbolos formais.

### Verificação com Z3
- Dado um conjunto de premissas e uma conclusão
- Z3 verifica se é logicamente válido usando SAT solving
- Determina se a conclusão é consequência lógica das premissas

### Geração de Provas em LEAN (Gemini)
- Se é consequência: pede prova formal em LEAN 3
- Baseado em natural dedução natural baseado no artigo sobre LEAN.

### Geração e Comparação de Contra-exemplos (Gemini)
- Se NÃO é consequência: gera atribuição de valores
- **COM GUIDANCE**: Instruções explícitas sobre verificação
- **SEM GUIDANCE**: Apenas premissas, conclusão e contra-exemplo
- Compara acurácia entre os dois modos

### Métricas de Comparação
Para cada contra-exemplo gerado pela LLM:
- **Validação**: Verifica se tem estrutura apropriada (assignments e valores true/false)
- **Comparação**: Analisa qual modo (com/sem guidance) acerta mais
- **Resultado**: Indica se guidance melhorou a geração

---

## Exemplos Inclusos

1. **Modus Ponens** (válido)
   - Premissas: p, p → q
   - Conclusão: q

2. **Silogismo Disjuntivo** (válido)
   - Premissas: p ∨ q, ¬p
   - Conclusão: q

3. **Afirmação do Consequente** (inválido - falácia)
   - Premissas: p → q, q
   - Conclusão: p
   - *Inclui comparação de contra-exemplos com/sem guidance*

4. **Raciocínio Complexo** (válido)
   - Premissas: p → q, r → ¬p, p
   - Conclusão: q

---

## Objetivo da Comparação

Avaliar se fornecer instruções explícitas sobre como verificar contra-exemplos (guidance) 
melhora a capacidade da LLM de gerar contra-exemplos válidos em lógica proposicional.