# Parte 4.1 — 7 Cases STAR Construídos da Sua Experiência Real

> **Princípio:** todos os cases abaixo usam **apenas fatos do seu currículo**. Onde há lacuna, marquei `[VERIFICAR]` — você precisa preencher com o número real ou remover. **Não invente dado.** Num time cujo valor declarado é "Rigor Analítico", um número inventado que desmorona sob pergunta destrói a entrevista inteira.

> **Como cada case está organizado:** Situation → Task → Action → Result, seguido de *força do case*, *riscos*, *perguntas de aprofundamento esperadas* e *ponte com a ATY*.

---

## Case 1 — Rentabilidade e Controle de Margem
### 🎯 Tema: Revenue/Margin Optimization · Oferta ATY: Gestão de Categoria

**Força: ⭐⭐⭐⭐ | Risco: usar como análogo de pricing sem assumir a diferença**

### Situation
Na V4 Company, a diretoria decidia a alocação de um orçamento anual superior a R$ 5 milhões. A decisão dependia de entender, mês a mês, como receitas, custos e margens estavam se comportando contra o que havia sido projetado — mas não havia uma visão consolidada e confiável que permitisse enxergar isso com a granularidade necessária para agir.

### Task
Como Analista Financeiro Júnior, eu era responsável pelas análises mensais de DRE, pela modelagem financeira e pelas projeções de fluxo de caixa. Meu produto final era o relatório gerencial que a diretoria usava como base de decisão de alocação orçamentária — o que significa que **eu não estava produzindo um relatório informativo, estava produzindo o insumo de uma decisão de R$ 5M**.

### Action
1. **Estruturei a leitura de DRE por período**, separando receitas, custos e margens de forma comparável mês a mês.
2. **Construí o modelo de comparação realizado vs. projetado**, que é onde o valor analítico realmente está: não importa o número absoluto, importa o desvio e a causa do desvio.
3. **Investiguei os desvios**, atacando as linhas de maior variação para entender se a causa era volume, preço, mix ou custo — a decomposição clássica de variação de margem.
4. **Consolidei em relatório gerencial** com a informação organizada na ordem em que a diretoria precisava decidir, não na ordem em que o sistema contábil entregava.

### Result
- A diretoria passou a ter base recorrente e confiável para alocar orçamento anual de **R$ 5M+**
- A comparação realizado vs. projetado permitiu correção de rota dentro do exercício, não só no fechamento
- `[VERIFICAR]` — Se você tiver: erro médio de projeção, número de linhas de custo revisadas, ou alguma decisão específica que mudou por causa de uma análise sua, **adicione aqui**. É o que falta para o case virar ⭐⭐⭐⭐⭐.

### 🔗 Ponte com a ATY
A oferta de **Gestão de Categoria** da ATY é descrita como "otimizar preços, definir o sortimento ideal e **impulsionar a rentabilidade**". Rentabilidade é o objetivo final; margem é o mecanismo. **Eu venho do lado do mecanismo** — sei ler onde a margem vaza e decompor variação. O que eu não fiz ainda foi usar analytics para *otimizar* o preço que gera essa margem, e é exatamente isso que quero aprender.

### ⚠️ Como se defender
Se perguntarem *"isso é pricing?"*, a resposta honesta é:

> *"Não, e eu não quero vender como se fosse. Eu analisei margem realizada; pricing é decidir o preço que a gera. A ponte que eu vejo é que quem otimiza preço precisa saber exatamente onde a margem vaza — mix, desconto, custo — e essa parte eu fiz na prática. A elasticidade eu tenho pela Econometria, na teoria."*

### Perguntas de aprofundamento esperadas
- *Como você decompunha uma variação de margem?* → volume × preço × mix × custo
- *O que causava mais desvio nas projeções?* → `[VERIFICAR]`
- *Você já sugeriu mudar um preço?* → responda com honestidade
- *Como a diretoria usava o relatório na prática?*

---

## Case 2 — Projeção de Fluxo de Caixa como Exercício de Forecasting
### 🎯 Tema: Forecasting / Demand Planning · Oferta ATY: Supply Chain

**Força: ⭐⭐⭐⭐ | Risco: confundir projeção financeira com modelo estatístico de série temporal**

### Situation
A V4 Company precisava de previsibilidade de caixa para operar. Sem projeção confiável, a empresa decide no escuro: não sabe se pode antecipar um investimento, se vai precisar de capital de giro, ou se uma despesa aprovada cabe no mês.

### Task
Eu era responsável pelas projeções de fluxo de caixa e pelo acompanhamento de receitas, custos e margens de cada período, comparando realizado com projetado.

### Action
1. **Estruturei a projeção a partir dos drivers** — receitas por origem, custos fixos e variáveis, calendário de recebíveis e de pagáveis — em vez de projetar um agregado.
2. **Estabeleci o ciclo de medição de erro:** todo mês, realizado contra projetado, e a diferença virava pergunta, não apenas registro.
3. **Revisei premissas com base no erro observado**, que é o loop de aprendizado de qualquer forecast.
4. **Integrei com a operação de caixa** — eu mesmo administrava conciliação bancária e contas a pagar/receber com mais de 400 transações mensais, o que significa que **minha projeção era alimentada pelo dado que eu mesmo tratava**. Não havia intermediário entre o dado bruto e a previsão.

### Result
- Visão diária e confiável da posição de caixa para a gestão
- Loop mensal estabelecido de realizado vs. projetado com revisão de premissa
- `[VERIFICAR]` — erro médio de projeção, se você mediu. **Se você tiver qualquer número de acurácia aqui, é o maior ganho possível neste case.**

### 🔗 Ponte com a ATY
A oferta de **Supply Chain** fala em "aprimorar a previsão de demanda". O André atingiu **2,3% de WMAPE** com redes neurais. O objeto é diferente — caixa não é demanda — mas **a disciplina é a mesma**: projetar, medir erro, entender se o erro é viés ou variância, revisar premissa, repetir. Eu aprendi essa disciplina no lado financeiro, com método de negócio. Quero aprender a fazê-la com método estatístico.

### ⚠️ Como se defender (este é o ponto mais provável de ataque)
Se perguntarem *"que modelo você usou?"* — **não blefe**. A resposta forte é:

> *"Foi projeção baseada em driver de negócio e calendário de recebimento, não modelo estatístico de série temporal. Eu não rodei ARIMA nem Prophet ali. Mas sei qual é a diferença e por que ela importa: minha projeção não me dava intervalo de confiança nem separava sazonalidade de tendência, e eu validava contra o mês seguinte, não com backtest de janela deslizante. É justamente essa camada que eu quero construir."*

**Essa resposta é melhor do que se você tivesse usado ARIMA.** Ela prova que você conhece o método correto, sabe o que faltava no seu, e não inflou nada. É o valor "Rigor Analítico" em ação.

### Perguntas de aprofundamento esperadas
- *Qual era o horizonte da projeção?* → `[VERIFICAR]`
- *Como tratava sazonalidade?*
- *Por que WMAPE e não MAPE em varejo?* → MAPE explode com denominador pequeno e não pondera por volume; WMAPE pondera pela quantidade, refletindo impacto econômico real
- *Como você validaria um forecast de demanda hoje?* → holdout temporal / backtest com janela deslizante, nunca split aleatório

---

## Case 3 — Modelos Preditivos em Saúde e Transporte
### 🎯 Tema: Machine Learning / AI · Oferta ATY: transversal

**Força: ⭐⭐⭐⭐⭐ POTENCIAL / ⭐⭐ ATUAL | Risco: 🔴 O MAIS ALTO DE TODOS**

> ### 🔴 LEIA ISTO ANTES
> Este é **o case mais importante e o mais perigoso** do seu repertório. Mais importante porque é o único que fala diretamente a língua técnica da ATY. Mais perigoso porque o seu CV diz *"modelos preditivos"* sem especificar **nada** — e num time com mestrado em estatística e valor declarado de "Rigor Analítico", **três perguntas de aprofundamento sem resposta concreta aqui derrubam a sua credibilidade em todos os outros cases**.
>
> **Você tem duas opções, e precisa escolher antes da entrevista:**
> - **(A)** Reconstituir o projeto com detalhe técnico completo → o case vira o seu mais forte
> - **(B)** Se não conseguir sustentar, reduzir o escopo da afirmação para o que você aguenta defender
>
> **Não existe opção (C) "improviso na hora".**

### Situation
No Clube de Consultoria da UNICAMP, projetos para clientes/parceiros nos setores de **Saúde** e **Transporte** exigiam análise preditiva sobre bases com **mais de 1,2 milhão de registros** — volume em que Excel deixa de ser viável e é preciso tratamento programático.

### Task
Eu era responsável por estruturar os modelos preditivos em Python e as rotinas de extração de dados em SQL, além do tratamento e da análise das bases.

### Action

**Esqueleto a preencher com os fatos reais:**

1. **Extração (SQL):** `[VERIFICAR]` — quais tabelas, que granularidade, que joins, se agregou no banco antes de trazer para o Python (decisão importante com 1,2M registros — mostra que você pensou em performance).
2. **Tratamento:** `[VERIFICAR]` — como tratou missing, outliers, duplicatas; como lidou com o volume (pandas direto? chunks? agregação prévia?).
3. **Feature engineering:** `[VERIFICAR]` — quais variáveis criou e qual a hipótese de negócio atrás de cada uma.
4. **Modelagem:** `[VERIFICAR]` — qual algoritmo, **e principalmente por que ele**. Se foi regressão logística, ótimo: defenda pela interpretabilidade, que é argumento forte em consultoria (cliente precisa entender o modelo para confiar nele).
5. **Validação:** `[VERIFICAR]` — split, cross-validation, métrica escolhida e por quê.
6. **Entrega:** `[VERIFICAR]` — o resultado virou decisão? Quem usou?

### Result
`[VERIFICAR]` — precisa de pelo menos: **uma métrica de performance** + **uma comparação com baseline** + **o que mudou na decisão do cliente**.

> **Sobre baseline:** é a pergunta que separa quem entende modelagem de quem só rodou `fit()`. O que acontecia *antes* do modelo? Se você bateu um baseline simples (média histórica, regra de negócio existente, chute do especialista) por uma margem clara, **isso vale mais que um AUC alto sem contexto** — porque mede valor incremental, não performance absoluta.

### 🔗 Ponte com a ATY
- **Saúde** é o setor do case de detecção de fraude do André (**~R$ 9,8M** de economia)
- **Transporte** conversa com a otimização de rotas e malhas logísticas da Nicole
- 1,2M registros mostra que você não trava em volume

**Frase de conexão:**
> *"Vi que o André trabalhou com detecção de fraude em saúde. Meu contato com o setor foi por outro ângulo e em outra escala, mas o que aprendi ali foi principalmente sobre a qualidade do dado de saúde — `[VERIFICAR: seu aprendizado real]`."*

### Perguntas de aprofundamento esperadas — **prepare TODAS**
1. Qual era a variável-alvo?
2. Qual algoritmo e por que esse?
3. Qual métrica e por que essa? (se classificação com classe desbalanceada: **por que não acurácia?**)
4. Como validou? Houve vazamento de dados?
5. Quais features mais importaram? Fizeram sentido para o negócio?
6. Como tratou 1,2M registros? Onde foi o gargalo?
7. Qual era o baseline?
8. O modelo foi usado? Por quem? Gerou decisão?
9. O que deu errado?
10. Se refizesse hoje, o que mudaria?

---

## Case 4 — Controle de Vencimentos e Redução de Inadimplência
### 🎯 Tema: Intervenção medida (análogo de experimentação) · Oferta ATY: Marketing & Customer Insights / Risco

**Força: ⭐⭐⭐⭐⭐ | Risco: atribuição causal — e é aqui que você BRILHA se souber jogar**

> **Este é o case que eu recomendo abrir a entrevista técnica.** Não porque é o mais sofisticado, mas porque é onde você pode demonstrar **rigor analítico de forma mais convincente** — e rigor analítico é literalmente um dos três valores da ATY.

### Situation
Na V4 Company, a operação financeira movimentava mais de 400 transações mensais. A cobrança de recebíveis acontecia de forma reativa, sem controle sistemático de vencimentos — o que gerava atraso na cobrança, inadimplência na carteira e imprevisibilidade de caixa.

### Task
Eu administrava fluxo de caixa, conciliação bancária e as rotinas de contas a pagar e a receber. Identifiquei que o problema não era volume de cobrança, era **timing**: cobrança que sai depois do vencimento tem taxa de recuperação muito menor.

### Action
1. **Diagnostiquei o mecanismo** — a hipótese não era "precisamos cobrar mais", era "precisamos cobrar antes". Isso é definição de problema, e é onde a maior parte do valor de uma intervenção se decide.
2. **Implantei um controle diário de vencimentos**, transformando um processo reativo em um processo com calendário.
3. **Antecipei a cobrança** dos recebíveis, atuando antes do vencimento em vez de depois do atraso.
4. **Medi o efeito** acompanhando inadimplência da carteira e posição diária de caixa.
5. **Integrei ao relatório de gestão**, para que a posição de caixa deixasse de ser uma consulta pontual e passasse a ser informação diária confiável.

### Result
- **Redução da inadimplência da carteira**
- Antecipação efetiva da cobrança de recebíveis
- Visão diária e confiável da posição de caixa para a gestão
- `[VERIFICAR]` — qualquer número: % de queda de inadimplência, dias de redução no prazo médio de recebimento (DSO), valor recuperado

### 🔗 Ponte com a ATY — e o momento de brilhar

Este case conecta com **duas** coisas de uma vez:

1. **A expertise do André em risco de crédito.** Ele construiu a função de risco do Cartão Elo do zero e modelou risco a partir de demonstrações financeiras. Inadimplência de carteira é o problema dele, em escala menor.
2. **A cultura de experimentação da casa.** E aqui está o movimento decisivo — **qualifique sua própria conclusão antes que perguntem**:

> *"A inadimplência caiu depois da implantação, e o mecanismo é direto: cobrança antes do vencimento recupera mais que cobrança depois do atraso. Mas sendo rigoroso sobre atribuição, eu **não** tinha grupo de controle. Não posso separar o efeito do controle diário de uma eventual mudança no mix de clientes ou na conjuntura do período. O que eu defendo com segurança é a redução do prazo de cobrança, que é o efeito de primeira ordem e está sob meu controle direto. O efeito total na inadimplência eu trataria como hipótese consistente, não como conclusão provada.*
>
> *Se eu fizesse isso hoje com o que sei, eu teria separado a carteira em dois grupos comparáveis e aplicado o controle em um só, por um ou dois ciclos. Aí eu teria o contrafactual e poderia afirmar o efeito com intervalo de confiança."*

**Por que isso é tão forte:** você acabou de demonstrar, sem ser perguntado, que entende (a) atribuição causal, (b) a necessidade de contrafactual, (c) desenho experimental, e (d) a diferença entre o que o dado sustenta e o que você gostaria que sustentasse. Num time que declara "Rigor Analítico" como valor, **isso é o comportamento exato que eles querem ver** — e é raríssimo em candidato júnior, que quase sempre infla resultado.

E, de bônus, cobre parcialmente o seu gap de A/B testing: você não rodou um teste, mas provou que sabe desenhar um.

### Perguntas de aprofundamento esperadas
- *Como você mediria isso corretamente?* → você já respondeu acima; aprofunde em tamanho de amostra e duração
- *Como garantiria que os dois grupos são comparáveis?* → aleatorização; se não possível, pareamento por sacado/ticket/histórico
- *Qual o risco ético/comercial de testar cobrança em só metade da carteira?* → excelente pergunta para responder com maturidade: custo de oportunidade do grupo controle vs. valor de aprender o efeito real
- *O que é DSO e como se calcula?*

---

## Case 5 — Governança de Informação e Rastreabilidade
### 🎯 Tema: Data Governance / sustentação · Oferta ATY: Estratégia de Dados & IA

**Força: ⭐⭐⭐⭐ | Risco: soar administrativo em vez de estratégico**

### Situation
Dois contextos com o mesmo problema estrutural:
- Na **V4 Company**, as rotinas de fechamento mensal e a documentação de controles internos eram frágeis, gerando exposição a risco operacional e lentidão no fechamento.
- No **IME Jr**, informação financeira e jurídica — fluxo de caixa, orçamentos, contratos, notas fiscais — estava dispersa, sem padrão de organização ou nomenclatura.

### Task
Reestruturar ambos: na V4, o processo de fechamento e a documentação de controles; no IME Jr, a arquitetura de arquivo do departamento.

### Action

**Na V4:**
1. **Reestruturei as rotinas de fechamento mensal**, reduzindo o tempo de ciclo.
2. **Documentei os controles internos**, reduzindo exposição a risco operacional.
3. **Estabeleci rastreabilidade ponta a ponta** — cada lançamento passou a ser rastreável até o comprovante de origem.
4. Com isso, **formei a base documental que sustentou as auditorias e os processos de Due Diligence** da empresa.

**No IME Jr:**
1. **Consolidei tudo em estrutura única de mais de 12 pastas**, com hierarquia lógica.
2. **Criei convenção de nomenclatura** que tornou cada documento localizável **por período e por contraparte** — ou seja, defini as duas dimensões de busca que realmente importavam para o uso do dia a dia.
3. **Padronizei o ambiente digital** do departamento.

### Result
- Fechamento mais ágil e com menor risco operacional
- **Rastreabilidade completa até o comprovante** — requisito que sustentou auditoria e Due Diligence
- Arquivo padronizado e localizável, com padrão que sobreviveu à minha atuação

### 🔗 Ponte com a ATY — traduza para o vocabulário deles

A oferta **Estratégia de Dados & IA** fala em "fortalecer a governança". O valor **Solução Duradoura** fala em soluções "sólidas, adaptáveis e sustentáveis ao longo do tempo". O Gilberto construiu governança de deploy de modelos e modelo de governança de dados para varejista farmacêutico.

**O que eu fiz não foi governança de dados — foi governança de informação. Mas os princípios são os mesmos**, e é exatamente essa tradução que você deve fazer em voz alta:

| O que eu fiz | Como se chama em dados |
|---|---|
| Convenção de nomes por período e contraparte | **Naming convention / padrão de catalogação** |
| Rastreabilidade do lançamento até o comprovante | **Data lineage / auditabilidade** |
| Documentação dos controles internos | **Documentação de processo / controles de qualidade** |
| Estrutura única de 12+ pastas com hierarquia | **Arquitetura de camadas / organização de repositório** |
| Base que sustentou auditoria e Due Diligence | **Compliance e confiabilidade do dado** |
| Padrão que sobreviveu à minha saída | **Sustentabilidade / redução de dependência de pessoa** |

**Frase de fechamento:**
> *"Aprendi na prática por que rastreabilidade importa: quando a auditoria e a Due Diligence chegaram, a diferença entre um número defensável e um número frágil era conseguir chegar ao comprovante de origem. Entendo que em dados o problema é o mesmo em outra escala — e é por isso que o MLOps e a governança do Gilberto me interessam: é a diferença entre um modelo que alguém confia e um que ninguém usa."*

### ⚠️ Como não soar administrativo
Nunca descreva como "organizei pastas". Descreva pelo **efeito**: *reduzi risco operacional*, *criei rastreabilidade que sustentou auditoria*, *o padrão sobreviveu à minha saída*. O objeto é banal; o princípio é o mesmo que sustenta governança de dados.

---

## Case 6 — Análise de Custos e Segmentação de Despesa
### 🎯 Tema: Customer/Cost Analytics · Oferta ATY: Gestão de Categoria (rentabilidade)

**Força: ⭐⭐⭐ | Risco: falta de magnitude declarada**

### Situation
No IME Jr, a empresa júnior tinha despesas operacionais sem visibilidade estruturada. Não havia clareza sobre onde o dinheiro estava indo nem sobre quais linhas tinham potencial real de corte — o que tornava o orçamento imprevisível.

### Task
Como Analista Financeiro do departamento Jurídico-Financeiro, analisar as despesas operacionais e identificar oportunidades de redução.

### Action
1. **Categorizei as despesas**, criando a taxonomia que antes não existia — e aqui está o ponto analítico: **a escolha das categorias determina o que você consegue ver**. Categoria errada esconde o problema.
2. **Ordenei por materialidade**, aplicando lógica de Pareto: atacar primeiro onde há volume, não onde é fácil.
3. **Avaliei potencial de redução por linha**, separando custo estrutural (não compressível sem afetar operação) de custo discricionário (compressível).
4. **Recomendei os cortes** de maior relação impacto/esforço.

### Result
- **Economia mensal recorrente** — recorrente é a palavra-chave: não foi corte pontual, foi mudança de patamar
- Maior previsibilidade orçamentária
- `[VERIFICAR]` — valor ou % da economia, e quantas linhas de custo foram revisadas

### 🔗 Ponte com a ATY
Gestão de Categoria existe para "impulsionar a rentabilidade". Rentabilidade se move por dois lados: receita e custo. **Categorizar despesa para achar onde há potencial é estruturalmente o mesmo exercício de categorizar SKU para achar onde há margem** — muda o objeto, não o método: taxonomia correta → materialidade → potencial de ação → recomendação priorizada.

**Frase de conexão:**
> *"A parte que eu mais levei desse trabalho foi que a taxonomia decide o resultado. Com a categoria errada, o custo problemático fica diluído e invisível. Imagino que em gestão de categoria de varejo seja o mesmo problema — como vocês definem o agrupamento de categoria num cliente novo? É pela árvore mercadológica que ele já tem ou vocês reconstroem pelo comportamento de compra?"*

☝️ Essa pergunta final é excelente: mostra que você entende que **definição de categoria é decisão analítica, não cadastro** — que é precisamente o debate real de category management.

---

## Case 7 — Liderança, Ensino e Processo Seletivo
### 🎯 Tema: Cross-functional Leadership · Valor ATY: "fazer juntos"

**Força: ⭐⭐⭐⭐⭐ | Risco: nenhum — este é o seu case mais seguro**

### Situation
O Clube de Consultoria da UNICAMP precisava de duas coisas: **formar** alunos capazes de enfrentar processos seletivos de consultoria (que exigem estruturação de problema, uma habilidade que a graduação não ensina), e **selecionar** os melhores candidatos para o programa trainee.

### Task
Como **Diretor de Gestão de Pessoas** (ago/2025 – set/2026), eu era responsável por instrução, condução do processo seletivo e desenvolvimento dos membros mais novos.

### Action

**Formação — Prep4Consulting (3 edições):**
1. **Ministrei aulas de Finanças e Case Interview** para **mais de 80 alunos por edição**, capacitando-os a estruturar e resolver os problemas exigidos em processos de consultoria.
2. **Orientei os membros mais novos do clube** a responder dúvidas e comentários dos alunos — ou seja, **não escalei apenas a minha entrega, escalei a capacidade do time de entregar**. Formei quem forma.

**Seleção:**
3. **Conduzi o processo seletivo do clube**, atuando em todas as etapas e avaliando desempenho por fase, culminando na seleção para o programa trainee — cuja etapa final é apresentação de case para banca avaliadora.

**Desenvolvimento — Getting the Job:**
4. **Conduzi sessões de preparação** com simulações de entrevista e **devolutiva de desempenho**, além de revisões estratégicas de currículo, para candidatos disputando vagas nas principais consultorias do mercado.

### Result
- **240+ alunos alcançados** (80+ × 3 edições) em Finanças e Case Interview
- Membros novos capacitados a assumir a linha de frente do atendimento aos alunos
- Processo seletivo conduzido com avaliação estruturada por etapa
- Candidatos preparados para processos das principais consultorias do mercado
- `[VERIFICAR]` — se você souber de alguém que passou em processo depois da sua preparação, **isso é resultado e vale citar**

### 🔗 Ponte com a ATY — múltiplas conexões

Este é o case com mais pontes de todo o repertório:

1. **"Fazer juntos" é literalmente o que você faz.** A ATY se define por cocriação e transferência de conhecimento. Você ensina por ofício. Não é afinidade declarada — é comportamento comprovado, três edições seguidas.

2. **Structured problem solving é o método da casa.** A Nicole tem o **McKinsey Forward Program**, cujas competências são resolução de problemas, adaptabilidade e comunicação. **Você ensina essa disciplina.** Vocês têm vocabulário comum imediato.

3. **O André é Licenciado em Matemática** — formado para ensinar. Ele vai reconhecer o valor de quem ensina.

4. **O Gilberto fomenta educação em tecnologia** publicamente (parceria Anchieta × Rocketseat, divulgação de vagas docentes, semana de tecnologia). É valor pessoal dele.

5. **Consultoria é ensinar sob outro nome.** Todo projeto termina em transferência de conhecimento para o cliente. Quem já ensinou 240 pessoas a estruturar problema tem vantagem direta nisso.

**Frase de fechamento:**
> *"A coisa que mais me preparou para consultoria não foi uma disciplina, foi ensinar case interview. Quando você precisa explicar a 80 pessoas como quebrar um problema que elas nunca viram, você descobre rápido que dominar a resposta e conseguir conduzir alguém até ela são habilidades diferentes. Como a ATY se define por construir 'a quatro mãos', imagino que essa segunda habilidade seja a que mais importa no dia a dia com cliente."*

---

## Matriz de decisão: qual case usar em cada situação

| Situação na entrevista | Case principal | Case de reforço |
|---|---|---|
| "Fale sobre você" | 7 (liderança/ensino) | 1 (P&L R$ 5M) |
| "Seu maior impacto de negócio" | 1 (R$ 5M) ou 4 (inadimplência) | 6 (economia recorrente) |
| "Experiência técnica em ML" | 3 (**só se preparado**) | 2 (forecasting) |
| "Como você garante rigor" | **4** (atribuição causal) | 2 (erro de projeção) |
| "Trabalho em equipe / fazer juntos" | 7 | Nunes&Lucato (parcerias) |
| "Projeto que falhou / aprendizado" | `[PREPARAR — ver Parte 6]` | — |
| "Você é mão na massa?" | 4 (400 transações + relatório) | 5 (rastreabilidade) |
| "Governança / sustentabilidade" | 5 | — |
| "Pricing / rentabilidade" | 1 | 6 |
| "Forecasting" | 2 | 1 |
| "Experimentação / A/B" | 4 (desenho que faria) | — |
| "Liderança e influência" | 7 | Nunes&Lucato (Midea/Carrier) |
| "Negociação / cliente" | Nunes&Lucato (NK Store, Track&Field) | 7 |

### Os 3 cases que você precisa dominar ao ponto de contar sem pensar

1. **Case 4 (inadimplência)** — porque é onde você demonstra rigor analítico, que é o valor mais importante deles e o seu maior risco percebido
2. **Case 7 (ensino/liderança)** — porque é onde você é indiscutivelmente forte e onde encosta na cultura "fazer juntos"
3. **Case 1 (R$ 5M / margem)** — porque prova impacto de negócio real com número grande e verificável

**Case 3 é o curinga:** se você o preparar de verdade, ele passa à frente de todos. Se não preparar, **evite-o ativamente** e redirecione para o Case 2 quando o assunto for técnico.
