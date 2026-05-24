# Projeto-Pratico-LCOMP
Repositório voltado para entrega do projeto prático proposto na disciplina de Lógica para Computação.

# Proposta

Avaliar raciocínio de LLM com e sem demonstrações em LEAN. Gerar premissas e conclusao diretamente com formulas em logica proposicional.

Usar Z3 pra saber se é consequência lógica. Pedir para a LLM apresentar a prova usando a linguagem LEAN. Checar se a demonstracão está correta. 
Caso nao seja consequencia logica, pedir para a LLM dar um contra exemplo. Checar o contra exemplo. Comparar se acerta mais quando pedimos pra 
fornecer a demonstracao.

Usar o seguinte material sobre LEAN: https://leanprover.github.io/logic_and_proof_lean3/natural_deduction_for_propositional_logic.html

---

# 🚀 Como Executar

## Pré-requisitos
- Docker e Docker Compose instalados
- Chave da API Anthropic (Claude) - [obter aqui](https://console.anthropic.com/)

## Opção 1: Docker Compose (Recomendado)

### 1. Configure a chave da API
```bash
export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
```

### 2. Execute o projeto
```bash
docker-compose up
```

## Opção 2: Com arquivo `.env`

### 1. Crie um arquivo `.env` na raiz do projeto
```bash
cp .env.example .env
# Edite .env e adicione sua chave ANTHROPIC_API_KEY
```

### 2. Execute
```bash
docker-compose up
```

## Opção 3: Shell interativo
```bash
export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
docker-compose run --rm solver bash
python solver.py
```

## Opção 4: Usando Makefile
```bash
make build
export ANTHROPIC_API_KEY='sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
make run
```

---

# 📚 Estrutura do Projeto

```
├── solver.py          # Main - executa os exemplos com Z3 + Claude
├── lean_prover.py     # Integração com Claude API para gerar provas LEAN
├── requirements.txt   # Dependências Python
├── Dockerfile         # Configuração Docker
├── docker-compose.yml # Orquestração de containers
├── Makefile          # Atalhos para comandos comuns
└── README.md         # Este arquivo
```

---

# 🔍 O que o projeto faz

## 1️⃣ Verifica consequência lógica com Z3
- Dado um conjunto de premissas e uma conclusão
- Z3 verifica se é logicamente válido
- Usa SAT solving (insatisfiabilidade)

## 2️⃣ Gera provas em LEAN (Claude)
- Se é consequência: pede prova formal em LEAN 3
- Baseado em natural deduction (dedução natural)
- Segue o material: https://leanprover.github.io/logic_and_proof_lean3/

## 3️⃣ Gera contra-exemplos (Claude)
- Se NÃO é consequência: gera atribuição de valores
- Mostra proposições que falsificam o argumento

---

# 📋 Exemplos Inclusos

1. **Modus Ponens** - Argumento válido clássico
   - Premissas: p, p → q
   - Conclusão: q
   - Resultado: ✓ Válido

2. **Silogismo Disjuntivo** - Outro argumento válido
   - Premissas: p ∨ q, ¬p
   - Conclusão: q
   - Resultado: ✓ Válido

3. **Falácia da Afirmação do Consequente** - Argumento inválido
   - Premissas: p → q, q
   - Conclusão: p
   - Resultado: ✗ Inválido (com contra-exemplo)

4. **Raciocínio Complexo** - Múltiplas proposições
   - Demonstra capacidade com 3+ proposições
   - Z3 + Claude trabalham juntos

---

# 🛠️ Estrutura do Código

### `solver.py`
- **`verificar_consequencia()`**: Usa Z3 para validar
- **`exemplo_X_com_prova()`**: Executa exemplo + Claude
- Trata erros de API graciosamente

### `lean_prover.py`
- **`gerar_prova_lean()`**: Claude gera prova LEAN
- **`gerar_contra_exemplo()`**: Claude gera contra-exemplo
- **`validar_prova_lean()`**: Validação básica de sintaxe
- **`conversa_interativa()`**: Chat com Claude (futuro)

---

# ⚙️ Variáveis de Ambiente

| Variável | Obrigatória | Padrão |
|----------|---|---|
| `ANTHROPIC_API_KEY` | ✅ Sim | - |
| `PYTHONUNBUFFERED` | ❌ Não | 1 |

---

# 🤖 Modelos e Parâmetros

- **Modelo Claude**: `claude-opus-4-7` (mais poderoso para provas LEAN)
- **Max tokens**: 1024 (provas), 512 (contra-exemplos)
- **Sistema prompt**: Especializado em lógica proposicional + LEAN

---

# 📝 Próximas Funcionalidades

- [ ] Validação de provas LEAN via compilação real
- [ ] Comparação: LLM com vs sem demonstrações
- [ ] Benchmark: taxa de acerto por tipo de argumento
- [ ] Interface web para explorar provas interativamente
- [ ] Suporte a quantificadores (FOL - First Order Logic)

---

# 🐛 Troubleshooting

### "ANTHROPIC_API_KEY not configured"
```bash
export ANTHROPIC_API_KEY='sua-chave'
docker-compose up
```

### "Failed building wheel for z3-solver"
Já resolvido via Docker! No container está pré-compilado.

### "Connection timeout" ao chamar Claude
- Verifique sua chave de API
- Verifique sua conexão com internet
- Tente novamente

---

# 📄 Licença

Projeto educacional para disciplina de Lógica para Computação.
