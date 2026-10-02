# Parte 13 — As 4 Frentes do Projeto de Malha e Quem Faz o Quê na ATY

> **Base:** o que o sócio te contou (projeto de malha logística com 4 frentes, planilha de negociação em Excel, split payment) + perfis públicos da equipe. Frentes marcadas como `[HIPÓTESE]` são minha reconstrução a partir de como projetos de rede logística são estruturados. **Pergunte na entrevista em vez de afirmar.**

---

## 13.1 A equipe, e por que isso importa para o projeto

### Nicole Gradice Silva — Senior Data Scientist
**ATY desde set/2025 · remoto · Física Computacional (USP, 2015–2019)**

**O detalhe que muda tudo:** entre as competências declaradas dela no LinkedIn está, literalmente, **"otimização de rotas e malhas logísticas"**.

> **Conclusão com base forte:** a Nicole é, com altíssima probabilidade, **a responsável técnica pelo projeto de malha**. É a única pessoa da casa com otimização de rede declarada como especialidade, e o projeto está rodando agora.

**Trajetória completa:**

| Período | Posição | Relevância para o projeto |
|---|---|---|
| set/2025 – hoje | **Senior Data Scientist, ATY** | Capacidade de entrega técnica da casa |
| jul/2024 – mai/2025 | Associate, ADVISIA | Nível de senioridade e gestão |
| jul/2023 – jun/2024 | Senior Data Scientist, ADVISIA | |
| jul/2022 – jun/2023 | Data Scientist Pleno, ADVISIA | |
| jul/2021 – jun/2022 | **Data Scientist Jr, ADVISIA** | **Entrou júnior e subiu 4 níveis em 4 anos** |
| fev/2020 – jul/2021 | **Analista de Planejamento, Carglass** | Planejamento de operação de campo, não cargo de dados |
| out/2018 – jan/2020 | Analista de mineração de dados, IFSC/USP | Projeto CUCo, enquanto se formava |

**Competências declaradas:** testes A/B para avaliação de impacto comercial · previsão de vendas, sazonalidade e projeções de faturamento · análise de churn e segmentação · **cálculo de elasticidade de preço** · pipelines analíticos e automações em Python · **otimização de rotas e malhas logísticas**

**Stack:** Python (principal), SQL, R
**Certificações:** **McKinsey Forward Program** (jul/2025) · Machine Learning, Stanford (nov/2021)
**Setores:** varejo, combustíveis, mobilidade

### Por que ela é a pessoa mais importante da sua entrevista

**1. A trajetória dela é exatamente a sua rota.** Física Computacional, não ciência de dados. Depois **Analista de Planejamento na Carglass**, um cargo de operação e negócio. Só então entrou como Data Scientist Jr. Ela fez a conversão que você quer fazer, e por isso reconhece o seu perfil em vez de descartá-lo.

**2. Ela provavelmente será sua gestora direta.** Numa boutique de 3 a 8 pessoas, a sênior de entrega é quem distribui e revisa trabalho júnior. A pergunta silenciosa dela não é "essa pessoa é brilhante?", é **"essa pessoa vai me dar mais trabalho ou menos?"**.

**3. Vocês têm vocabulário comum imediato.** O McKinsey Forward é um programa de structured problem solving, comunicação e adaptabilidade. **Você ensina isso no Prep4Consulting.** É afinidade metodológica real, não forçada.

**4. Ela faz elasticidade de preço.** Que é microeconomia, a sua base.

**Fala para guardar, se ela estiver na sala:**

> "Vi que você entrou na ADVISIA como Data Scientist Jr vindo de um cargo de planejamento na Carglass, com formação em Física Computacional. Estou numa transição parecida, saindo de um papel financeiro pra analytics. Como foi essa passagem pra você, e o que foi mais difícil de aprender que a graduação não tinha dado?"

E, sobre o projeto:

> "Vi otimização de rotas e malhas logísticas entre as suas competências. No projeto de malha, o gargalo tem sido mais o modelo de otimização em si ou a qualidade do dado de origem e destino?"

☝️ Essa segunda pergunta é excelente porque **a resposta quase sempre é "o dado"**, e aí você pode oferecer exatamente onde um júnior ajuda.

### Gilberto Volpe — Sócio
Única bio no site, `gvolpe@atyconsulting.com`. Mestrado USP, MBA FGV, 4 anos na **Ultrapar** (Ipiranga e Oxiteno) onde **reduziu ruptura de estoque de 10% para 5%** e implantou Oracle Retail Demand Forecast. Competências top: Estratégia de TI e **MLOps**.

> **A ligação com o projeto:** ele já viveu malha e estoque **do lado do cliente**, numa distribuidora de combustíveis. Quando ele fala de rede logística, fala de operação que ele mesmo operou.

### André Shirassu — Partner
Matemática USP, pós em Finanças Corporativas e IB na FIA, risco de crédito no HSBC e no Cartão Elo. Stack: Python, SQL, **dbt, Databricks**, Power BI. Dynamic pricing, forecasting com redes neurais (**2,3% WMAPE**), fraude (**~R$ 9,8M**).

> **A ligação com o projeto:** split payment, antecipação de recebível e custo de capital são a língua dele. Se a conversa sobre caixa surgiu, provavelmente veio dele ou passa por ele.

### Gustavo Horta
**Não encontrei informação pública confiável** (sem LinkedIn localizável, sem menção no site da ATY, sem registro em fontes de mercado). **Não incluí para não te fazer afirmar algo incorreto numa entrevista.** Se você tiver o perfil dele, me passe e eu complemento.

### Quem provavelmente faz o quê no projeto `[HIPÓTESE]`

```
GILBERTO    relação com cliente, enquadramento estratégico,
            decisão de footprint, governança e sustentação

ANDRÉ       modelagem, rigor estatístico, impacto financeiro
            (capital de giro, custo de capital, split payment)

NICOLE      responsável técnica da otimização de rede e rotas,
            previsão de demanda, pipelines em Python

VAGA JR     extração e tratamento de dado, construção do baseline de
            custo-servir, planilha de negociação, documentação
```

**Olhe a última linha.** É a descrição da vaga, e é exatamente onde você encaixa.

---

## 13.2 As 4 frentes, expandidas

> Para cada frente: objetivo, perguntas que ela responde, dado necessário, técnica, entregável, **onde um júnior agrega**, e a armadilha típica.

---

### FRENTE 1 — Diagnóstico e Custo-Servir

**Objetivo.** Construir o baseline. Quanto custa, hoje, servir cada loja, cada rota e cada categoria de produto. Sem isso não existe otimização, só opinião.

**Perguntas que responde**
- Qual o custo logístico total e como se divide entre inbound, armazenagem, outbound e capital de estoque?
- Quanto custa servir cada loja? Existe loja que destrói valor na operação atual?
- Onde está a concentração: 20% das rotas respondem por quanto do custo?
- Qual o custo por unidade movimentada, por peso e por cubagem?

**Dado necessário**
Volume origem-destino por período · peso e cubagem por SKU · frete pago por rota e por transportadora · custo fixo e variável do CD · nível de estoque por local · lead time por fornecedor · janela de entrega por loja

**Técnica.** Quase nada de modelagem. É **engenharia analítica e rateio**: consolidar fontes, definir critério de alocação de custo indireto, construir visão por dimensão (loja, rota, categoria).

**Entregável.** Baseline de custo-servir, curva de concentração, mapa de fluxo.

> **Onde um júnior agrega, e é aqui que você entra.** Esta frente é **80% extração, tratamento e reconciliação de dado**. É trabalho pesado, é pré-requisito de todas as outras frentes, e é exatamente o que se delega. Você tem SQL, Python e, principalmente, **experiência de reconciliar número contra fonte independente**, que é a parte que mais trava.

**Fala para a entrevista:**
> "Imagino que a frente de diagnóstico seja onde mais trava, porque custo logístico raramente está consolidado num lugar só. Normalmente frete está no financeiro, volume está no WMS e cadastro de peso e cubagem está incompleto. Eu acho que é aí que um júnior ajuda mais rápido, e é o tipo de trabalho que eu já fiz: na V4 eu reconciliava o número contra a contabilidade, e quando não fechava eu tinha que achar onde estava a diferença."

**A armadilha.** Critério de rateio de custo indireto define o resultado. Ratear armazenagem por volume ou por valor dá respostas diferentes sobre qual categoria é caro servir. **A escolha do critério é decisão analítica, não contábil**, e precisa ser explicitada.

---

### FRENTE 2 — Footprint: quantos CDs, onde, com que capacidade

**Objetivo.** Definir a configuração física da rede. Número de instalações, localização, capacidade e qual região cada uma atende.

**Perguntas que responde**
- Um CD ou dois? Onde?
- Em que volume a configuração atual deixa de ser a melhor?
- Quais lojas cada instalação atende, ao menor custo total?
- Quanta capacidade precisa, considerando o plano de expansão?

**Dado necessário**
Coordenadas de lojas e fornecedores · demanda projetada por loja · matriz de custo de frete por distância e modal · custo de instalação e operação por candidato a local · restrição de capacidade

**Técnica.** Otimização. Formulação clássica é **problema de localização de instalações** (facility location), resolvido como programação inteira mista: minimizar custo total sujeito a atender toda a demanda e respeitar capacidade. Em seguida, **análise de cenários**: rodar a otimização para vários níveis de volume e ver quando a resposta muda.

**O conceito central, e você precisa dominá-lo: a regra do √N**

```
Estoque de segurança com N locais  ≈  centralizado × √N

  1 CD → 2 CDs  =  × 1,41   (+41%)
  1 CD → 4 CDs  =  × 2,00  (+100%)
```

> "É diversificação de portfólio aplicada a estoque. A demanda de regiões diferentes não é perfeitamente correlacionada, então, agregando, os desvios se compensam parcialmente. Quando eu separo em dois locais, perco parte desse efeito."

☝️ **Sua melhor conexão conceitual do projeto inteiro**, e vem de Derivativos e Gestão de Portfólio, que está no seu CV.

**A conta que mostra o trade-off** (rede de R$ 400 M, estoque de segurança de R$ 20 M, custo de capital 20%):

```
Custo adicional do 2º CD
  Estoque de segurança   20 × √2 = 28,3    →  +8,3 M de capital
  Custo do capital       8,3 × 20%         =  R$ 1,66 M/ano
  Fixo do novo CD                          =  R$ 3,00 M/ano
                                              ─────────────
                                              R$ 4,66 M/ano

Ganho em outbound (redução de 30% na distância, sobre 9,6 M)
                                           =  R$ 2,88 M/ano

RESULTADO                                  =  −R$ 1,78 M/ano
```

**Ponto de virada:** receita de aproximadamente **R$ 650 M**, perto da 65ª loja.

**A opção que quase sempre é esquecida: transit point**
```
Transbordo SEM estoque: a regra do √N não se aplica
  Ganho (18% de redução de last mile)      =  R$ 1,73 M/ano
  Custo fixo                                =  R$ 0,80 M/ano
  LÍQUIDO                                   =  +R$ 0,93 M/ano
```

> **Onde um júnior agrega.** Montar a matriz origem-destino, calcular distância entre coordenadas, preparar os cenários e consolidar os resultados comparáveis. A formulação do modelo é da Nicole; a preparação do insumo e a análise de sensibilidade são delegáveis.

**A armadilha.** Otimizar com custo de frete médio em vez de tabela real por faixa de distância e por modal. O modelo fica elegante e a resposta, errada.

---

### FRENTE 3 — Política de Estoque e Alocação

**Objetivo.** Decidir o que fica onde, em que quantidade, e com que nível de serviço. É onde o capital de giro é definido.

**Perguntas que responde**
- Quanto de estoque de segurança por SKU e por local?
- Que nível de serviço por classe de produto? 95% para todos é desperdício
- O que centraliza e o que descentraliza?
- Qual o ponto de pedido e o lote de reposição?

**Dado necessário**
Histórico de demanda por SKU e por loja (para estimar média e **variabilidade**) · lead time e sua variabilidade · custo de capital · margem por SKU · custo de ruptura · classificação ABC/XYZ

**Técnica.** Previsão de demanda mais política de estoque. A fórmula central:

```
Estoque de segurança  =  z × σ_demanda × √(lead time)

  z        = fator da normal para o nível de serviço desejado
             (95% → z ≈ 1,65    99% → z ≈ 2,33)
  σ         = desvio-padrão da demanda no período
  lead time = prazo de reposição
```

**A implicação econômica que vale citar:** ir de 95% para 99% de nível de serviço **não** custa 4% mais estoque. O fator z sai de 1,65 para 2,33, ou seja, **+41% de estoque de segurança** para ganhar 4 pontos de disponibilidade. A cauda da normal é não-linear.

> "Por isso nível de serviço é decisão econômica e não meta institucional. A pergunta certa não é qual nível queremos, é quanto custa cada ponto adicional e quanto vale evitar aquela ruptura. Em SKU de margem alta e giro alto compensa 99%; em cauda longa, não."

**Centralizar ou descentralizar, por classe:**

```
Giro alto + demanda estável     →  descentralizar (perto da loja)
Giro baixo + demanda errática   →  centralizar (aproveita o efeito √N)
Margem alta                     →  nível de serviço maior
Cauda longa                     →  centralizar, ou nem estocar
```

> **Onde um júnior agrega.** Classificação ABC/XYZ, cálculo de σ da demanda por SKU, simulação de níveis de serviço e tradução disso em capital imobilizado. **É cálculo estruturado em Python ou Excel**, direto na sua praia.

**A armadilha.** Calcular σ sem tratar promoção e ruptura. Promoção infla a variabilidade e faz o modelo pedir estoque demais; **ruptura não registrada aparece como venda zero**, o modelo aprende que não há demanda e pede estoque de menos. Censura de dado, exatamente nos itens que mais faltam.

---

### FRENTE 4 — Transporte e Abastecimento

**Objetivo.** Definir como o produto se move. Modal, frota, frequência, roteirização, consolidação.

**Perguntas que responde**
- Frota própria, dedicada ou mercado spot?
- Com que frequência repor cada loja?
- Qual a melhor rota e sequência de entrega?
- Vale consolidar carga? Faz sentido milk run?
- Entrega direta do fornecedor para a loja em algum caso?

**Dado necessário**
Tabela de frete por faixa e modal · capacidade do veículo em peso e cubagem · janela de recebimento por loja · tempo de deslocamento e de descarga · volume por entrega

**Técnica.** Roteirização (variações do problema do caixeiro viajante com capacidade e janela de tempo) e otimização de frequência.

**O trade-off central:**

```
Repor com mais frequência  →  estoque MENOR na loja, frete MAIOR
Repor com menos frequência →  estoque MAIOR na loja, frete MENOR

Ponto ótimo: onde o custo marginal de frete iguala
             o custo marginal de capital de estoque
```

> **A conexão com a planilha de negociação.** Esta frente é onde **frete é negociado**, e frete é item de custo com fornecedor (transportadora). Se uma das 4 frentes envolve sourcing, provavelmente é aqui, ou numa frente própria de negociação.

> **Onde um júnior agrega.** Consolidar tabela de frete, calcular custo por entrega e por rota, simular cenários de frequência, e **construir a planilha de negociação com as transportadoras**.

**A armadilha.** Otimizar frete isoladamente. Aumentar lote reduz frete por unidade e aumenta estoque e obsolescência. **Só o custo total importa.**

---

## 13.3 Como as frentes se encadeiam

```
FRENTE 1  Diagnóstico e custo-servir
             │  (sem baseline, nada depois faz sentido)
             ▼
FRENTE 2  Footprint: quantos CDs e onde
             │  (a configuração define o que vem depois)
             ▼
FRENTE 3  Política de estoque e alocação
             │  (o que fica em cada local definido na frente 2)
             ▼
FRENTE 4  Transporte e abastecimento
             │  (como conectar o que foi decidido)
             ▼
         Negociação com fornecedor e transportadora
         (a planilha que ele mencionou)
```

**O que dizer se perguntarem por onde você começaria:**

> "Pela frente 1, e não por gosto, por dependência. Sem custo-servir consolidado, a otimização de footprint roda em cima de premissa e entrega número bonito e errado. E na minha experiência é a frente que mais consome tempo, porque o dado está espalhado: frete no financeiro, volume no sistema de armazém, cadastro de peso e cubagem incompleto. É pouco glamouroso e é o caminho crítico."

---

## 13.4 Alternativas de desenho das 4 frentes `[HIPÓTESE]`

Como você não captou as quatro, tenha as três leituras possíveis:

**Por tema (a que eu detalhei acima):** diagnóstico · footprint · estoque · transporte

**Por etapa de projeto:** dados e diagnóstico · modelagem e otimização · simulação de cenários · implementação e governança

**Mista, com sourcing:** diagnóstico · desenho de rede · política de estoque · **negociação e sourcing** ← esta explicaria diretamente a planilha de negociação em Excel

**A pergunta a fazer:**
> "Você mencionou que o projeto de malha tem quatro frentes e eu só peguei a de supply chain. Quais são as outras três? Fiquei curioso se a planilha de negociação que você citou está dentro de uma frente de sourcing, porque frete e condição de entrega acabam sendo item negociado."

---

## 13.5 Resumo para a véspera

| Frente | Em uma linha | Seu encaixe |
|---|---|---|
| **1. Diagnóstico e custo-servir** | Construir o baseline de quanto custa servir cada ponto | **Alto.** Extração, tratamento, reconciliação |
| **2. Footprint** | Quantos CDs, onde, e quando a resposta muda | **Médio.** Matriz O-D, cenários, sensibilidade |
| **3. Estoque e alocação** | O que fica onde, com que nível de serviço | **Médio-alto.** ABC/XYZ, σ, capital imobilizado |
| **4. Transporte** | Como mover, com que frequência, por qual rota | **Médio.** Tabela de frete, custo por rota, planilha |

**Os 4 conceitos para ter na ponta da língua**
1. **√N** no estoque de segurança, e a ligação com diversificação de portfólio
2. **Custo total de servir**, nunca otimizar uma linha isolada
3. **Nível de serviço é decisão econômica**: 95% → 99% custa +41% de estoque de segurança
4. **Transit point** como meio-termo entre um e dois CDs

**Os 3 números**
2º CD hoje: **−R$ 1,8 M/ano** · virada em **~R$ 650 M** de receita · transit point: **+R$ 0,93 M/ano**
