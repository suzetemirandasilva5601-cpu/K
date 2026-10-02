# Briefing Pré-Entrevista — ATY Consulting

**Matteo Lucato** · consulta rápida · 4 blocos

---

## BLOCO 1 — Projeto em Python e SQL

> O bullet do CV: *"modelos preditivos em Python e rotinas de extração em SQL, Saúde e Transporte, bases com mais de 1,2 milhão de registros"*. É o que mais vão aprofundar. **Decida hoje: você sustenta o detalhe ou reduz a afirmação. Não improvise.**

### A estrutura de resposta — 5 passos, nesta ordem

```
1. PROBLEMA   qual era a pergunta de negócio e quem decidia com a resposta
2. DADO       de onde vinha, qual grão, o que estava sujo
3. MÉTODO     o que você fez e POR QUÊ (o "por quê" vale mais que o "o quê")
4. VALIDAÇÃO  como testou e contra qual baseline
5. LIMITE     o que você faria diferente hoje
```

**Comece pelo passo 1 sempre.** Candidato júnior começa pelo algoritmo; quem entende consultoria começa pela decisão.

### O argumento que amarra tudo — decore

> "A base não cabia no Excel: 1,2 milhão de linhas passa do limite de pouco mais de um milhão da planilha. Foi por isso que o trabalho foi para SQL e Python. Filtrei e agreguei no banco e trouxe para o Python já no grão da análise. E 1,2 milhão cabe em pandas — não precisava de Spark, e eu prefiro não inventar complexidade que o problema não pede."

**Por que funciona:** é verificável, explica a escolha de ferramenta por restrição real, e mostra dimensionamento correto nas duas direções.

### Respostas para os 6 ataques mais prováveis

| Pergunta | Resposta |
|---|---|
| **"Qual algoritmo?"** | Se foi regressão logística/linear, **defenda, não se desculpe**: *"escolhi por interpretabilidade — o cliente precisava entender por que o modelo apontava um caso, não só receber o score. Modelo que ninguém entende não é seguido."* |
| **"Qual métrica e qual valor?"** | Se não guardou: *"avaliei com [métrica], mas não guardei o valor exato e não vou chutar. O que eu lembro é a comparação que importava: batia o baseline de [regra atual]."* |
| **"Como validou?"** | *"Split simples de treino e teste. Hoje eu faria diferente: se houver ordem temporal, split aleatório vaza futuro no treino e infla a performance — o correto é corte temporal. E usaria cross-validation, porque um split só pode ser sorte."* |
| **"Qual era o baseline?"** | *"A regra que o cliente já usava — [média histórica / critério manual]. Isso importa mais que a métrica absoluta, porque mede valor incremental."* |
| **"Como tratou 1,2M registros?"** | Agregação no SQL antes; pandas depois; cuidado com tipo de dado; operação vetorizada em vez de `apply`. |
| **"O modelo foi usado?"** | Se não: *"foi projeto de clube, com escopo de clube. Entregamos análise e recomendação, sem implantação. O que eu levei foi tratamento de dado e definição de problema."* |

### As 3 armadilhas

**1. Vazamento de dados** — *"a checagem que eu faria: para cada variável, no momento real da predição, esse campo já está preenchido? Se não, é suspeito."*

**2. Classe desbalanceada** — nunca cite acurácia. *"Com evento raro, acurácia engana: dizer sempre 'não' acerta 95% e é inútil. Uso precisão, recall e AUC-PR, e o corte sai do custo do falso positivo contra o da perda não detectada."*

**3. Query lenta** — *"não tenho experiência de tuning em produção. Pelo conceito: reduzir linha e coluna, filtrar antes de juntar, índice na coluna de join e filtro. Aprofundando, leria o plano de execução — aí já precisaria de ajuda."*

### Nunca diga

✗ Nome de ferramenta que não usou · ✗ métrica inventada · ✗ "usei machine learning" sem especificar · ✗ "deu 95% de acurácia" sem saber como foi medido · ✗ "usei Spark" (1,2M não justifica)

### Se travar

> "Isso eu não vou conseguir detalhar com precisão agora, e prefiro não chutar. O que eu sustento desse projeto é [a parte que você domina]."

**Isso não te derruba. Número inventado que desmorona, sim.**

---

## BLOCO 2 — Modelagem Financeira

> **Seu terreno mais forte, e a ponte direta com o André Shirassu** — que fez Matemática na USP, modelou risco de crédito no HSBC a partir de demonstrações financeiras, e fez pós em Finanças Corporativas na FIA.

### O que você fez, em uma frase

> "Na V4 eu era responsável pela análise mensal de DRE, pela modelagem financeira e pelas projeções de fluxo de caixa. O produto final era o relatório que a diretoria usava para decidir a alocação de um orçamento anual superior a R$ 5 milhões — e ao mesmo tempo eu operava a base: conciliação bancária e contas a pagar e receber, mais de 400 transações por mês."

**O detalhe que impressiona:** você fazia as duas pontas. Quem nunca tocou no dado bruto não sabe de onde desconfiar.

### "Como você estruturava a análise de DRE?"

> "Base comparável mês a mês, e o valor analítico não está no número absoluto — está no desvio e na causa do desvio. Eu **decompunha a variação de margem em volume, preço, mix e custo**, porque cada um pede uma ação diferente: volume é comercial, preço é pricing, mix é sortimento, custo é compra."

☝️ **Essa decomposição é a frase de maior retorno do bloco.** É o que liga finanças a Gestão de Categoria, o pilar nº 1 da ATY.

### "Como você projetava fluxo de caixa?"

> "Por driver, não por agregado: receita por origem, custo fixo e variável, calendário de recebível e pagável. E todo mês realizado contra projetado, com o desvio virando pergunta.
>
> Foi olhando o padrão do erro que eu achei o mais útil: o erro era enviesado num sentido, o que indica premissa errada e não ruído. Eu projetava recebimento pelo prazo contratual em vez do comportamento real de pagamento do cliente."

**Se perguntarem "que modelo estatístico?":** *"nenhum — era projeção por driver de negócio. Não rodei ARIMA nem Prophet ali. Sei a diferença e por que importa: minha projeção não dava intervalo de confiança nem separava sazonalidade de tendência, e eu validava contra o mês seguinte, não com backtest. É essa camada que eu quero construir."*

### Viés × variância — a distinção que vale ponto

```
Erro sempre no mesmo sentido  →  VIÉS      →  premissa errada (corrigível)
Erro alternando de sinal      →  VARIÂNCIA →  ruído (não corrigível por premissa)
```

### Valor presente — seu diferencial que quase ninguém usa

**Desconte sempre que houver fluxo plurianual.** A maioria dos candidatos calcula LTV sem desconto.

```
LTV = margem/compra × compras/ano × anos        ← errado se a vida é > 1 ano
LTV = Σ [ margem do ano / (1 + i)^ano ]         ← correto

Exemplo: margem R$ 240/ano, 2 anos, i = 10%
  Sem desconto : 480
  Com desconto : 240 + 240/1,10  =  R$ 458   (−4,6%)
```

### Custo efetivo — a conta que converte prazo em dinheiro

```
Custo Efetivo = Preço − [ Preço × (custo_capital_anual / 365) × dias de prazo ]

Com custo de capital de 20% a.a.:
  R$ 100 a 30 dias  →  100 − 1,64  =  R$ 98,36
  R$  97 a 10 dias  →   97 − 0,53  =  R$ 96,47   ← melhor
  R$ 103 a 90 dias  →  103 − 5,08  =  R$ 97,92   ← melhor que os R$ 100!
```

> "A proposta de R$ 103 tem etiqueta mais cara e é financeiramente melhor que a de R$ 100, porque 90 dias de prazo valem mais que os R$ 3. Sem converter para custo efetivo, o comprador escolhe errado achando que economizou."

### Certificações — como citar sem parecer catálogo

> "Minha base vem de Economia na UNICAMP, com Econometria, Estatística e Matemática Financeira, mais a parte formal de finanças: CPA-20, sou candidato ao CFA Nível I, e fiz valuation modeling e análise de demonstrações financeiras."

**A ponte com o André, se ele estiver na sala:**
> "Vi que você veio da Matemática na USP, passou por modelos de crédito no HSBC e fez a pós em Finanças Corporativas na FIA antes de migrar para analytics. Estou fazendo esse caminho pelo outro lado. Tenho curiosidade: o que a base de finanças te deu que um cientista de dados puro não tem?"

---

## BLOCO 3 — O Projeto da ATY

### Malha logística — as 4 frentes

Você não captou as quatro. **Pergunte** — prova que você pensou depois da conversa.

**Hipótese mais provável (por tema):**

```
1. DIAGNÓSTICO E CUSTO-SERVIR   fluxo origem-destino, custo por rota/loja
2. FOOTPRINT                    quantos CDs, onde, que capacidade
3. ESTOQUE E ALOCAÇÃO           o que estoca onde, nível de serviço
4. TRANSPORTE E ABASTECIMENTO   modal, frota, frequência, roteirização
```

**Alternativas:** por etapa (dados → modelagem → simulação → implementação) ou com uma frente de **sourcing/negociação** — o que explicaria a planilha.

### O conceito que você precisa ter na ponta: regra do √N

```
Estoque de segurança com N locais  ≈  centralizado × √N
  1 CD → 2 CDs  =  × 1,41  (+41%)
  1 CD → 4 CDs  =  × 2,00  (+100%)
```

> "É o mesmo princípio de diversificação de portfólio: a demanda de regiões diferentes não é perfeitamente correlacionada, então agregando os desvios se compensam parcialmente."

☝️ **Sua melhor conexão aqui** — vem de Derivativos e Gestão de Portfólio, que está no seu CV.

### Os 3 números do case de malha

| | |
|---|---|
| 2º CD numa rede de R$ 400 M | **−R$ 1,8 M/ano** (destrói valor) |
| Receita de equilíbrio do 2º CD | **~R$ 650 M** (~65ª loja) |
| **Transit point** (transbordo sem estoque) | **+R$ 0,93 M/ano** (vale hoje) |

> "A decisão não é 'se', é 'quando' — e o gatilho é volume transportado, não número de lojas. E transit point não aparece se a pergunta for tratada como binária entre um e dois CDs."

### Planilha de negociação — sua porta de entrada

**Eles anunciaram a necessidade e Excel é a sua ferramenta mais forte.** Construa o esqueleto antes da entrevista.

```
ABA 1  PARÂMETROS     custo de capital, taxas, câmbio — nenhum número em fórmula
ABA 2  BASE           fornecedor, SKU, volume, preço, prazo, curva ABC
ABA 3  SHOULD-COST    decomposição do custo do fornecedor por linha
ABA 4  CENÁRIOS       preço × prazo × desconto → CUSTO EFETIVO ÚNICO
ABA 5  PAINEL         1 página para a mesa: alvo, reserva, BATNA, moedas
ABA 6  TRACKER        negociado vs. realizado
```

**As 5 alavancas, da mais barata para a mais cara:**
```
1. Previsibilidade de pedido   custo ~zero, reduz o estoque do fornecedor
2. Consolidação de volume      custo zero, escala para os dois
3. Revisão de especificação    elimina custo que não gera valor
4. Prazo de pagamento          custo = seu custo de capital (mensurável)
5. Preço puro                  soma zero — a última
```

> "Preço é a única alavanca em que o ganho de um é exatamente a perda do outro. Eu deixaria para o fim."

### Split payment — o efeito duplo

**O que é:** com a Reforma Tributária (EC 132/2023, LC 214/2025, regulamentada pelo Decreto 12.955/2026), o IBS e a CBS são retidos **na liquidação financeira** da venda. O vendedor recebe o líquido.

**Cronograma:** CBS entra em 01/01/2027; o split **não** começa junto — expectativa de piloto voluntário a partir de meados de 2027, B2B primeiro, cartões depois. *Regra em evolução — não afirme data como fato.*

**O efeito que quase ninguém comenta:**

```
Rede de R$ 400 M/ano, carga ~27%, float atual ~25 dias, custo de capital 20%

1) PERDE O FLOAT TRIBUTÁRIO
   Capital de giro permanente adicional        R$ 7,5 M
   Custo anual                                 R$ 1,5 M/ano

2) E A BASE ANTECIPÁVEL ENCOLHE
   Recebível de cartão: 23,3 → 17,0 M          −27%
```

> "Split payment não aumenta a carga — antecipa o desembolso. E ele faz duas coisas ao mesmo tempo: aumenta a necessidade de capital de giro de forma permanente e reduz o instrumento usado hoje para cobri-la. A necessidade sobe e a cobertura desce — por isso não se resolve antecipando mais."

### A unificação — as três coisas são a mesma conta

```
┌──────────────────────────────┬─────────────────────────┬─────────────┐
│ Antecipar recebível          │ 1,5% a.m. → 19,6% a.a.  │ só se o uso │
│                              │                         │ render mais │
├──────────────────────────────┼─────────────────────────┼─────────────┤
│ Tomar desconto do fornecedor │ 2% em 20d → 37,2% a.a.  │ tomar se >  │
│                              │ (44,6% composta)        │ custo cap.  │
├──────────────────────────────┼─────────────────────────┼─────────────┤
│ Alongar prazo de pagamento   │ o que o fornecedor cobra│ alongar se  │
│                              │                         │ < custo cap.│
└──────────────────────────────┴─────────────────────────┴─────────────┘

Regra única: comparar a taxa implícita anualizada com o custo de capital.
```

**Dois números para a mesa de negociação:**
- Vale pagar até **~0,8%** de aumento de preço por +15 dias de prazo (a 20% a.a.)
- Desconto **abaixo de ~1,1%** não compensa antecipar o pagamento em 20 dias

### A alavanca que resolve

```
Alongar prazo de fornecedor de 30 → 45 dias (compras de R$ 260 M/ano)
  Capital liberado      R$ 10,8 M
  Valor anual a 20%     R$  2,17 M/ano    → cobre os R$ 1,5 M do split
```

### 4 perguntas para fazer

1. "Quais são as outras três frentes do projeto de malha? Eu só peguei a de supply chain."
2. "A planilha de negociação é para preço de produto, de frete, ou os dois?"
3. **"Eu converteria preço, prazo e desconto num custo efetivo único, para comparar R$ 100 a 30 dias com R$ 103 a 90 dias. Vocês tratam prazo como variável financeira na negociação, ou ele fica separado do preço?"**
4. "Quando você mencionou split payment junto de antecipação, me chamou atenção que os dois se agravam. Os clientes já estão vendo esse efeito duplo, ou a conversa ainda está mais no lado fiscal e de ERP?"

---

## BLOCO 4 — O Que Esperam de um Júnior

> A pergunta silenciosa por trás de tudo, numa boutique de 3 a 8 pessoas:
> **"Essa pessoa vai me dar mais trabalho ou menos?"**

### O que você vai fazer de fato

| Demanda | Peso | Como demonstrar que você dá conta |
|---|---|---|
| **Extrair e tratar dado** (SQL/Python) | Alto | O projeto de 1,2M registros; o ritual de inspeção de base |
| **Construir entregável operável** (Excel, Power BI, slide) | Alto | A planilha de negociação; o relatório da diretoria na V4 |
| **Reconciliar e conferir número** | Alto | *"fechava contra a contabilidade; se não fecha, nada mais importa"* |
| **Análise exploratória e primeiras hipóteses** | Médio | Decomposição de margem; categorização de despesa |
| **Documentar e organizar** | Médio | Rastreabilidade até o comprovante; padrão de arquivo |
| **Pesquisa e benchmark de mercado** | Médio | Market sizing; prospecção na Nunes&Lucato |
| **Apoio em reunião de cliente** | Baixo-médio | Anotar, consolidar follow-up, preparar material |

### O que NÃO esperam — e assumir isso te valoriza

✗ Decidir metodologia sozinho · ✗ desenhar arquitetura de dados · ✗ conduzir reunião com C-level sem sócio · ✗ colocar modelo em produção · ✗ dominar Databricks e dbt já

> "Imagino que a expectativa para um júnior aqui seja aprender o stack rodando, com alguém corrigindo. É exatamente o que eu quero."

### As 4 competências que realmente avaliam

**1. Autonomia** — tentar resolver antes de perguntar, e perguntar bem quando trava
> *"Travei nisso, tentei X e Y, e minha hipótese é Z. Como você faria?"* ← pergunta de quem pensou

**2. Rigor** — não entregar número que não fecha, e qualificar o que é frágil
> **A frase mais forte que você tem:** *"a inadimplência caiu, mas eu não tinha grupo de controle. Então defendo a redução do prazo de cobrança, que é o efeito de primeira ordem; o efeito total eu trato como hipótese, não como conclusão."*

**3. Velocidade de aprendizado** — curva curta em ferramenta nova
> *"Sempre com um problema concreto no meio. E meu teste de que entendi é conseguir explicar — se eu não consigo ensinar, eu não entendi, só reconheci."*

**4. Comunicação** — recomendação antes do método
> *"Ninguém decide com AUC. 'O modelo acerta 7 de cada 10 na lista prioritária, então quem investiga 100 casos por mês vai achar 70 em vez de 20' — isso decide."*

### Calibragem honesta das ferramentas

| | Declare |
|---|---|
| Excel / VBA | **avançado** ✓ (tem certificação e uso real) |
| SQL · Python | **intermediário** |
| Power BI | **básico-intermediário** |
| Databricks · dbt | **não conheço — estudei o conceito** |

**Rebaixar o rótulo custa zero e te protege de tudo.**

### O posicionamento, em uma frase

> "Não sou o modelador mais forte que vocês vão entrevistar. Sou quem já sentou na cadeira de quem decide com o número — DRE, margem, risco de crédito, fluxo de caixa — e tenho Python e SQL para sujar a mão no dado desde o primeiro dia. A modelagem eu aprendo com vocês; a parte de negócio eu já trago."

---

## COLINHA FINAL

### Números deles
**+7 p.p.** lucro em pricing de moda (e +20 p.p. vs. time comercial) · **2,3% WMAPE** em forecasting com redes neurais · **~R$ 9,8 M** em fraude na saúde · fundada **fev/2025** · **ATY = "fazer juntos"**

### Números seus
**R$ 5 M+** de orçamento decidido com seus relatórios · **1,2 M+** registros em Python/SQL · **400+** transações/mês · **80+ alunos × 3 edições** · **R$ 150 mil / 2.500 itens** (Midea, Carrier, Santista)

### Os 4 pilares — nas palavras deles
**Gestão de Categoria** · **Supply Chain** · **Marketing & Customer Insights** · **Estratégia de Dados & IA**

### Os 3 valores
**Mão na Massa** · **Rigor Analítico** · **Solução Duradoura**

### Os 4 clientes
**Aramis** (moda masculina premium) · **Kraft Heinz** (CPG) · **Maravilhas do Lar** (utilidades) · **Vero**

### Contas de cabeça
```
Taxa efetiva anual         (1 + i_mês)¹² − 1
Desconto de fornecedor     [d/(1−d)] × (365/dias)
Valor de +N dias de prazo  valor × (custo_cap/365) × N
Estoque de segurança       centralizado × √N
Margem após mudança        Q₁ × (P₁ − C)  vs.  Q₀ × (P₀ − C)
Variação conjunta          (1 + %ΔP) × (1 + %ΔQ) − 1
```

### Notícia para citar
Pesquisa da **Kyndryl**: cerca de **76% das empresas brasileiras** temem que a IA avance além da sua capacidade operacional, governança e preparo de equipe.
> "Isso me pareceu exatamente a tese da oferta de Estratégia de Dados e IA de vocês — e explica por que governança aparece antes de agente na descrição."

### Erros que eliminam
✗ Inflar resultado · ✗ blefar em ferramenta · ✗ afirmar causalidade sem contrafactual · ✗ não ter lido o site · ✗ falar de IA como solução universal · ✗ se vender como gênio solitário · ✗ não ter perguntas

---

*Material de apoio. O relatório completo (162 páginas) está em `preparacao-aty/` e no `Relatorio-ATY-Consulting.pdf`.*
