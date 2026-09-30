# Parte 4.2 — 20 Perguntas Técnicas Esperadas

> **Calibragem:** as respostas abaixo estão escritas no nível que se espera de um **júnior/estagiário com base quantitativa sólida** — não de um cientista de dados sênior. O objetivo não é parecer expert; é demonstrar **fundamento correto, vocabulário certo e honestidade sobre o limite**.

> **Regra de ouro que vale para todas as 20:** quando não souber, diga que não sabe e mostre como pensaria sobre o problema. Num time cujo valor é "Rigor Analítico", **blefe detectado é eliminatório**. Não saber é aceitável em júnior; fingir saber, não.

---

## 🏷️ Bloco A — Pricing e Elasticidade (oferta nº 1 da ATY)

### 1. Como você estimaria a elasticidade-preço de um produto?

**Por que perguntam:** é a competência declarada de Nicole e André, e a primeira frase da oferta de Gestão de Categoria. Para você, estudante de Economia, **é a pergunta que você mais tem obrigação de acertar**.

**Resposta:**

> "O ponto de partida é a especificação log-log: regredir o log da quantidade sobre o log do preço, porque aí o coeficiente do preço já é a própria elasticidade — variação percentual de quantidade por variação percentual de preço.
>
> Mas a estimativa ingênua é enviesada, e o motivo é que **preço não é aleatório**. Três problemas concretos:
>
> **Primeiro, endogeneidade/simultaneidade.** Preço e quantidade são determinados conjuntamente. Se a empresa sobe preço quando enxerga demanda forte, o coeficiente vem atenuado — parece que o produto é menos elástico do que é.
>
> **Segundo, variável omitida.** Promoção quase nunca vem sozinha: vem com destaque no encarte, ponta de gôndola, sazonalidade. Se eu não controlo isso, atribuo ao preço um efeito que é de exposição.
>
> **Terceiro, concorrência.** O que importa é preço relativo, não absoluto. Preciso do preço do concorrente e dos substitutos, para capturar elasticidade cruzada e canibalização.
>
> Então o que eu faria: controlar o máximo observável — sazonalidade, calendário promocional, estoque e ruptura, preço de substitutos — e usar efeitos fixos de produto e de loja para absorver heterogeneidade estrutural. Se houver instrumento crível — custo de insumo, câmbio, choque de frete que mexe no preço sem mexer na demanda — usaria variável instrumental.
>
> E a versão ideal, que é o que eu imagino que vocês fazem: **experimento de preço**. Variar preço deliberadamente em lojas ou regiões comparáveis. Aí a variação é exógena por construção e a elasticidade sai limpa, sem depender de premissa de identificação."

**Se perguntarem "e se a elasticidade for -0,8?"** → "É inelástica: aumento de 10% no preço derruba só 8% do volume, então **receita sobe**. E se olho margem em vez de receita, a conta melhora mais ainda, porque vendo menos unidade com margem maior. Nesse caso, preço baixo está deixando dinheiro na mesa — que é provavelmente o tipo de achado do case de +7 p.p. de lucro em moda."

---

### 2. O que é pricing dinâmico e quando NÃO usar?

**Resposta:**

> "Pricing dinâmico é ajustar preço ao longo do tempo em função de demanda, estoque, sazonalidade, concorrência e disposição a pagar, em vez de fixar preço por tabela e revisar por calendário.
>
> **Onde funciona bem:** estoque perecível ou com prazo — moda com coleção e markdown, passagem aérea, hotel — e e-commerce, onde mudar preço é barato e reversível.
>
> **Onde eu não usaria, ou usaria com muito cuidado:**
>
> - **Quando dói na percepção de justiça.** Preço que muda demais, ou que muda por cliente, gera percepção de discriminação e queima confiança na marca. Em varejo físico de recorrência, isso pode custar mais que o ganho.
> - **Quando há risco regulatório.** Categorias sensíveis — medicamento, combustível — têm escrutínio de CADE e de órgãos de defesa do consumidor. Vale notar que o André tinha interação com CADE e Banco Central no Elo, então imagino que vocês tratem isso com cuidado.
> - **Quando o custo de mudar preço é alto.** Etiqueta física, encarte impresso, catálogo: o custo operacional pode comer o ganho.
> - **Quando o dado não sustenta.** Se não há variação histórica de preço, não há como estimar elasticidade. Modelo sofisticado em cima de dado sem variação é falsa precisão.
> - **Quando o cliente não tem maturidade para operar.** Um modelo que o time comercial não entende não é seguido. Prefiro regra mais simples e adotada do que modelo ótimo e ignorado."

**☝️ O último ponto é o que mais pontua**, porque é exatamente o valor "Solução Duradoura" da ATY.

---

### 3. Como você mediria se uma mudança de preço deu certo?

**Resposta:**

> "Primeiro, definir a métrica certa. Receita é armadilha: posso subir receita destruindo margem com desconto. Eu olharia **margem bruta absoluta** como métrica primária, com volume como guardrail para não crescer margem matando a categoria.
>
> Segundo, o contrafactual. Comparar antes e depois é fraco porque confunde efeito de preço com sazonalidade e tendência. O ideal é **teste controlado** — aplicar em um conjunto de lojas e manter outro comparável como controle, com aleatorização ou pareamento por porte, região e histórico de venda.
>
> Terceiro, efeitos de segunda ordem, que é onde análise ingênua erra mais: **canibalização** — subi o preço do produto A e migrou para B, então a margem de categoria pode não ter mudado — e **efeito de tráfego**, se o item era gerador de fluxo de loja.
>
> Por isso eu avaliaria no nível de **categoria**, não de SKU. O SKU pode melhorar e a categoria piorar."

---

## 🏷️ Bloco B — Forecasting e Séries Temporais (oferta nº 2)

### 4. Como você construiria um forecast de demanda?

**Resposta:**

> "Começaria definindo **para que serve a previsão**, porque isso muda o desenho todo: previsão para compra precisa de horizonte de lead time do fornecedor; previsão para orçamento é mensal e agregada; previsão para reposição de loja é semanal e granular. Granularidade e horizonte vêm da decisão, não do dado.
>
> Depois, **baseline sério antes de qualquer modelo**: média móvel, ou naive sazonal — que é usar o mesmo período do ano anterior. Em varejo com sazonalidade forte, naive sazonal é surpreendentemente difícil de bater, e é a régua honesta. Se um modelo complexo não bate isso, ele não deveria ir para produção.
>
> Modelo: começaria por decomposição — tendência, sazonalidade, resíduo — e SARIMA ou Prophet para capturar sazonalidade múltipla e feriado. Se houver variável externa relevante — preço, promoção, clima, calendário —, aí prefiro abordagem com regressores, tipo gradient boosting com features de calendário e lags, que lida melhor com esse tipo de informação que ARIMA puro.
>
> Validação: **backtest com janela deslizante**, nunca split aleatório.
>
> Métrica: **WMAPE**, que eu vi que vocês usam. E o motivo é bom: MAPE explode quando o denominador é pequeno — um SKU que vendeu 1 unidade e você previu 3 gera 200% de erro e contamina a média — e trata igualmente um SKU de giro alto e um de cauda longa. WMAPE pondera pelo volume, então reflete o impacto econômico real do erro."

**☝️ Citar WMAPE e explicar por que é superior ao MAPE em varejo é o detalhe que mostra que você pesquisou de verdade.**

---

### 5. Por que não se pode usar split aleatório em série temporal?

**Resposta curta e precisa:**

> "Porque gera vazamento temporal. Se eu sorteio linhas aleatoriamente, o treino contém pontos posteriores aos do teste — o modelo aprende com o futuro para prever o passado. A performance medida fica otimista e não se reproduz em produção, onde só existe passado.
>
> O correto é **split temporal**: treinar até uma data de corte e testar no período seguinte. E para robustez, backtest com janela deslizante — repetir isso em vários cortes, para ver se o erro é estável ou se aquele resultado foi sorte de um período específico."

---

### 6. Como trataria uma promoção ou evento atípico no histórico?

**Resposta:**

> "Não removeria sem pensar, porque promoção não é ruído — é informação, e provavelmente vai acontecer de novo. Eu a modelaria como variável explicativa: flag de promoção, profundidade do desconto, tipo de mecânica.
>
> Para evento genuinamente único e irrepetível — uma ruptura de fornecimento, um lockdown — eu trataria como outlier e controlaria com dummy, para o modelo não aprender aquele padrão como recorrente.
>
> E o cuidado extra: se a promoção antecipa compra, ela **rouba demanda do período seguinte**. Um modelo que não captura isso superestima o período pós-promoção. Vale medir o efeito líquido numa janela maior, não só no pico."

---

## 🏷️ Bloco C — Experimentação e A/B Testing

### 7. Como você desenharia um teste A/B?

> ⚠️ **Você nunca rodou um. Não finja.** Abra com a teoria, e ofereça o gap com naturalidade se pressionado.

**Resposta:**

> "Começaria pela hipótese escrita de forma falsificável: qual mudança, em qual métrica, em qual magnitude. 'Melhorar engajamento' não é hipótese testável.
>
> Definiria **uma** métrica primária — múltiplas métricas primárias criam problema de comparação múltipla e viram desculpa para escolher o resultado que agradou — mais métricas de guardrail para detectar dano colateral.
>
> Calcularia o **tamanho de amostra antes de começar**, a partir de quatro coisas: baseline da métrica, efeito mínimo detectável que é economicamente relevante, nível de significância e poder — convenção de 5% e 80%. Esse cálculo diz se o teste é viável: se preciso de seis meses para detectar o efeito, talvez o teste não valha.
>
> Aleatorizaria na **unidade correta**, que é o erro mais comum. Se o efeito contamina entre indivíduos, aleatorizo por loja ou região, não por cliente — senão o controle é afetado pelo tratamento e o efeito medido vem atenuado.
>
> Definiria a duração antecipadamente e **não olharia o resultado antes do fim** — peeking com parada ao primeiro resultado significativo infla drasticamente o erro tipo I.
>
> Na leitura: efeito com **intervalo de confiança**, não só p-valor. E separaria significância estatística de relevância prática — efeito de 0,3% pode ser significante com amostra grande e irrelevante para o negócio."

**Se perguntarem "você já rodou algum?":**

> "Rodado em produção, não. Minha base é de inferência estatística pela Econometria, e eu desenhei o experimento que *deveria* ter feito num caso próprio — reduzi inadimplência com um controle de cobrança mas sem grupo de controle, então não consigo afirmar causalidade, só o mecanismo direto. Foi aprendendo a enxergar essa limitação que eu passei a estudar desenho experimental a sério. É uma das coisas que mais quero fazer na prática."

**☝️ Essa resposta converte um gap em demonstração de maturidade analítica.**

---

### 8. Qual a diferença entre significância estatística e relevância prática?

> "Significância estatística responde 'o efeito que eu vi é distinguível de zero, dado o ruído?'. Relevância prática responde 'esse efeito muda alguma decisão?'.
>
> Com amostra suficientemente grande, quase qualquer efeito fica significante — inclusive efeitos triviais. O inverso também acontece: um efeito economicamente relevante pode não atingir significância se a amostra for pequena, e aí o erro é concluir 'não funciona' quando o correto é 'não consegui medir'.
>
> Por isso eu defino o **efeito mínimo detectável a partir do negócio, antes do teste**: quanto de ganho justifica o custo de implementar? Aí o teste é dimensionado para responder a pergunta que importa, não para produzir um p-valor."

---

### 9. O que é p-hacking e como evitar?

> "É explorar o dado até achar um resultado significante e reportá-lo como se fosse a hipótese original. As formas comuns: testar muitas métricas e reportar a que deu certo, parar o teste quando fica significante, cortar em subgrupos até achar um que funcione, ou excluir outlier que atrapalha.
>
> Como evitar: **registrar hipótese, métrica primária e duração antes de começar**; corrigir para múltiplas comparações quando testar várias métricas; não fazer parada adaptativa sem método sequencial apropriado; e tratar análise de subgrupo como geradora de hipótese, nunca como conclusão — subgrupo precisa de teste próprio para valer.
>
> Vale dizer que em consultoria a pressão para p-hacking é estrutural: o cliente pagou e quer resultado positivo. Acho que é aí que rigor analítico deixa de ser técnica e passa a ser postura."

---

## 🏷️ Bloco D — Machine Learning

### 10. Descreva seu processo para desenvolver um modelo do zero.

> "Antes do dado, três perguntas de negócio: **qual decisão esse modelo vai mudar, quem decide, e com que frequência?** Se não há decisão associada, não tem por que fazer o modelo. Isso define target, granularidade, latência e o quanto de interpretabilidade é necessária.
>
> Depois:
>
> 1. **Definir o target com precisão.** É onde nasce a maioria dos erros. 'Prever churn' não é definição: churn é 30 dias sem compra, ou 90? Isso muda o problema inteiro.
> 2. **Baseline simples primeiro** — regra de negócio atual, média histórica, ou regressão logística. É a régua e às vezes já é a solução.
> 3. **Explorar e entender o dado.** Distribuições, missing, outliers, e principalmente: **o dado disponível no momento da predição é o mesmo que eu tenho agora?** É aqui que mora o vazamento.
> 4. **Feature engineering com hipótese de negócio.** Cada variável deveria ter uma razão para estar lá.
> 5. **Modelar do simples para o complexo**, só subindo complexidade se o ganho compensar a perda de interpretabilidade e de facilidade de manutenção.
> 6. **Validar com o desenho correto** — temporal se houver ordem, estratificado se houver desbalanceamento.
> 7. **Interpretar.** Importância de variável, e checar se faz sentido para quem conhece o negócio. Feature importante e inexplicável geralmente é vazamento, não descoberta.
> 8. **Traduzir em ação.** Score sem regra de decisão não serve. Onde corta? O que se faz com quem está acima do corte?
> 9. **Monitorar** — drift de dado e de performance.
>
> E um viés que eu tento manter: em consultoria, prefiro o modelo que o cliente entende e mantém ao modelo com 2 pontos a mais de AUC que ninguém sabe operar."

---

### 11. Como você escolhe entre modelo interpretável e modelo complexo?

> "Olho três coisas.
>
> **Primeiro, o custo do erro e a exigência de explicação.** Se a decisão precisa ser justificada — crédito negado, cobrança, algo com implicação regulatória — interpretabilidade não é preferência, é requisito. Imagino que o André tenha vivido isso no Elo, com CADE e Banco Central: modelo de risco de crédito precisa ser explicável ao regulador.
>
> **Segundo, o ganho real.** Se a árvore complexa ganha pouco de uma logística bem especificada, o ganho não paga o custo de manutenção e de confiança.
>
> **Terceiro, quem vai operar.** Modelo que o time do cliente não entende não é seguido. Um modelo pior que é usado gera mais valor que um melhor que é ignorado.
>
> Um caminho intermediário que eu acho útil: usar o modelo complexo para descobrir o padrão e depois destilar numa regra simples que capture a maior parte do ganho e seja operável."

---

### 12. Como detectaria e evitaria vazamento de dados (data leakage)?

> "Vazamento é quando o treino usa informação que não existiria no momento real da predição. Os sinais clássicos: performance suspeitamente alta, ou uma variável dominando a importância sem explicação de negócio.
>
> Fontes comuns:
> - **Vazamento temporal** — usar informação posterior ao evento. Ex.: prever inadimplência usando um campo que só é preenchido *depois* que a dívida foi para cobrança.
> - **Vazamento de pré-processamento** — calcular normalização, imputação ou encoding com a base inteira antes de separar treino e teste. O correto é ajustar só no treino e aplicar no teste.
> - **Vazamento por duplicata ou agrupamento** — mesma entidade em treino e teste. Se a unidade é cliente, o split tem que ser por cliente, não por transação.
> - **Proxy do target** — variável que é consequência do resultado, não causa.
>
> A checagem prática que eu faria: para cada variável, perguntar 'no momento em que eu preciso fazer essa predição na vida real, esse campo já está preenchido?'. Se a resposta for não ou 'depende', é suspeito."

---

### 13. Como lidar com classes desbalanceadas (ex.: fraude)?

> "Primeiro, abandonar acurácia. Com 1% de fraude, um modelo que diz 'nunca é fraude' acerta 99% e é inútil. Uso **precisão e recall, curva PR, e AUC-PR**, que é mais informativa que ROC em desbalanceamento severo.
>
> Segundo, definir o trade-off pelo custo real: quanto custa uma fraude não detectada versus quanto custa investigar um falso positivo? Isso define o ponto de corte, e é decisão de negócio, não estatística. No case de fraude em saúde com R$ 9,8M de economia, imagino que essa conta tenha sido central — porque cada alerta gera custo de auditoria.
>
> Técnicas: **class weights** costumam ser meu primeiro recurso, por ser simples e não distorcer o dado; SMOTE ou undersampling se necessário, mas **só no treino, nunca na validação** — senão a métrica mede uma realidade que não existe.
>
> E uma coisa prática: em fraude, frequentemente o mais valioso não é o score, é o **ranking** — entregar a lista dos N casos mais suspeitos que a equipe de auditoria consegue investigar na capacidade que ela tem. Aí a métrica que importa é precisão no top N, não AUC global."

---

### 14. O que é overfitting e como você identifica?

> "É quando o modelo aprende ruído específico do treino em vez do padrão generalizável. Identifico pela diferença entre performance no treino e em dado não visto — erro baixo no treino e alto no teste é o sinal clássico.
>
> Mitigação: mais dado quando possível; reduzir complexidade; regularização (L1/L2); early stopping em modelos iterativos; e cross-validation para não superajustar a decisão a um único split.
>
> Um ponto menos citado: **overfitting no processo de escolha do modelo**. Se eu testo cinquenta configurações e escolho a melhor no conjunto de validação, eu superajustei à validação. Por isso existe o conjunto de teste separado, tocado só uma vez, no fim."

---

## 🏷️ Bloco E — SQL, Python e Dados

### 15. Como você lidou com uma base de 1,2 milhão de registros?

> ⚠️ **Esta pergunta virá, porque está no seu CV.** Prepare a resposta real. O esqueleto:

> "A decisão principal foi **onde fazer o trabalho pesado**. Com 1,2M de linhas, trazer tudo cru para o Python e agregar em memória é possível mas ineficiente — o banco é melhor nisso. Então eu `[VERIFICAR: agregou no SQL antes? filtrou? trouxe cru?]`.
>
> No SQL eu `[VERIFICAR: joins, filtros, agregações, window functions]`.
>
> No Python, o cuidado foi com tipo de dado — `[se aplicável: converter object para category, downcast de numérico]` — e evitar loop linha a linha em favor de operação vetorizada.
>
> O gargalo real foi `[VERIFICAR]`."

**Se a base era pequena o suficiente para pandas puro, diga isso.** 1,2M linhas cabe em memória tranquilamente — admitir que não precisou de Spark é mais honesto e mais correto tecnicamente do que inventar complexidade. Inclusive é um bom ponto: *"1,2 milhão de linhas ainda cabe em pandas; eu não precisaria de Spark aí, e acho importante não inventar complexidade que o problema não pede."*

---

### 16. Escreva/explique uma query com window function.

**O que você precisa saber fazer:**

```sql
-- Ranking de produtos por margem dentro de cada categoria
SELECT
    categoria,
    produto,
    margem,
    ROW_NUMBER()  OVER (PARTITION BY categoria ORDER BY margem DESC) AS rank_margem,
    SUM(margem)   OVER (PARTITION BY categoria)                     AS margem_categoria,
    margem / SUM(margem) OVER (PARTITION BY categoria)              AS share_na_categoria
FROM vendas;

-- Comparação com o mês anterior (crescimento MoM)
SELECT
    mes,
    receita,
    LAG(receita) OVER (ORDER BY mes)                                  AS receita_mes_anterior,
    receita / LAG(receita) OVER (ORDER BY mes) - 1                    AS crescimento_mom,
    AVG(receita) OVER (ORDER BY mes ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) AS media_movel_3m
FROM receita_mensal;
```

**Conceitos para dominar:**
- `PARTITION BY` reinicia o cálculo por grupo; `ORDER BY` define a ordem dentro da janela
- `ROW_NUMBER` vs. `RANK` vs. `DENSE_RANK` — diferença no tratamento de empate
- `LAG` / `LEAD` para comparação temporal
- Frame (`ROWS BETWEEN`) para média móvel
- **Diferença-chave:** window function **não colapsa linhas**; `GROUP BY` colapsa. Window permite ter o detalhe e o agregado na mesma linha.

---

### 17. Como você garante qualidade de dado num projeto?

> "Trato como camada explícita do trabalho, não como etapa implícita.
>
> Começo pelo **perfil do dado**: contagem de linhas, unicidade da chave, % de nulo por coluna, distribuição e faixa dos numéricos, cardinalidade dos categóricos. Isso já revela a maioria dos problemas.
>
> Depois, **reconciliação contra fonte independente**: o total de receita da minha base fecha com o que a controladoria reporta? Essa é a checagem que mais me salvou no trabalho financeiro. Se não fecha, o modelo não importa — o número não é confiável, e um número não confiável apresentado para diretoria custa credibilidade que não se recupera fácil.
>
> Depois, **testes recorrentes** — chave única, campo obrigatório não nulo, valor dentro de faixa esperada, volume dentro do intervalo histórico. Entendo que é isso que se formaliza com testes no dbt.
>
> E **documentar a decisão de tratamento**, porque a escolha de como imputar ou excluir afeta o resultado, e quem lê depois precisa saber o que foi feito. Isso é o mesmo princípio da rastreabilidade que eu implementei no fechamento contábil: cada número tem que ser rastreável até a origem."

---

### 18. O que é dbt e por que se usa? / Conhece Databricks?

> **Seja honesto e mostre que estudou o conceito:**

> "Não usei em cliente. Estudei o conceito porque vi que faz parte do stack de vocês.
>
> **dbt** é transformação de dado no data warehouse com disciplina de engenharia de software: as transformações são SELECTs versionados em Git, organizados em camadas — staging, intermediate, marts —, com testes automatizados, documentação e lineage. Duas coisas me atraem nele: a transformação deixa de ser script solto na máquina de alguém e passa a ser código revisável; e o lineage mostra o que quebra quando você muda algo upstream. É a versão madura do problema de rastreabilidade que eu resolvi na mão no fechamento contábil.
>
> **Databricks** eu entendo como plataforma unificada sobre Spark — notebook, job, Delta Lake para transação e versionamento no data lake, MLflow para rastrear experimento e registrar modelo. A arquitetura medallion, bronze/silver/gold, é a organização por nível de refinamento: cru, limpo, pronto para consumo.
>
> Não vou dizer que sei operar em produção, porque não sei. Mas conceito e vocabulário eu tenho, e por vir de SQL a curva do dbt me parece curta."

---

### 19. O que são agentes de IA e onde fazem sentido?

> ⚠️ **A oferta nº 4 do site fala em "integram agentes inteligentes" e "torres de controle". Esta pergunta é provável.**

> "A distinção que eu faço: um chatbot responde; um **agente** decide e age. Ele tem um objetivo, acesso a ferramentas — consultar banco, chamar API, executar cálculo —, capacidade de encadear passos e de reagir ao resultado de cada passo.
>
> Onde eu vejo fazer sentido: tarefa com muitos passos, regras que mudam com frequência, e onde o caminho não é totalmente previsível de antemão. Por exemplo, um agente que monitora um painel de performance, detecta desvio, investiga a causa provável cruzando fontes, e entrega um diagnóstico com a recomendação — que é mais ou menos o que eu imagino por trás de 'torre de controle capaz de orquestrar performance ponta a ponta'.
>
> Onde eu **não** usaria: quando a tarefa é determinística e bem definida — aí SQL agendado ou regra resolve, é mais barato, mais rápido e auditável. E quando o custo do erro é alto sem revisão humana, porque agente erra de forma menos previsível que regra.
>
> Minha preocupação principal seria observabilidade e custo: agente que encadeia chamadas fica caro e difícil de depurar. Vi que o Gilberto trabalhou estimativa precisa de custo de processamento em MLOps — imagino que essa disciplina fique ainda mais crítica com agente, porque o consumo é variável por natureza."

**☝️ Fechar conectando ao trabalho real do Gilberto é um movimento forte.** Mostra que você leu, entendeu e conectou.

---

### 20. Como você comunica resultado técnico para quem não é técnico?

> "Invertendo a ordem natural. A tentação de quem fez a análise é contar a jornada — dado, método, resultado. Para quem decide, isso é ruído. Eu começo pela **recomendação e pelo impacto**, e só entro no método se perguntarem ou se o método for a razão de confiar.
>
> Isso eu aprendi na prática, e de forma bem concreta: eu produzia o relatório que a diretoria usava para alocar mais de R$ 5 milhões. Ninguém ali queria saber como eu conciliei as 400 transações — queriam saber onde a margem desviou e o que fazer. Então o relatório passou a ser organizado na ordem da decisão, não na ordem da apuração.
>
> Três coisas que eu faço:
>
> **Traduzo métrica técnica em métrica de negócio.** Ninguém decide com AUC. 'O modelo acerta 7 de cada 10 na lista prioritária, então a equipe que investiga 100 casos por mês vai encontrar 70 em vez de 20' — isso decide.
>
> **Explicito a incerteza sem esconder e sem exagerar.** Dizer 'a estimativa é 8% com intervalo entre 5 e 11' é mais útil que '8%', e mais honesto que 'mais ou menos 8'.
>
> **Deixo a recomendação acionável.** Não 'a categoria X tem elasticidade baixa', mas 'dá para subir preço em X até Y% com perda esperada de volume de Z, e o efeito em margem é W — sugiro testar em 20 lojas antes de generalizar'.
>
> E ensinar me ajudou muito nisso. Quando você explica estruturação de problema para 80 alunos que nunca viram um case, você aprende rápido que a clareza é responsabilidade de quem explica, não de quem escuta."

---

## Perguntas bônus que podem aparecer

**21. Qual a diferença entre correlação e causalidade — e como você lida na prática?**
→ Fale de confundidor, e das ferramentas: aleatorização (padrão-ouro), diferenças-em-diferenças, variável instrumental, controle por observável. Mencione que na Econometria você viu isso formalmente. **Conecte com o Case 4** (inadimplência sem grupo de controle) — é a sua melhor demonstração de honestidade causal.

**22. O que é LTV e como calcularia?**
→ Margem por cliente × tempo de retenção esperado, descontado a valor presente. **Aqui você tem vantagem:** desconto a valor presente é Matemática Financeira e Finanças Corporativas — você faz isso com propriedade. Mencione que LTV sem desconto e sem margem (só receita) é erro comum. André declara LTV como expertise.

**23. Como você definiria churn num varejo sem contrato?**
→ Não existe evento de cancelamento, então churn é construção: janela sem compra calibrada pelo ciclo de recompra da categoria. Cite que a janela errada inventa ou esconde churn — em categoria de compra anual, 90 dias sem comprar não é churn.

**24. Explique viés e variância.**
→ Viés é erro por premissa simplificadora demais (modelo não captura o padrão); variância é sensibilidade excessiva ao dado de treino. Modelo simples tende a viés alto, complexo a variância alta. Conecte: *"em consultoria eu tendo a aceitar um pouco mais de viés em troca de estabilidade e interpretabilidade, porque modelo instável quebra a confiança do cliente rápido."*

**25. Você tem 2 semanas e o dado do cliente está uma bagunça. O que faz?**
→ Priorizar: qual é a **única** pergunta que precisa ser respondida? Reduzir escopo para o subconjunto de dado confiável e responder bem uma coisa, em vez de responder mal cinco. Documentar as limitações explicitamente. Entregar o diagnóstico da qualidade do dado como resultado — frequentemente é o achado mais valioso, porque destrava tudo o que vem depois.

---

## Como se preparar para este bloco

**As 6 perguntas com maior probabilidade de aparecer, na sua ordem de prioridade:**

1. **Nº 15** — sobre os 1,2M registros (está no seu CV; é certa)
2. **Nº 1** — elasticidade (você é economista; eles esperam que você saiba)
3. **Nº 4** — forecast de demanda (oferta central)
4. **Nº 7** — desenho de A/B test (competência declarada de dois dos três)
5. **Nº 20** — comunicação (você tem a melhor resposta do repertório aqui)
6. **Nº 10** — processo de modelagem (pergunta padrão)

**Ensaie em voz alta.** Resposta técnica lida no papel parece fluida e sai travada na boca. Grave-se respondendo as seis acima e ouça — você vai encontrar os pontos onde está inseguro, e são exatamente esses que o entrevistador vai farejar.
