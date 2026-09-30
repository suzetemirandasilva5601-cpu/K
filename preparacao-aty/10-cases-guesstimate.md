# Parte 10 — Cases de Entrevista: Guesstimate, Clarificação, Contas na Folha e Brainstorm

> **Premissa deste documento.** Você ensina case interview, então não vou explicar o que é MECE. O que este documento faz é diferente: mostra **onde o case de consultoria de analytics diverge do case clássico de estratégia**, e treina exatamente essas divergências nos temas reais da ATY.

---

## 10.1 O que muda num case de analytics

Um case de MBB clássico quer saber se você estrutura e calcula. Um case de consultoria de dados quer isso **e mais quatro coisas** — e é aqui que candidatos bem treinados em case tradicional tropeçam:

| Movimento | Case clássico | Case de analytics |
|---|---|---|
| **Dado** | Assume-se disponível | **"Que dado existe?" é pergunta de clarificação obrigatória.** Recomendação que exige dado inexistente não vale nada |
| **Dimensionamento** | Calcula o mercado | **Dimensiona antes de propor solução:** "quanto vale resolver isso?" decide se o projeto existe |
| **Medição** | Recomenda e encerra | **"Como eu provo que funcionou?"** — contrafactual, teste, baseline |
| **Decisão** | Recomendação estratégica | **Quem decide, com que frequência, e em que formato recebe** — define granularidade e latência da solução |
| **Custo** | Ignorado | **Custo de construir e de rodar.** Gilberto destaca "estimativa precisa de custo de processamento" |

**Regra prática:** em todo case da ATY, encaixe estas quatro frases em algum momento:

1. *"Antes de propor, qual dado o cliente tem?"*
2. *"Deixa eu dimensionar o valor em jogo para saber se vale o esforço."*
3. *"E como eu provaria que o efeito foi da intervenção?"*
4. *"Qual a decisão que muda com isso, e quem a toma?"*

---

## 10.2 Framework de condução em 5 fases

```
┌─ 1. CLARIFICAÇÃO ─────────────────────────────────────────────┐
│  Objetivo, escopo, métrica de sucesso, restrição, DADO        │
│  4 a 6 perguntas. Repita o problema com suas palavras.        │
└───────────────────────────────────────────────────────────────┘
                              │
┌─ 2. ESTRUTURAÇÃO ─────────────────────────────────────────────┐
│  Árvore MECE. Diga em voz alta por onde vai começar e por quê.│
│  "Vou atacar o ramo X primeiro porque concentra o valor."      │
└───────────────────────────────────────────────────────────────┘
                              │
┌─ 3. DIMENSIONAMENTO (as contas) ──────────────────────────────┐
│  Números redondos. Verbalize cada passo. Arredonde e corrija  │
│  no fim. SEMPRE faça o teste de sanidade.                     │
└───────────────────────────────────────────────────────────────┘
                              │
┌─ 4. BRAINSTORM ───────────────────────────────────────────────┐
│  Alavancas em buckets MECE. Priorize por impacto × esforço.    │
│  Inclua o que o dado permite E o que ele não permite.         │
└───────────────────────────────────────────────────────────────┘
                              │
┌─ 5. SÍNTESE ──────────────────────────────────────────────────┐
│  Recomendação → número que a sustenta → risco → próximo passo │
│  (que quase sempre é: testar num piloto controlado)           │
└───────────────────────────────────────────────────────────────┘
```

**Disciplinas de condução que valem ponto:**
- **Peça 20 segundos** antes de estruturar. Silêncio pensado > improviso falante.
- **Verbalize a aritmética.** O entrevistador avalia o raciocínio, não a conta.
- **Arredonde com anúncio:** "vou usar 75 milhões de domicílios, arredondando".
- **Teste de sanidade sempre:** divida o resultado por população ou por cliente e pergunte se faz sentido.
- **Nunca dê falsa precisão.** "Da ordem de R$ 2,5 bilhões" é melhor que "R$ 2.447.328.000".

---

## 10.3 Folha de âncoras — Brasil

> **Uso:** são âncoras de **ordem de grandeza** para conta de cabeça, não estatística oficial. Em case interview, consistência importa mais que precisão — e **anunciar a premissa** protege você: se o entrevistador tiver outro número, ele corrige e vocês seguem.

| Âncora | Valor de trabalho |
|---|---|
| População | ~215 milhões |
| Domicílios | ~75 milhões (~2,8 pessoas/domicílio) |
| População urbana | ~87% |
| População ocupada | ~100 milhões |
| Faixas de idade | 0–14: ~20% · 15–64: ~70% · 65+: ~10% |
| Classes | AB: ~20% · C: ~50% · DE: ~30% |
| Salário mínimo | ~R$ 1.500/mês |
| Renda domiciliar média | ~R$ 3.000/mês (mediana bem menor) |
| PIB | ~R$ 12 trilhões/ano |
| Varejo (restrito) | ~R$ 2 trilhões/ano |
| Cidade de SP · Estado de SP | ~12 mi · ~46 mi |
| Região Metrop. de SP · Campinas | ~21 mi · ~1,2 mi |

**Âncoras de negócio úteis:**

| Métrica | Faixa típica |
|---|---|
| Margem bruta — varejo de moda | 50–60% |
| Margem bruta — supermercado | 20–28% |
| Margem bruta — CPG (indústria) | 30–40% |
| Margem líquida — varejo | 2–8% |
| Ruptura de gôndola | 5–10% |
| Receita/m² — loja de shopping | R$ 10–20 mil/m²/ano |
| LTV/CAC saudável | ≥ 3 |
| Taxa de conversão e-commerce | 1–2% |

---

## 10.4 Aritmética de cabeça

**Frações → porcentagem** (decore: elimina 80% da dificuldade)

| 1/3 | 1/6 | 1/7 | 1/8 | 1/9 | 1/11 | 1/12 |
|---|---|---|---|---|---|---|
| 33% | 17% | 14% | 12,5% | 11% | 9% | 8,3% |

**Atalhos:**
- **Regra de 72:** dobra em `72 ÷ taxa%` anos. 8%/ano → ~9 anos.
- **Crescimento composto pequeno:** 5% por 3 anos ≈ 15% + pouco ≈ 16%. (Exato: 15,8%.)
- **Variação conjunta:** preço +5% e volume −6% → `1,05 × 0,94 = 0,987` → −1,3%.
- **Multiplicar por 12:** ×10 + ×2. R$ 17M/mês → 170 + 34 = R$ 204M/ano.
- **Dividir por 7:** ×1,4 e ande a vírgula. 350/7 = 50.

**Ordem de grandeza — sempre confira a casa decimal:**
```
75 milhões × R$ 12  =  7,5×10⁷ × 1,2×10¹  =  9×10⁸  =  R$ 900 milhões
```
Erro de casa decimal é o erro mais grave e o mais comum. Trabalhe em potências de 10 quando o número ficar grande.

---

# Cases completos

---

## CASE 1 — Gestão de Categoria e Pricing
### Tema ATY: oferta nº 1 · Cliente análogo: Aramis

### O enunciado (como o entrevistador daria)

> *"Uma rede de moda masculina premium quer aumentar a rentabilidade sem perder volume de vendas. Eles acham que estão dando desconto demais, mas o time comercial diz que sem desconto não vende. Como você abordaria?"*

### Fase 1 — Clarificação (faça 4-6, não mais)

| Pergunta | Por que ela importa |
|---|---|
| "Rentabilidade — margem bruta, ou resultado operacional? Preciso saber se custo de loja está no escopo" | Define a árvore inteira |
| "'Sem perder volume' — volume em unidades ou em receita? São coisas diferentes e podem entrar em conflito" | Define a restrição, e mostra rigor |
| "Quantas lojas, e qual a divisão entre físico e e-commerce?" | Dimensionamento e viabilidade de teste |
| **"Que dado existe? Tenho histórico de preço por SKU e por loja, calendário promocional, estoque e preço de concorrente?"** | **A pergunta que distingue case de analytics** |
| "Há restrição de posicionamento de marca? Em premium, desconto agressivo pode ser proibido pela estratégia" | Restrição não-quantitativa que muda a recomendação |
| "Qual o horizonte? Uma coleção ou o ano?" | Moda tem ciclo; muda a alavanca |

**Suposições que o entrevistador te daria:** 60 lojas, receita ~R$ 240M/ano, margem bruta 55%, ~30% da receita sai com desconto, desconto médio de 40%, histórico de 3 anos por SKU/loja disponível.

### Fase 2 — Estruturação

```
RENTABILIDADE
│
├── RECEITA
│   ├── Volume  ──── tráfego × conversão × itens por cesta
│   └── Preço   ──── preço cheio · profundidade do desconto · TIMING do desconto
│
├── CUSTO DO PRODUTO VENDIDO
│   ├── Custo de compra / produção
│   └── Mix ────── participação de categorias de margem diferente
│
└── PERDA DE VALOR
    ├── Markdown de fim de coleção (sobra)
    └── Ruptura de tamanho/cor (venda perdida com estoque na rede)
```

**Onde começar, e diga isso em voz alta:**
> "Vou atacar primeiro **preço e timing de markdown**, por duas razões: é onde o cliente já suspeita que há problema, e em moda o markdown é geralmente a maior fonte de destruição de margem — porque o desconto é decidido por calendário, não por comportamento de venda do SKU."

### Fase 3 — Dimensionamento (as contas, passo a passo)

**a) Quanto vale 1 ponto percentual de margem?**

```
Receita anual                    R$ 240 M
1 p.p. de margem sobre receita   240 × 1%  =  R$ 2,4 M/ano
```

> "Então cada ponto percentual vale R$ 2,4 milhões. Isso já me diz que o projeto se paga com folga se eu conseguir mover 1 ou 2 pontos."

**b) Dimensionar o desconto concedido**

```
Receita com desconto      240 × 30%           =  R$ 72 M
Desconto médio 40% → o preço cheio seria      72 ÷ 0,60  =  R$ 120 M
Desconto concedido        120 − 72            =  R$ 48 M/ano
```

> "São R$ 48 milhões de desconto por ano. Esse é o pote onde está o dinheiro."

**c) Alavanca: reduzir a profundidade média do desconto em 4 p.p. (40% → 36%)**

```
Ganho  =  R$ 120 M (receita a preço cheio)  ×  4%  =  R$ 4,8 M/ano
       ≈  2 p.p. de margem
```

**d) A conta que resolve a objeção do time comercial**

> "O time comercial diz que sem desconto não vende. Deixa eu testar isso com elasticidade. Suponha elasticidade de −1,2, que é plausível em premium, e um aumento de 5% no preço:"

```
Volume:   −1,2 × 5%  =  −6%
Receita:  1,05 × 0,94  =  0,987   →  −1,3%   (cai!)

Margem, com preço 100 e custo 45:
  Antes:  100 un × (100 − 45)  =  5.500
  Depois:  94 un × (105 − 45)  =  5.640      →  +2,5%   (sobe!)
```

> **"E aqui está o ponto central: a receita cai 1,3% e a margem sobe 2,5%. O time comercial está otimizando a métrica errada — ele é medido por faturamento, e faturamento e margem apontam em direções opostas quando a elasticidade é menor que a razão preço/margem. Isso não é um problema de modelo, é um problema de incentivo."**

☝️ **Esta é a resposta que fecha o case.** E conecta com o case real da ATY: "+7 p.p. de lucro **sem mudança de margem**, superando o time comercial em +20 p.p. na mesma cesta" — ou seja, eles provaram exatamente isso, com teste.

**e) Teste de sanidade**

```
Ganho potencial ≈ R$ 5 M  sobre receita de R$ 240 M  ≈  2% da receita
O case real da ATY foi +7 p.p. de lucro  ≈  R$ 17 M
```
> "Minha estimativa de R$ 5 milhões é conservadora e da ordem de grandeza certa. Faz sentido."

### Fase 4 — Brainstorm de alavancas (MECE)

**Preço**
- Repricing por elasticidade estimada por categoria (não por SKU — ruído)
- Preço diferenciado por cluster de loja (região, perfil de público)
- Alinhamento de preço relativo a substitutos

**Markdown (a maior alavanca em moda)**
- Markdown acionado por **velocidade de venda e cobertura de estoque**, não por calendário
- Profundidade escalonada: 20% → 30% → 50%, em vez de 40% direto
- Markdown por tamanho/cor: a grade quebrada é o que realmente não vende

**Sortimento e mix**
- Aumentar participação de categorias de margem alta na vitrine
- Cortar cauda longa de SKU que só gera markdown

**Dado / capacidade**
- Estimar elasticidade com o histórico de 3 anos, controlando sazonalidade e promoção
- **Experimento de preço em lojas pareadas** — a única forma de elasticidade limpa

**O que o dado NÃO permite** (diga isso — é rigor):
- Sem preço de concorrente, não dá para estimar elasticidade cruzada
- Sem dado de tráfego de loja, não dá para separar queda de conversão de queda de fluxo

### Fase 5 — Síntese

> "Recomendo atacar **timing e profundidade de markdown** antes de mexer no preço cheio. Três razões: é onde estão os R$ 48 milhões de desconto concedido; reduzir 4 pontos na profundidade média vale cerca de R$ 4,8 milhões, o equivalente a 2 pontos de margem; e não exige mexer no posicionamento de preço da marca, que é uma restrição de premium.
>
> O risco é canibalização e percepção de marca, então eu não faria roll-out direto. Faria um piloto em lojas pareadas por porte e região, com uma coleção, medindo **margem de categoria** — não de SKU — para capturar canibalização, e com volume como guardrail.
>
> E o achado que eu levaria para a diretoria não é o modelo: é que o time comercial é medido por faturamento enquanto a empresa quer margem. Sem corrigir o incentivo, o modelo não vai ser seguido."

---

## CASE 2 — Market Sizing em Bens de Consumo
### Tema ATY: projeção de mercado e go-to-market · Cliente análogo: Kraft Heinz

### O enunciado

> *"Dimensione o mercado brasileiro de ketchup."*

### Fase 1 — Clarificação

| Pergunta | Por quê |
|---|---|
| "Mercado em valor (R$) ou volume (toneladas/unidades)?" | Muda a conta |
| "Inclui food service — lanchonete, restaurante, fast food — ou só varejo para consumo doméstico?" | Em condimentos, food service é parcela grande |
| "Preço ao consumidor ou preço ao fabricante?" | Diferença de ~40-50% |
| "Só ketchup ou a categoria de condimentos?" | Escopo |

**Defina em voz alta:** "Vou dimensionar **valor, a preço de consumidor, no canal varejo**, e depois adiciono food service como bloco separado."

### Fase 2 — Estruturação

```
MERCADO = Domicílios consumidores × Frequência de compra × Preço
                    │
    Domicílios totais × Penetração da categoria
```

### Fase 3 — Dimensionamento

**Canal varejo:**

```
Domicílios no Brasil                      75 milhões
Penetração de ketchup                     ~45%
  (premissa: é mais discricionário que molho de tomate,
   concentrado em AB/C urbano — AB+C ≈ 70%, e nem todos compram)

Domicílios consumidores    75 × 0,45   =  34 milhões

Frequência: 1 frasco a cada 2 meses  =  0,5 frasco/mês
Frascos/mês       34 × 0,5           =  17 milhões
Frascos/ano       17 × 12            =  204 milhões

Preço médio (frasco ~400 g)          =  R$ 12

MERCADO VAREJO   204 M × 12          =  R$ 2,45 bilhões/ano
```

**Food service:**
```
Premissa: food service ≈ 30% do consumo total da categoria
Total  =  2,45 ÷ 0,70  ≈  R$ 3,5 bilhões/ano
Food service ≈ R$ 1,0 bilhão
```

**Testes de sanidade — faça DOIS:**

```
1) Por habitante:  2,45 bi ÷ 215 mi  =  R$ 11,4/pessoa/ano
   ≈ um frasco por pessoa por ano. Plausível.

2) Contra o varejo total: 3,5 bi ÷ 2 trilhões = 0,18% do varejo brasileiro
   Para uma categoria de condimento, plausível.
```

> "Então: da ordem de **R$ 2,5 bilhões no varejo e R$ 3,5 bilhões incluindo food service**. Eu trataria como ordem de grandeza, não como número fechado."

### Fase 4 — Brainstorm: onde a estimativa mais erra?

- **Penetração** é a premissa mais frágil e a de maior alavanca. Errar de 45% para 60% muda o resultado em 33%.
- **Frequência** varia muito por classe social — o certo seria segmentar AB / C / DE com frequências diferentes.
- **Preço** varia por embalagem (sachê, frasco, galão food service) — mix de embalagem importa.
- **Como validar:** dado de *retail measurement* (Nielsen/Scanntech), pesquisa de painel de domicílio, ou dado de sell-out do próprio cliente.

### Fase 5 — Síntese com utilidade de negócio

> "R$ 3,5 bilhões é o tamanho. Mas para uma decisão de go-to-market, o número sozinho não serve — o que decide é onde está o crescimento. Eu quebraria por classe social e região, porque a alavanca de penetração em DE é conquista de novos domicílios, e em AB é frequência e ocasião de consumo. São estratégias e investimentos diferentes, e é aí que o dimensionamento passa a valer alguma coisa."

---

## CASE 3 — Supply Chain e Ruptura
### Tema ATY: oferta nº 2 · Cliente análogo: Maravilhas do Lar

### O enunciado

> *"Uma rede de utilidades domésticas do interior de São Paulo tem 5 lojas e quer abrir mais 5 nos próximos dois anos. A operação reclama de ruptura de estoque. Vale a pena investir num projeto de previsão de demanda?"*

### Fase 1 — Clarificação

| Pergunta | Por quê |
|---|---|
| **"Ruptura medida como? Percentual de SKUs em falta na gôndola, ou percentual de ocasiões de compra que não encontram o item?"** | **Definições completamente diferentes** — e a segunda é a que importa |
| "Faturamento aproximado da rede?" | Dimensionamento |
| "Quantos SKUs? Utilidades domésticas costuma ter cauda longa enorme" | Complexidade do problema |
| "Existe histórico de venda por SKU e por loja? Por quanto tempo? Há registro de ruptura?" | **Sem registro de ruptura, a venda perdida é invisível no dado** |
| "A dor é ruptura ou é capital preso em estoque? Pode ser os dois ao mesmo tempo" | Reenquadra o problema |

**Suposições dadas:** faturamento R$ 50M/ano, ruptura de 8%, margem bruta 35%, 3 anos de histórico de venda por SKU/loja, **sem** registro formal de ruptura.

### Fase 2 — Dimensionamento (e este case ensina algo importante)

```
Faturamento                                    R$ 50 M/ano
Ruptura                                        8% das ocasiões
Mas ruptura ≠ venda perdida: parte substitui
Premissa: 50% substitui por outro item, 50% se perde

Venda perdida   50 M × 8% × 50%          =   R$ 2,0 M/ano
Margem perdida  2,0 M × 35%              =   R$ 0,7 M/ano

Meta: reduzir ruptura de 8% para 5%
  (referência: o Gilberto reduziu de 10% para 5% na Ultrapar)
Recuperação     0,7 M × (3/8)            =   R$ 262 mil/ano
```

> **"E aqui eu paro, porque o dimensionamento mudou a resposta. Recuperar R$ 262 mil por ano não paga um projeto de forecasting com modelo estatístico, integração e sustentação. Meu instinto inicial estava errado, e o número é que me disse isso."**

☝️ **Este é o case mais valioso do conjunto**, porque demonstra a disciplina que a ATY valoriza: **dimensionar antes de propor.** Um candidato que constrói o projeto sem dimensionar propõe queimar dinheiro do cliente.

### Fase 3 — Reenquadramento

> "Então eu reenquadro. Se o valor não está na ruptura das 5 lojas atuais, onde está?
>
> **Na expansão.** Abrir 5 lojas dobra a rede. E a decisão de **sortimento inicial de uma loja nova** é de altíssimo valor e altíssima incerteza: errar o sortimento de abertura significa capital preso em item que não gira e falta do que vende. Não há histórico da loja nova — então é um problema de previsão sem série própria, resolvido por analogia entre lojas.
>
> Isso vale muito mais que 262 mil por ano, e é um problema genuinamente analítico."

**Dimensionamento do reenquadramento:**
```
5 lojas novas × estoque inicial de R$ 400 mil   =  R$ 2,0 M de capital alocado
Se 25% do sortimento inicial for errado          =  R$ 500 mil mal alocados
  + margem perdida nos itens que faltaram
```
> "Aqui o valor em jogo é de ordem superior, e numa decisão que acontece 5 vezes nos próximos 2 anos."

### Fase 4 — Brainstorm

**Se a dor for ruptura (baixa prioridade):** política de estoque de segurança por classe ABC; revisão de ponto de pedido; nível de serviço diferenciado por giro. Não precisa de ML — precisa de regra bem calibrada.

**Se a dor for expansão (alta prioridade):**
- Clusterizar as 5 lojas existentes por perfil de demanda e usar a loja mais parecida como semente do sortimento da nova
- Modelar demanda por **categoria** na abertura (grão fino não tem sinal) e refinar por SKU com as primeiras semanas de venda real
- Curva de maturação de loja nova: quanto tempo até o regime, para não confundir rampa com erro de previsão

**O bloqueio de dado, e ele é sério:**
> "Sem registro de ruptura, a venda perdida não existe no dado — o histórico mostra venda zero, que o modelo vai aprender como 'não há demanda'. É censura, e enviesa a previsão para baixo exatamente nos itens que mais faltam. A primeira entrega do projeto provavelmente é instrumentar a medição de ruptura, não o modelo."

### Fase 5 — Síntese

> "Minha recomendação é **não** fazer o projeto de forecasting que eles pediram. A ruptura atual vale cerca de R$ 260 mil por ano em margem, o que não paga a solução.
>
> O valor está na **decisão de sortimento das lojas novas**, que envolve R$ 2 milhões de capital e se repete 5 vezes. Eu proporia começar por aí, com clusterização das lojas atuais para servir de semente, e com uma entrega intermediária de instrumentação da medição de ruptura — porque sem ela nenhum modelo de demanda vai ser confiável, hoje ou depois."

---

## CASE 4 — Alocação de Verba de Marketing
### Tema ATY: oferta nº 3 · Território que você viveu na V4

### O enunciado

> *"Um cliente investe R$ 500 mil por mês em mídia, dividido em três canais. Quer saber se está alocando bem. Como você responde?"*

### Fase 1 — Clarificação

| Pergunta | Por quê |
|---|---|
| "Objetivo é volume de clientes novos, receita, ou lucro?" | Muda a métrica de otimização |
| "Como a conversão é atribuída hoje? Last-click?" | **Atribuição é o cerne do problema** |
| "É negócio de compra recorrente ou única? Preciso saber se LTV entra" | Define se CAC pode ser maior que a primeira margem |
| "Tenho dado a nível de usuário ou só agregado por canal?" | Define o que é possível analisar |
| "Já rodaram algum teste — pausaram canal, variaram verba por região?" | Existe variação exógena para explorar? |

**Dados dados:**

| Canal | Investimento | Clientes novos | CAC |
|---|---|---|---|
| A | R$ 200 mil | 1.000 | **R$ 200** |
| B | R$ 250 mil | 500 | **R$ 500** |
| C | R$ 50 mil | 200 | **R$ 250** |

Ticket médio R$ 150 · margem de contribuição 40% · 4 pedidos/ano · vida média 2 anos.

### Fase 2 — Dimensionamento

**LTV:**
```
Margem por pedido      150 × 40%        =  R$ 60
Pedidos na vida        4/ano × 2 anos   =  8
LTV (sem desconto)     60 × 8           =  R$ 480

Com desconto a valor presente (10% a.a., ~metade no ano 2):
LTV ≈ 60×4 + (60×4)/1,10  =  240 + 218  =  R$ 458
```
> "Vou usar R$ 460. Desconto importa porque metade do valor vem no segundo ano — e ignorar isso superestima o LTV."

☝️ **Aqui você usa Matemática Financeira e Finanças Corporativas.** A maioria dos candidatos calcula LTV sem desconto. **Descontar é o seu diferencial natural — não deixe passar.**

**LTV/CAC e payback:**

| Canal | CAC | LTV/CAC | Payback |
|---|---|---|---|
| A | 200 | **2,3** | 200/240 ≈ 0,8 ano |
| B | 500 | **0,9** ⚠️ | não paga na vida do cliente |
| C | 250 | **1,8** | ~1 ano |

**Conclusão ingênua:** matar B, migrar os R$ 250 mil para A.

### Fase 3 — Por que a conclusão ingênua está errada (é aqui que o case se decide)

> "Antes de recomendar isso, três problemas.
>
> **Primeiro: CAC médio não é CAC marginal.** O canal A tem CAC de R$ 200 nos R$ 200 mil atuais. Isso não significa que os próximos R$ 250 mil virão a R$ 200. Canal satura: você esgota o público de melhor resposta e o CAC marginal sobe. É perfeitamente possível que os R$ 250 mil adicionais em A venham a R$ 400 de CAC.
>
> **Segundo: atribuição.** Se é last-click, o canal B pode estar **gerando demanda que A colhe**. Canal de topo de funil aparece mal no last-click por construção. Desligar B pode derrubar a performance de A — e aí você destrói valor achando que otimizou.
>
> **Terceiro: LTV pode diferir por canal.** Cliente que vem de um canal caro pode ter retenção maior. Comparar CAC com um LTV médio único esconde isso."

### Fase 4 — Brainstorm de como resolver de verdade

**O que fazer com o dado existente**
- Recalcular LTV **por canal de origem**, não médio
- Curva de CAC vs. investimento ao longo do histórico, para enxergar saturação
- Análise de caminho de conversão, se houver dado de multi-touch

**O que exige experimento (e é a resposta certa)**
- **Geo-experiment:** desligar ou reduzir B em um conjunto de praças comparáveis e medir o efeito no total de clientes novos — não só nos atribuídos a B. É o teste que revela demanda incremental.
- **Escalar A em degraus** (+20%, +40%) medindo CAC marginal em cada degrau
- Dimensionar antes: com ~1.700 clientes/mês, detectar efeito de 10% exige quantos meses? Isso decide se o teste é viável

**Estrutura de decisão final**
- Alocar até onde **CAC marginal = LTV ÷ meta de LTV/CAC** (ex.: 460/3 ≈ R$ 153)
- Guardrail: manter investimento mínimo de topo de funil, porque cortar tudo hoje aparece como ganho e cobra o preço em 3 meses

### Fase 5 — Síntese

> "Não recomendo realocar com base nesses números, e a razão é que eles medem CAC médio com atribuição last-click — que é exatamente o desenho que penaliza canal de geração de demanda.
>
> Recomendo duas coisas. Primeira, recalcular LTV por canal de origem e com desconto a valor presente, porque o LTV médio de R$ 460 pode estar escondendo diferenças que mudam a conclusão. Segunda, e mais importante, rodar um geo-experiment desligando B em praças comparáveis por dois ciclos de compra. Se o total de clientes novos não cair, B é realmente ineficiente e aí o corte está justificado com contrafactual. Se cair, descobrimos que B gera a demanda que A estava levando o crédito.
>
> O que eu não faria é a realocação imediata. O ganho aparente é de R$ 250 mil por mês mal alocados; o risco é destruir o topo do funil por um artefato de atribuição."

---

## CASE 5 — Business Case de um Agente de IA
### Tema ATY: oferta nº 4 ("agentes inteligentes", "torres de controle")

### O enunciado

> *"Um cliente quer um agente de IA que monitore a performance comercial e avise quando algo sair da curva. Vale a pena?"*

### Fase 1 — Clarificação

| Pergunta | Por quê |
|---|---|
| "Qual decisão muda quando o alerta chega? Quem age, e em quanto tempo?" | **Se nada muda, o projeto não existe** |
| "Hoje como isso é detectado, e com quanto de atraso?" | Define o ganho real |
| "Frequência necessária: diária, semanal?" | Define custo de execução |
| "O que é 'fora da curva'? Existe definição ou é preciso construir?" | Metade do trabalho pode estar aqui |
| "A base de performance já existe e é confiável?" | Sem dado confiável, agente amplifica erro |

### Fase 2 — Dimensionamento dos dois lados

**Custo:**
```
Desenvolvimento   2 pessoas × 2 meses                    ≈  R$ 120 mil
Execução          1.000 execuções/mês × ~15 chamadas
                  de LLM × custo por chamada             ≈  R$ 2-5 mil/mês
Sustentação       manutenção, observabilidade            ≈  R$ 3 mil/mês
                                                    ────────────────────
Ano 1  ≈  120 mil + 12 × 7 mil  ≈  R$ 205 mil
```

**Ganho — versão ingênua (economia de hora):**
```
Analista gasta 10 h/semana montando relatório  =  40 h/mês
Custo-hora carregado                           ≈  R$ 80
Economia                40 × 80 × 12           =  R$ 38 mil/ano
```
> "Só com economia de hora, o payback é de mais de 5 anos. **Não se justifica.** E é assim que a maior parte dos projetos de automação é vendida — erradamente."

**Ganho — versão correta (velocidade de detecção):**
```
Premissa: um desvio comercial não detectado custa R$ 100 mil/mês
Hoje é detectado no fechamento: atraso médio  ≈  3 semanas
Com monitoramento diário: atraso              ≈  2 dias

Ganho por evento      R$ 100 mil × (19/30 de mês)  ≈  R$ 63 mil
Se ocorrem 4 eventos relevantes/ano                =  R$ 250 mil/ano
```
> **"Agora o payback é de menos de um ano. E o insight é que o valor do agente não está em economizar hora de analista — está em comprimir o tempo entre o desvio acontecer e alguém agir. Se o cliente estiver comprando economia de mão de obra, ele está comprando a coisa errada e vai se decepcionar."**

### Fase 3 — Brainstorm: agente é a solução certa?

**Escada de solução, do mais barato ao mais caro:**

| Nível | Solução | Quando basta |
|---|---|---|
| 1 | Query agendada + alerta por regra (limite fixo) | Desvio é bem definido e estável |
| 2 | Detecção estatística de anomalia (banda de controle) | Desvio depende de sazonalidade e variância |
| 3 | Camada de diagnóstico: alerta + decomposição automática da causa | Saber *que* desviou não basta; precisa saber *onde* |
| 4 | **Agente**: investiga cruzando fontes, encadeia passos, entrega hipótese | Caminho de investigação não é previsível de antemão |

> "Eu começaria pelo nível 2 e entregaria valor em semanas. O nível 4 se justifica quando a investigação é genuinamente ramificada — quando a próxima pergunta depende da resposta da anterior. Aí um agente com acesso a ferramentas faz sentido de verdade, e é isso que eu entendo por 'torre de controle orquestrando ponta a ponta'."

**Riscos a levantar (e eles pontuam):**
- **Custo variável imprevisível:** agente que encadeia chamadas tem consumo que escala com a complexidade do caso, não com o número de casos. Precisa de teto e monitoramento.
- **Observabilidade:** agente erra de forma menos previsível que regra. Sem log do raciocínio, não é depurável.
- **Fadiga de alerta:** o modo mais rápido de matar o projeto é gerar alerta demais. Precisão importa mais que recall aqui.
- **Confiança:** primeiro alerta errado com visibilidade alta custa a adoção.

### Fase 4 — Síntese

> "Vale a pena, mas não pelo motivo que o cliente deu, e não no nível de sofisticação que ele pediu.
>
> Não se justifica por economia de hora de analista: são R$ 38 mil por ano contra R$ 205 mil de custo no primeiro ano. Justifica-se por compressão do tempo de detecção — se um desvio custa R$ 100 mil por mês e a gente reduz o atraso de três semanas para dois dias, o valor é da ordem de R$ 250 mil por ano.
>
> Eu começaria por detecção estatística com banda de controle e uma camada de decomposição de causa, que entrega em semanas. O agente propriamente dito eu construiria depois, quando a gente souber quais investigações são realmente ramificadas — e com teto de custo definido desde o início, porque consumo de agente escala com complexidade, não com volume."

---

## CASE 6 — Inadimplência e Desenho de Teste
### Tema ATY: território direto do André Shirassu · Espelha seu case real

### O enunciado

> *"Uma empresa tem carteira de recebíveis de R$ 50 milhões e inadimplência de 6%. Quer reduzir. Como você abordaria, e como provaria que funcionou?"*

### Fase 1 — Clarificação

| Pergunta | Por quê |
|---|---|
| "Inadimplência definida como? Vencido acima de quantos dias?" | Muda o número e a meta |
| "Carteira B2B ou B2C? Quantos sacados?" | **Determina se um teste é estatisticamente viável** |
| "A perda é definitiva ou há recuperação posterior?" | Diferença entre atraso e perda |
| "Existe análise de crédito na entrada hoje?" | Prevenção vs. recuperação |
| "Tenho histórico de comportamento de pagamento por sacado?" | Viabilidade de score |

### Fase 2 — Dimensionamento

```
Carteira                     R$ 50 M
Inadimplência 6%             R$ 3,0 M
1 p.p. de redução            R$ 500 mil
```
> "Cada ponto percentual vale R$ 500 mil. Isso paga um projeto sério."

### Fase 3 — Estruturação das alavancas por momento

```
INADIMPLÊNCIA
│
├── ENTRADA (prevenção)      score de crédito, limite, garantia,
│                            condição de pagamento por risco
│
├── VIGÊNCIA (timing)        cobrança ANTES do vencimento,
│                            lembrete, controle diário de vencimento
│
└── ATRASO (recuperação)     régua de cobrança, negociação,
                             priorização por valor × probabilidade
```

> "Eu atacaria **timing** primeiro, e por uma razão de custo de implementação: não exige modelo, exige processo. Cobrança que sai antes do vencimento recupera mais que cobrança depois do atraso. É a alavanca de maior relação impacto/esforço."

☝️ **Aqui você conecta com sua experiência real, e essa é a jogada:** *"Isso é exatamente o que eu implementei na V4 — um controle diário de vencimentos que antecipou a cobrança."*

### Fase 4 — A parte que decide o case: como provar

> "Agora a parte da medição, e é onde eu quero ser rigoroso, porque comparar antes e depois não prova nada — confunde o efeito da intervenção com mudança de mix de clientes e com conjuntura.
>
> O correto é dividir a carteira em dois grupos comparáveis e aplicar a régua nova em um só. Mas antes de propor isso, eu preciso checar se o teste é **viável**:"

**Cálculo de tamanho de amostra:**
```
Regra prática (proporções):   n por grupo ≈ 16 × p(1−p) / δ²

p = 6% = 0,06  ·  detectar δ = 1 p.p. = 0,01

n ≈ 16 × (0,06 × 0,94) / 0,0001
  =  16 × 0,0564 / 0,0001
  ≈  9.000 contas por grupo
```

> **"E aqui está o problema. Se for B2C com centenas de milhares de contas, tranquilo. Mas se for uma carteira B2B com, digamos, 500 sacados, eu precisaria de 18 mil contas para detectar 1 ponto percentual — e eu tenho 500. O teste é inviável, e descobrir isso antes de rodar é a diferença entre um projeto honesto e três meses gastos para chegar a 'inconclusivo'."**

**As três saídas, e saber escolher é o que se avalia:**

1. **Aumentar o MDE.** Com 500 contas, só dá para detectar efeito grande. Aceitar que o teste responde "o efeito é grande?" e não "o efeito é de 1 ponto?".
2. **Mudar para métrica contínua.** Em vez de taxa de inadimplência (binária, baixa variância de sinal), medir **DSO — prazo médio de recebimento**. Métrica contínua tem muito mais poder estatístico com a mesma amostra, e é o efeito de primeira ordem da intervenção. **Esta é geralmente a resposta certa.**
3. **Desenho longitudinal.** Escalonar a implantação em ondas por carteira e usar diferenças-em-diferenças, com cada onda servindo de controle temporário para a seguinte.

### Fase 5 — Síntese

> "Cada ponto percentual de inadimplência vale R$ 500 mil, então o projeto se justifica. Eu atacaria timing de cobrança primeiro, porque é processo e não modelo — implementação rápida e barata.
>
> Sobre a medição, eu não prometeria medir a queda de inadimplência: com carteira pequena, eu precisaria de milhares de contas por grupo para detectar 1 ponto percentual, e provavelmente não tenho isso. Eu mediria **DSO**, que é contínuo, tem muito mais poder estatístico, e é o mecanismo direto pelo qual a intervenção age. A inadimplência eu acompanharia como métrica secundária, sabendo que não vou conseguir atribuição limpa nela.
>
> Depois, se o timing funcionar, aí entra o modelo de score na entrada — que é onde está o ganho estrutural, mas exige histórico e leva mais tempo."

---

## 10.5 Drills rápidos de guesstimate

> Faça em **3 minutos cada**, verbalizando. O objetivo é fluência, não precisão.

| # | Pergunta | Caminho | Ordem de grandeza |
|---|---|---|---|
| 1 | Lojas de moda masculina em shoppings no Brasil | ~600 shoppings × ~8 lojas de moda masc. | ~5 mil |
| 2 | Cafés vendidos por dia em SP capital | 12 mi × 50% consome × 1,5 café/dia | ~9 milhões |
| 3 | Mercado de e-commerce de moda no Brasil | Varejo 2 tri × ~6% moda = 120 bi × ~15% online | ~R$ 18 bi |
| 4 | Litros de gasolina/mês no Brasil | ~40 mi de autos × 100 L/mês × 60% gasolina | ~2,4 bi L |
| 5 | Receita anual de uma loja de shopping de 100 m² | 100 m² × R$ 15 mil/m²/ano | ~R$ 1,5 mi |
| 6 | Consultas médicas/ano no Brasil | 215 mi × ~2,5 consultas/ano | ~540 milhões |
| 7 | Nº de padarias no Brasil | 75 mi domicílios ÷ ~1.200 domicílios/padaria | ~60 mil |
| 8 | Mercado de seguro de automóvel | 40 mi autos × 30% segurados × R$ 2,5 mil | ~R$ 30 bi |

**Para cada um, treine o fechamento:** *"da ordem de X — e a premissa mais frágil é Y, que se eu errasse pela metade mudaria o resultado em Z"*.

---

## 10.6 Erros que derrubam candidatos em case de analytics

| Erro | Correção |
|---|---|
| **Não perguntar que dado existe** | É a pergunta que define se a recomendação é executável |
| **Propor modelo antes de dimensionar** | Case 3 existe para treinar isso: o número pode dizer "não faça" |
| **Confundir receita e margem** | Case 1: receita cai e margem sobe. São direções opostas |
| **Ignorar canibalização** | Sempre avalie no nível de categoria, não de SKU |
| **Não propor contrafactual** | "Como eu provo que foi a intervenção?" tem que sair da sua boca |
| **Não checar viabilidade do teste** | Case 6: teste sem poder estatístico é desperdício planejado |
| **Falsa precisão** | "R$ 2,45 bilhões" quando a penetração é chute vale menos que "da ordem de R$ 2,5 bi" |
| **Não fazer teste de sanidade** | Divida por população ou por cliente. Sempre |
| **Esquecer o custo de rodar** | Gilberto cobra isso explicitamente |
| **Calcular fluxo futuro sem desconto** | Case 4: LTV sem valor presente superestima. **Este é o seu terreno — não erre** |

---

## 10.7 Seus quatro diferenciais em case, e como ativá-los

1. **Desconto a valor presente.** Você tem Matemática Financeira e CFA. Quando aparecer LTV, payback ou fluxo plurianual, **desconte** — a maioria não faz.
2. **Leitura de margem e DRE.** Decomposição volume × preço × mix × custo você faz de cabeça. Use no Case 1.
3. **Elasticidade e endogeneidade.** Você sabe *por que* a estimativa ingênua é enviesada. Isso soa avançado e é só a sua graduação.
4. **Viabilidade estatística do teste.** Calcular tamanho de amostra e concluir "esse teste é inviável" é raro e impressiona — é o Case 6.

E o seu diferencial de condução: **você avalia candidatos em banca.** Você sabe que o que se julga é o raciocínio visível, não a resposta. Então verbalize tudo — inclusive a dúvida e a premissa que você está escolhendo.
