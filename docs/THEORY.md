# Fundamentos Teóricos - Lógica Proposicional e SAT Solving

## 📚 Índice

1. [Lógica Proposicional Básica](#lógica-proposicional-básica)
2. [Consequência Lógica](#consequência-lógica)
3. [Dedução Natural](#dedução-natural)
4. [SAT Solving](#sat-solving)
5. [LEAN 3 e Prova Formal](#lean-3-e-prova-formal)

---

## Lógica Proposicional Básica

### Definição

A **lógica proposicional** é um sistema formal que estuda proposições e suas relações através de conectivos lógicos.

#### Proposições Atômicas

Uma **proposição** é uma afirmação que pode ser verdadeira (T) ou falsa (F), mas não ambas.

- **Exemplos**: p, q, r, ...
- **Notação**: Variáveis proposicionais minúsculas

#### Conectivos Lógicos

| Conectivo | Símbolo | Notação | Significado |
|-----------|---------|---------|------------|
| Negação | ¬ | NOT | "não" |
| Disjunção | ∨ | OR | "ou" |
| Conjunção | ∧ | AND | "e" |
| Implicação | → | IMPLIES | "se...então" |
| Bicondicional | ↔ | IFF | "se e somente se" |

### Tabelas de Verdade

#### Negação
| p | ¬p |
|---|-----|
| T | F |
| F | T |

#### Conjunção
| p | q | p ∧ q |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | F |

#### Disjunção
| p | q | p ∨ q |
|---|---|-------|
| T | T | T |
| T | F | T |
| F | T | T |
| F | F | F |

#### Implicação
| p | q | p → q |
|---|---|-------|
| T | T | T |
| T | F | F |
| F | T | T |
| F | F | T |

**Nota**: p → q é falso apenas quando p é verdadeiro e q é falso.

#### Bicondicional
| p | q | p ↔ q |
|---|---|--------|
| T | T | T |
| T | F | F |
| F | T | F |
| F | F | T |

---

## Consequência Lógica

### Definição Formal

Uma conclusão **C** é **consequência lógica** de premissas **P₁, P₂, ..., Pₙ** (notação: P₁, P₂, ..., Pₙ ⊢ C) se:

> Para toda interpretação I, se I satisfaz todas as premissas, então I também satisfaz a conclusão.

### Definição Equivalente (Semântica)

C é consequência lógica de P₁, ..., Pₙ se e somente se não existe interpretação que:
- Torna **todas** as premissas verdadeiras
- E torna a conclusão **falsa**

### Exemplo: Modus Ponens

```
Premissas:
  1. p
  2. p → q

Conclusão: q
```

**Verificação**: 
- Qualquer interpretação que satisfaz ambas as premissas deve ter q = T
- Logo, q é consequência lógica

### Contra-exemplo: Afirmação do Consequente

```
Premissas:
  1. p → q
  2. q

Conclusão: p
```

**Contra-exemplo**:
- p = F, q = T
- p → q = F → T = T ✓
- q = T ✓
- p = F ✗

Portanto, p NÃO é consequência lógica.

---

## Dedução Natural

### Histórico

Desenvolvida por **Gentzen** (1934), a dedução natural é um sistema de prova que modelar o raciocínio matemático natural.

### Conceito Central

Na dedução natural, uma prova é uma sequência de proposições onde cada uma é:
1. Uma **premissa** (hipótese), ou
2. Derivada de proposições anteriores usando uma **regra de inferência**

### Regras de Inferência Principais

#### 1. Introdução da Conjunção
```
  A    B
  ------
  A ∧ B
```
Se provamos A e B, podemos concluir A ∧ B.

#### 2. Eliminação da Conjunção
```
  A ∧ B          A ∧ B
  ------    ou   ------
    A              B
```

#### 3. Introdução da Disjunção
```
  A              B
  ------    ou   ------
  A ∨ B         A ∨ B
```

#### 4. Eliminação da Disjunção (Silogismo Disjuntivo)
```
  A ∨ B    A → C    B → C
  ---------------------------
            C
```

#### 5. Modus Ponens (Eliminação da Implicação)
```
  A    A → B
  ----------
      B
```

#### 6. Introdução da Implicação (Prova Condicional)
```
  Assumindo A, provamos B
  ----------------------
      A → B
```

#### 7. Prova por Contradição
```
  Assumindo ¬A, derivamos contradição
  ----------------------------------
              A
```

#### 8. Lei do Terceiro Excluído
```
  A ∨ ¬A
```

### Exemplo: Prova de Modus Ponens

```
1. p          (premissa)
2. p → q      (premissa)
3. q          (de 1,2 por modus ponens)
```

---

## SAT Solving

### O Problema SAT

**SAT (Boolean Satisfiability)** é o problema de determinar se existe uma atribuição de valores verdade às variáveis de uma fórmula booleana que torna a fórmula verdadeira.

### Forma Normal Conjuntiva (CNF)

Uma fórmula está em **CNF** se é uma conjunção de disjunções de literais:

```
(l₁ ∨ l₂ ∨ l₃) ∧ (l₄ ∨ l₅) ∧ ... ∧ (lₙ)
```

onde cada lᵢ é uma variável ou sua negação.

### Conversão para CNF

**Exemplo**: Converter (p → q) ∧ q para CNF
1. p → q ≡ ¬p ∨ q  
2. (¬p ∨ q) ∧ q
3. Aplicar distribuição se necessário

### Consequência Lógica e SAT

Para verificar se C é consequência de P₁, ..., Pₙ:

1. Crie a fórmula: **Φ = (P₁ ∧ P₂ ∧ ... ∧ Pₙ ∧ ¬C)**
2. Se Φ é **insatisfazível** (UNSAT): C é consequência ✓
3. Se Φ é **satisfazível** (SAT): Existe contra-exemplo ✗

### Algoritmos Principais

#### DPLL (Davis-Putnam-Logemann-Loveland)
- Algoritmo clássico com backtracking
- Base para muitos SAT solvers modernos

#### CDCL (Conflict-Driven Clause Learning)
- Versão moderna do DPLL
- Usado em Z3, MiniSat, CaDiCaL
- Adiciona aprendizado de cláusulas em conflitos

### Z3 Solver

**Z3** é um SMT (Satisfiability Modulo Theories) solver desenvolvido pela Microsoft.

**Características**:
- Suporta múltiplas teorias (booleanas, lineares, não-lineares, etc.)
- Algoritmos otimizados e heurísticas avançadas
- API em múltiplas linguagens (Python, C++, Java, etc.)

**Uso no projeto**:
```python
from z3 import *

# Cria variáveis
p, q = Bools('p q')

# Cria solver
s = Solver()
s.add(p, Implies(p, q), Not(q))

# Verifica
if s.check() == unsat:
    print("Insatisfazível - consequência lógica!")
```

---

## LEAN 3 e Prova Formal

### O que é LEAN?

**LEAN** é um assistente de prova (proof assistant) desenvolvido por Leonardo de Moura.

Permite escrever e verificar formalmente provas matemáticas de forma rigorosa.

### Estrutura Básica de uma Prova LEAN

```lean
theorem theorem_name (p q : Prop) : p → q := by
  intro hp
  exact hp
```

**Componentes**:
- `theorem`: Palavra-chave que declara um teorema
- `theorem_name`: Nome único do teorema
- `(p q : Prop)`: Contexto (variáveis disponíveis)
- `: p → q`: Tipo (proposição a provar)
- `:= by`: Inicia prova tática
- `intro`, `exact`, etc.: Táticas (estratégias de prova)

### Dedução Natural em LEAN

#### Modus Ponens
```lean
theorem modus_ponens (p q : Prop) (hp : p) (hpq : p → q) : q := by
  exact hpq hp
```

#### Silogismo Disjuntivo
```lean
theorem disjunctive_syllogism (p q : Prop) (hpq : p ∨ q) (hnp : ¬p) : q := by
  cases hpq with
  | inl hp => contradiction
  | inr hq => exact hq
```

#### Prova Condicional
```lean
theorem conditional_proof (p q : Prop) (hpq : p → q) : q → q := by
  intro _
  assumption
```

### Táticas Principais

| Tática | Descrição |
|--------|-----------|
| `exact` | Fornece termo que prova exatamente o objetivo |
| `apply` | Aplica função/implicação ao objetivo |
| `intro` | Introduz uma hipótese ou variável quantificada |
| `cases` | Análise por casos (desconstrução) |
| `have` | Prova um lema intermediário |
| `rw` | Reescreve usando igualdade ou equivalência |
| `simp` | Simplificação automática |
| `omega` | Resolve aritmética linear automática |
| `sorry` | Admite um objetivo sem prova (incompleto) |

### Abordagem Term-Mode vs Tactic-Mode

#### Term-Mode (Termo Explícito)
```lean
theorem proof (p q : Prop) (hp : p) (hpq : p → q) : q := hpq hp
```
- Mais conciso
- Requer entender tipos exatamente

#### Tactic-Mode (Táticas)
```lean
theorem proof (p q : Prop) (hp : p) (hpq : p → q) : q := by
  exact hpq hp
```
- Mais legível
- Construção passo a passo

---
