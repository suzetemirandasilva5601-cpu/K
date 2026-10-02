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

> "A base não cabia no Excel: 1,2 milhão de linhas passa do limite de pouco mais de um milhão da planilha. Foi por isso que o trabalho foi para SQL e Python. Filtrei e agreguei no banco e trouxe para o Python já no grão da análise. E 1,2 milhão cabe em pandas, não precisava de Spark, e eu prefiro não inventar complexidade que o problema não pede."

**Por que funciona:** é verificável, explica a escolha de ferramenta por restrição real, e mostra dimensionamento correto nas duas direções.

### O projeto, em 20 segundos

> "Previsão de falta em consulta agendada, 1,2 milhão de registros. Extração e histórico do paciente em SQL com window function, regressão logística no Python por interpretabilidade, validação com split temporal e comparação contra a regra de negócio que já existia. O resultado prático foi dobrar a eficiência da fila de confirmação: a equipe passa a encontrar 45% de faltantes em vez de 21% na mesma capacidade de ligação."

**O projeto completo, rodável, está em `projeto-python/`.** Rode, entenda cada linha, e você fala dele com honestidade.

### Respostas para os ataques mais prováveis

**"Me conta esse projeto."**
> "O problema era no-show, falta em consulta agendada. Cada falta é um horário de médico que fica vazio e não dá pra revender, então o custo é direto. A pergunta de negócio era concreta: a equipe consegue ligar pra confirmar presença de uma parte das consultas, não de todas, então pra quem ela deve ligar.
>
> A base tinha 1,2 milhão de consultas. Fiz a extração em SQL com join da tabela de consultas com a de pacientes, apliquei o filtro de qualidade no banco e calculei o histórico de falta do paciente com window function. No Python usei regressão logística, validei com split temporal e comparei contra a regra que já existia, que era olhar quem tinha espera maior que 30 dias.
>
> Deu AUC de 0,68 contra 0,59 da regra. Mas o número que importava pro cliente era outro: priorizando os 10% mais prováveis, a equipe encontra 45% de faltantes em vez de 21% ligando ao acaso."

**"Por que regressão logística e não um modelo mais forte?"**
> "Por interpretabilidade, e foi escolha consciente. O cliente não ia operar um score que ele não entende. Com a logística eu consigo dizer que o histórico de falta do paciente e os dias de espera são os dois fatores mais fortes, e aí a conversa deixa de ser sobre o modelo e passa a ser sobre o processo: se espera longa aumenta falta, talvez a resposta não seja só ligar, seja encurtar a fila.
>
> Testei uma árvore como comparação e o ganho não pagava a perda de leitura. Num projeto de consultoria eu prefiro o modelo que o cliente mantém depois que eu saio."

**"Como você validou?"**
> "Split temporal, treinando nos primeiros 70% do período e testando no restante. Fiz assim porque existe ordem no dado e é assim que o modelo seria usado na prática, prevendo o próximo mês com o que já passou.
>
> Se eu tivesse feito split aleatório, consulta futura entraria no treino e a performance medida seria otimista. É um erro que aparece bonito no notebook e quebra em produção."

**"E vazamento de dados, você checou?"**
> "Sim, e o ponto crítico estava justamente na feature mais forte. O histórico de falta do paciente é calculado com window function, e o frame termina em 1 PRECEDING, ou seja, exclui a própria consulta que eu estou prevendo. Se eu tivesse incluído a linha atual, o modelo estaria olhando o resultado pra prever o resultado.
>
> A checagem que eu faço em geral é perguntar, pra cada variável, se no momento real da predição aquele campo já está preenchido. Se a resposta for não ou depende, é suspeito."

**"Como tratou 1,2 milhão de registros?"**
> "Essa parte foi mais simples do que parece. 1,2 milhão de linhas cabe em pandas numa máquina comum, então não precisei de nada distribuído. Deixei filtro e agregação no SQL, porque o banco faz isso melhor, e trouxe pro Python só o que eu ia modelar.
>
> O detalhe que importa é que não cabia no Excel. O limite da planilha é pouco mais de um milhão de linhas, então a base passava. Foi por isso que o trabalho foi pra SQL e Python, não por preferência de ferramenta. E eu prefiro não inventar complexidade que o problema não pede: falar que usei Spark pra 1,2 milhão de linhas seria exagero."

**"Qual era o baseline?"**
> "A regra que a operação já usava, priorizar quem tinha espera maior que 30 dias. Ela dá AUC de 0,59, então funciona um pouco, não é aleatória.
>
> Essa comparação importa mais que a métrica absoluta, porque mede valor incremental. Um modelo com AUC alto que não bate a regra existente não deveria ir pra produção, e isso acontece mais do que se imagina."

**"Por que não acurácia?"**
> "Porque ela engana com classe desbalanceada. Nesse caso 79% das consultas têm presença, então um modelo que chuta sempre presença acerta 79% e não identifica ninguém. Boa acurácia e zero utilidade.
>
> Usei AUC pra avaliar a ordenação e depois olhei precisão no topo da lista, que é o que realmente importa. A equipe tem capacidade limitada de ligação, então o que interessa é a precisão nos 10% que ela vai trabalhar, não a performance média."

**"O que deu errado?"**
> "Duas coisas. A primeira foi que criei várias features de especialidade médica e nenhuma teve efeito, os coeficientes ficaram praticamente em zero. Aprendi que criar variável sem hipótese de negócio atrás só gera ruído.
>
> A segunda foi mais útil: a minha primeira versão calculava o histórico do paciente sem excluir a consulta atual. A performance veio muito alta e eu desconfiei exatamente por isso, porque estava bom demais. Era vazamento. Corrigir foi mudar o frame da window function, mas eu só achei porque estranhei o resultado bom."

**"Se refizesse hoje, o que mudaria?"**
> "Três coisas. Usaria cross-validation em vez de um corte temporal só, porque um corte pode ser sorte de um período específico.
>
> Testaria um gradient boosting pra saber o tamanho do ganho que eu abri mão ao escolher interpretabilidade. Decidi por logística, mas não medi direito o custo dessa decisão.
>
> E a mais importante: ligaria o modelo a um teste de verdade. Hoje eu sei que ele ordena bem, mas não sei se ligar pro paciente reduz a falta. São duas perguntas diferentes, e a segunda é a que o cliente quer. Pra responder, eu precisaria sortear parte da lista priorizada pra não receber ligação e comparar."

**"Query lenta, o que você faz?"**
> "Não tenho experiência de tuning em produção, então vou pelo conceito. Primeiro olho volume: estou trazendo mais linha ou mais coluna do que preciso. Depois, onde está o filtro, porque filtrar antes de juntar é melhor que juntar tudo e filtrar. Depois, se há índice na coluna de join e de filtro. Aprofundando, eu leria o plano de execução, mas aí já é território em que eu ia precisar de ajuda."

### Nunca diga

✗ Nome de ferramenta que não usou · ✗ métrica inventada · ✗ "usei machine learning" sem especificar · ✗ "deu 95% de acurácia" sem saber como foi medido · ✗ "usei Spark" (1,2M não justifica)

### Se travar

> "Isso eu não vou conseguir detalhar com precisão agora, e prefiro não chutar. O que eu sustento desse projeto é [a parte que você domina]."

**Isso não te derruba. Número inventado que desmorona, sim.**

---

## BLOCO 2 — Modelagem Financeira

> **Seu terreno mais forte, e a ponte direta com o André Shirassu** — que fez Matemática na USP, modelou risco de crédito no HSBC a partir de demonstrações financeiras, e fez pós em Finanças Corporativas na FIA.

### O que você fez, em uma frase

> "Na V4 eu era responsável pela análise mensal de DRE, pela modelagem financeira e pelas projeções de fluxo de caixa. O produto final era o relatório que a diretoria usava para decidir a alocação de um orçamento anual superior a R$ 5 milhões, e ao mesmo tempo eu operava a base: conciliação bancária e contas a pagar e receber, mais de 400 transações por mês."

**O detalhe que impressiona:** você fazia as duas pontas. Quem nunca tocou no dado bruto não sabe de onde desconfiar.

### "Como você estruturava a análise de DRE?"

> "Base comparável mês a mês, e o valor analítico não está no número absoluto, está no desvio e na causa do desvio. Eu **decompunha a variação de margem em volume, preço, mix e custo**, porque cada um pede uma ação diferente: volume é comercial, preço é pricing, mix é sortimento, custo é compra."

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

### A equipe, e quem provavelmente te entrevista

**Nicole Gradice Silva** · Senior Data Scientist desde set/2025 · Física Computacional (USP)
Entre as competências declaradas dela está **"otimização de rotas e malhas logísticas"**. É quase certo que **ela seja a responsável técnica pelo projeto de malha**, e provável que seja sua gestora direta.

O ponto mais importante: ela entrou na ADVISIA como **Data Scientist Jr vindo de Analista de Planejamento na Carglass**, um cargo de operação. Subiu quatro níveis em quatro anos. **Ela fez exatamente a transição que você quer fazer.** Tem o McKinsey Forward (structured problem solving, que você ensina) e faz elasticidade de preço.

> "Vi que você entrou na ADVISIA como Data Scientist Jr vindo de um cargo de planejamento na Carglass. Estou numa transição parecida, saindo de um papel financeiro pra analytics. Como foi essa passagem, e o que foi mais difícil de aprender que a graduação não tinha dado?"

> "Vi otimização de rotas e malhas entre as suas competências. No projeto de malha, o gargalo tem sido mais o modelo de otimização ou a qualidade do dado de origem e destino?"

A segunda pergunta é forte porque **a resposta quase sempre é "o dado"**, e aí você oferece exatamente onde um júnior ajuda.

**Gilberto Volpe** · Sócio · reduziu ruptura de 10% para 5% na Ultrapar e implantou Oracle Retail Demand Forecast. Já viveu malha e estoque **do lado do cliente**.

**André Shirassu** · Partner · risco de crédito no HSBC e Elo, pós em Finanças Corporativas na FIA. **Split payment, antecipação e custo de capital são a língua dele.**

**Divisão provável do projeto:** Gilberto no enquadramento e cliente · André no rigor e no impacto financeiro · Nicole na otimização de rede · **vaga júnior na extração, no baseline de custo-servir, na planilha e na documentação**. A última linha é a descrição da vaga.

### Malha logística — as 4 frentes

Você não captou as quatro. **Pergunte** — prova que você pensou depois da conversa.

**Hipótese mais provável (por tema):**

| # | Frente | O que entrega | Seu encaixe |
|---|---|---|---|
| **1** | **Diagnóstico e custo-servir** | Baseline: quanto custa servir cada loja e rota | **Alto.** 80% é extração, tratamento e reconciliação |
| **2** | **Footprint** | Quantos CDs, onde, e em que volume a resposta muda | **Médio.** Matriz origem-destino, cenários |
| **3** | **Estoque e alocação** | O que fica onde, com que nível de serviço | **Médio-alto.** ABC/XYZ, desvio da demanda, capital |
| **4** | **Transporte e abastecimento** | Modal, frequência, rota, consolidação | **Médio.** Tabela de frete, custo por rota, planilha |

**Alternativas:** por etapa (dados → modelagem → simulação → implementação), ou com uma frente própria de **sourcing e negociação**, que explicaria diretamente a planilha.

**Por onde você começaria, se perguntarem:**
> "Pela frente 1, e não por gosto, por dependência. Sem custo-servir consolidado, a otimização de footprint roda em cima de premissa e entrega número bonito e errado. E costuma ser a frente que mais consome tempo, porque o dado está espalhado: frete no financeiro, volume no sistema de armazém, cadastro de peso e cubagem incompleto. É pouco glamouroso e é o caminho crítico."

**Dois números a mais para a frente 3:**
```
Estoque de segurança = z × desvio da demanda × raiz(lead time)
Nível de serviço 95% → 99%  =  z de 1,65 → 2,33  =  +41% de estoque
```
> "Por isso nível de serviço é decisão econômica e não meta institucional. Em SKU de margem e giro altos compensa 99%; em cauda longa, não."

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

> "A decisão não é 'se', é 'quando', e o gatilho é volume transportado, não número de lojas. E transit point não aparece se a pergunta for tratada como binária entre um e dois CDs."

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

> "Split payment não aumenta a carga, antecipa o desembolso. E ele faz duas coisas ao mesmo tempo: aumenta a necessidade de capital de giro de forma permanente e reduz o instrumento usado hoje para cobri-la. A necessidade sobe e a cobertura desce, por isso não se resolve antecipando mais."

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
> *"Sempre com um problema concreto no meio. E meu teste de que entendi é conseguir explicar. Se eu não consigo ensinar, eu não entendi, só reconheci."*

**4. Comunicação** — recomendação antes do método
> *"Ninguém decide com AUC. 'O modelo acerta 7 de cada 10 na lista prioritária, então quem investiga 100 casos por mês vai achar 70 em vez de 20'. Isso decide."*

### Calibragem honesta das ferramentas

| | Declare |
|---|---|
| Excel / VBA | **avançado** ✓ (tem certificação e uso real) |
| SQL · Python | **intermediário** |
| Power BI | **básico-intermediário** |
| Databricks · dbt | **não conheço — estudei o conceito** |

**Rebaixar o rótulo custa zero e te protege de tudo.**

### O posicionamento, em uma frase

> "Não sou o modelador mais forte que vocês vão entrevistar. Sou quem já sentou na cadeira de quem decide com o número: DRE, margem, risco de crédito, fluxo de caixa. E tenho Python e SQL para sujar a mão no dado desde o primeiro dia. A modelagem eu aprendo com vocês; a parte de negócio eu já trago."

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
> "Isso me pareceu exatamente a tese da oferta de Estratégia de Dados e IA de vocês, e explica por que governança aparece antes de agente na descrição."

### Erros que eliminam
✗ Inflar resultado · ✗ blefar em ferramenta · ✗ afirmar causalidade sem contrafactual · ✗ não ter lido o site · ✗ falar de IA como solução universal · ✗ se vender como gênio solitário · ✗ não ter perguntas

---

*Material de apoio. O relatório completo (162 páginas) está em `preparacao-aty/` e no `Relatorio-ATY-Consulting.pdf`.*
