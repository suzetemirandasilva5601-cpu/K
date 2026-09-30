# Parte 9 — Preenchimento dos Marcadores: Método, Recuperação de Números e Versões Sem Número

> **Como este documento funciona.** Os 26 `[VERIFICAR]` e 10 `[INFERÊNCIA]` do relatório são de naturezas diferentes e recebem tratamentos diferentes:
>
> | Tipo | Tratamento aqui |
> |---|---|
> | **Método / abordagem técnica** | **Preenchido** com a reconstrução mais provável dado o seu stack real e o contexto do projeto. Marcado como `HIPÓTESE` — confirme antes de usar. |
> | **Resultado medido** (%, dias, AUC, R$) | **Não preenchido com número inventado.** Recebe: (a) caminho de recuperação, (b) faixa de sanidade para ancorar sua memória, (c) **versão da frase que é forte sem o número**. |
> | **`[INFERÊNCIA]`** | **Permanece rotulado.** Recebe o raciocínio por trás e a **pergunta** que converte a inferência em fato durante a entrevista. |
>
> ### A linha vermelha
>
> Você vai entrevistar com alguém que construiu modelos de risco de crédito a partir de demonstrações financeiras e prestou contas a CADE e Banco Central. **Número inventado não sobrevive a duas perguntas.** E o custo não é perder aquele número — é que, a partir dali, tudo que você disse fica sob suspeita.
>
> A boa notícia: **quase todo bullet seu é forte sem a métrica**, porque o que você tem de raro é *mecanismo* e *escala de responsabilidade*, não percentual. As reescritas abaixo provam isso.

---

## 9.1 Seu stack real — a base de toda reconstrução

Do seu CV, o que você declara saber usar:

| Ferramenta | Nível declarado | Uso provável nos seus projetos |
|---|---|---|
| **Excel + VBA** | Avançado + certificação | Análise de DRE, despesas, modelagem financeira, automação de rotina |
| **Python** | Declarado | Tratamento de base, modelos preditivos |
| **SQL** | Declarado | Extração das bases de Saúde e Transporte |
| **Power BI** | Declarado | Relatórios gerenciais |

**Consequência para a reconstrução:** nada do que eu proponho abaixo usa ferramenta fora dessa lista. Se a reconstrução sugerir algo que você não fez, **descarte** — não adote uma versão mais impressionante do que a verdade.

---

## 9.2 Bloco crítico — os modelos preditivos (Saúde e Transporte)

> Este é o `[VERIFICAR]` mais importante do relatório. Abaixo, a reconstrução mais provável para cada um dos dez itens do checklist do Case 3.

### Reconstrução de método — `HIPÓTESE, confirme cada linha`

#### 1. Extração em SQL

**Mais provável:** `SELECT` com `JOIN` entre a tabela de eventos e as tabelas de cadastro, `WHERE` de recorte temporal, e `GROUP BY` para reduzir granularidade antes de exportar.

**Por que esta é a hipótese certa:** com 1,2M registros e Python local, a decisão racional é **agregar no banco e trazer o agregado**. Se você trouxe tudo cru, também está certo — 1,2M linhas cabe em memória.

**Como falar disso (e é um bom ponto):**
> "Com 1,2 milhão de linhas eu não precisava de Spark nem de nada distribuído — isso cabe em pandas numa máquina comum. Fiz o filtro e a agregação no SQL porque o banco é melhor nisso que o Python, e trouxe a base já no grão da análise. Acho importante não inventar complexidade que o problema não pede."

☝️ **Esta resposta é melhor que dizer que usou Spark.** Demonstra dimensionamento correto, que é justamente o que se cobra em consultoria.

#### 2. Tratamento em Python

**Mais provável:** `pandas` para carga; checagem de nulos com `isna().sum()`; remoção de duplicatas por chave; conversão de tipos (data, categórico); tratamento de outlier por corte de percentil ou inspeção de distribuição.

**O que vale mencionar sem exagerar:** que você olhou a distribuição antes de decidir o tratamento, e que documentou a decisão. Isso é verdade em qualquer análise séria e é o que o "Rigor Analítico" espera.

#### 3. Feature engineering

**Mais provável dado o contexto:** variáveis de calendário (dia da semana, mês, feriado), agregações históricas por entidade (média, contagem, recência), e variáveis categóricas codificadas.

**Como enquadrar:** cada variável tinha uma hipótese de negócio atrás. Se você criou "média histórica por unidade", a hipótese era que o comportamento passado da unidade prediz o futuro. **Saber verbalizar a hipótese vale mais que a lista de variáveis.**

#### 4. Algoritmo — `escolha a que corresponde à verdade`

| Se o alvo era… | Algoritmo mais provável | Como defender a escolha |
|---|---|---|
| Sim/não (evento ocorre?) | **Regressão logística** | Interpretabilidade: o coeficiente é lido como efeito, e o cliente entende. Padrão em risco. |
| Sim/não, buscando performance | **Árvore de decisão / Random Forest** (`sklearn`) | Captura não-linearidade e interação sem especificação manual |
| Número contínuo (volume, tempo, custo) | **Regressão linear múltipla** | Base econométrica; coeficientes interpretáveis |
| Número, com não-linearidade | **Random Forest Regressor** | Melhor ajuste quando a relação não é linear |

**Se foi regressão logística ou linear, não se desculpe — defenda.** Numa consultoria, a fala forte é:

> "Escolhi regressão logística por interpretabilidade. O cliente precisava entender *por que* o modelo apontava um caso, não só receber o score. Um modelo que ninguém entende não é seguido, e aí ele não gera decisão nenhuma. Testei uma árvore como comparação e o ganho não justificava a perda de leitura."

☝️ Isso alinha diretamente com o valor **Solução Duradoura** da ATY. É a resposta que um sócio quer ouvir.

#### 5. Métrica — `escolha conforme o tipo de problema`

| Problema | Métrica a citar | Por que essa |
|---|---|---|
| Classificação balanceada | Acurácia + matriz de confusão | Simples e suficiente |
| Classificação desbalanceada | **Precisão, recall, AUC** | Acurácia engana: 95% de acerto prevendo sempre "não" é inútil |
| Regressão | **RMSE ou MAE** + R² | RMSE pune erro grande; MAE é mais legível para o negócio |

**Se você não registrou o valor da métrica:** não invente. Diga o que é verdade:

> "Eu avaliei com [métrica], mas sinceramente não guardei o valor exato e não vou chutar um número aqui. O que eu lembro é a comparação que importava: o modelo batia o baseline de [regra atual / média histórica], e foi isso que sustentou a recomendação."

#### 6. Validação

**Mais provável:** `train_test_split` do scikit-learn, 70/30 ou 80/20.

**Como transformar isso em ponto forte** — assuma a limitação e mostre que sabe o correto:

> "Usei split simples de treino e teste. Hoje, sabendo mais, eu faria diferente em dois pontos: se houvesse ordem temporal no dado, split aleatório vaza futuro no treino e infla a performance — o correto seria corte temporal. E usaria cross-validation em vez de um único split, porque um split só pode ser sorte. É um dos motivos pelos quais eu quero trabalhar com quem já faz isso direito."

☝️ **Este é o melhor movimento disponível neste case.** Você converte uma limitação técnica em demonstração de que entende validação melhor do que executou — que é exatamente a posição honesta de um júnior.

#### 7. Baseline — `a pergunta que separa quem entende de quem só rodou fit()`

**Reconstrua qual era a alternativa ao modelo:**

| Setor | Baseline provável |
|---|---|
| **Saúde** | Média histórica do indicador; regra manual da equipe; ordenação por valor |
| **Transporte** | Média/mediana histórica por rota ou horário; planejamento por experiência do operador |

**Fala forte:**
> "O baseline era [a regra que o cliente já usava]. Isso importa mais que a métrica absoluta, porque mede valor incremental: um modelo com boa acurácia que não bate a regra que já existe não deveria ir para produção."

#### 8. Volume (1,2M registros)
Coberto no item 1. **O ponto de força é o dimensionamento correto, não a complexidade.**

#### 9. O que deu errado — `escolha o real; opções mais prováveis`

- **Qualidade do dado:** campos incompletos, categorias inconsistentes, duplicata por chave mal definida — dominante em base de saúde
- **Definição do alvo:** a primeira definição não era a que o negócio queria
- **Vazamento:** uma variável performava demais porque era consequência do resultado
- **Escopo:** a pergunta inicial mudou no meio

**Se foi qualidade de dado — e em saúde quase sempre é — essa é uma ótima história**, porque descobrir que o dado não sustenta a pergunta é achado legítimo de consultoria.

#### 10. O modelo foi usado?

**Se não foi implantado, diga.** E enquadre:
> "Foi um projeto de clube, com prazo e escopo de clube. Entregamos a análise e a recomendação; não houve implantação em produção. O que eu levei dali foi principalmente a parte de tratamento e de definição do problema, não a de sustentação de modelo."

### Reescrita do bullet 7 — três versões, escolha pela verdade

**Versão A — se você recuperar o detalhe técnico:**
> Estruturei modelos preditivos em Python (`scikit-learn`) e rotinas de extração em SQL para projetos nos setores de Saúde e Transporte, tratando bases com mais de 1,2 milhão de registros, com validação em conjunto de teste separado e comparação contra baseline de [regra vigente] — resultado que subsidiou as recomendações entregues ao cliente.

**Versão B — se você tem o método mas não a métrica:**
> Estruturei rotinas de extração em SQL e modelos preditivos em Python para projetos nos setores de Saúde e Transporte, tratando bases com mais de 1,2 milhão de registros, com feature engineering a partir de hipóteses de negócio e validação contra baseline.

**Versão C — se o trabalho foi mais de tratamento que de modelagem:**
> Estruturei rotinas de extração em SQL e de tratamento em Python para projetos nos setores de Saúde e Transporte, processando bases com mais de 1,2 milhão de registros e produzindo as análises que sustentaram as recomendações entregues ao cliente.

**A Versão C é mais forte que uma Versão A inflada.** Um bullet menor e sólido te dá a entrevista inteira; um bullet grande e oco te dá cinco segundos de triagem e depois te custa a credibilidade.

---

## 9.3 Números de resultado — caminho de recuperação e versão sem número

> Para cada um: onde achar o dado, uma faixa de sanidade **apenas para ancorar sua memória** (não para citar), e a reescrita que funciona sem o número.

### (a) Redução de inadimplência — V4 Company

**Onde recuperar:** relatório de aging de recebíveis antes e depois da implantação; ou o próprio controle diário que você criou; ou o DSO mensal (prazo médio de recebimento).

**Como calcular, se você tiver as bases:**
```
Inadimplência (%)  = saldo vencido acima de N dias / carteira total
DSO (dias)         = (contas a receber / receita do período) × dias do período
Efeito             = média dos 3 meses seguintes − média dos 3 meses anteriores
```

**Faixa de sanidade — só para você reconhecer o número quando vê-lo:** iniciativas de antecipação de cobrança em carteira B2B pequena costumam mover inadimplência em poucos pontos percentuais e DSO em alguns dias. **Se você "lembrar" de uma queda de 60%, desconfie da própria memória.**

**Versão sem número (use esta se não recuperar):**
> "Implantei um controle diário de vencimentos que mudou a cobrança de reativa para antecipada. O mecanismo é direto: cobrança que sai antes do vencimento recupera mais que cobrança que sai depois do atraso. A inadimplência da carteira caiu no período. Não vou te dar um percentual porque eu não tenho a medição controlada para sustentá-lo — e sendo honesto, eu não tinha grupo de controle, então não consigo separar o efeito da minha intervenção de uma mudança de mix ou da conjuntura. O que eu defendo com segurança é a redução do prazo de cobrança, que é o efeito de primeira ordem."

☝️ **Esta é a melhor fala de toda a sua entrevista, e ela não precisa de número nenhum.** Ela demonstra o valor "Rigor Analítico" de um jeito que praticamente nenhum candidato júnior demonstra.

### (b) Redução do ciclo de fechamento — V4 Company

**Onde recuperar:** data de fechamento efetivo por mês, antes e depois. Se o fechamento saía no 10º dia útil e passou ao 6º, o número é isso.

**Versão sem número:**
> "Reestruturei as rotinas de fechamento e a documentação dos controles internos. O ganho principal não foi velocidade, foi **rastreabilidade**: cada lançamento passou a ser rastreável até o comprovante de origem. Quando chegaram a auditoria e a Due Diligence, foi isso que sustentou os números — e é a diferença entre um número defensável e um número frágil."

☝️ **Aqui o número é secundário de verdade.** "Sustentou auditoria e Due Diligence" é validação externa, e vale mais que "reduzi 4 dias".

### (c) Economia recorrente — IME Jr

**Onde recuperar:** comparação da despesa mensal por categoria antes e depois; ou o valor das linhas cortadas.

**Versão sem número:**
> "Categorizei as despesas operacionais, ordenei por materialidade e separei custo estrutural de discricionário. A recomendação de corte gerou economia mensal recorrente — recorrente é a parte que importa, porque foi mudança de patamar, não corte pontual. O aprendizado que eu levei foi outro: **a taxonomia decide o resultado.** Com a categoria errada, o custo problemático fica diluído e invisível."

☝️ O insight sobre taxonomia é mais valioso que o valor economizado — e conecta direto com definição de categoria em *category management*, a oferta nº 1 da ATY.

### (d) Erro de projeção de fluxo de caixa — V4

**Onde recuperar:** se você guardava realizado vs. projetado, calcule:
```
Erro % do mês  = |realizado − projetado| / realizado
MAPE           = média dos erros % dos meses
Viés           = média de (realizado − projetado), com sinal
```
**O sinal importa mais que o tamanho:** erro sempre no mesmo sentido é **viés** (premissa errada, corrigível); erro alternando é **variância** (ruído). Saber essa distinção vale mais que o valor do MAPE.

**Versão sem número:**
> "Eu media realizado contra projetado todo mês, e o desvio virava pergunta, não só registro. Não tenho um MAPE calculado para te dar, porque o objetivo ali era decisão de caixa, não acurácia de modelo. Mas foi olhando o padrão do erro que eu descobri a coisa mais útil: o erro era enviesado num sentido, o que indicava premissa errada e não ruído — eu projetava recebimento pelo prazo contratual em vez do comportamento real de pagamento."

### (e) Horizonte da projeção

**`HIPÓTESE:`** projeção mensal com horizonte de 3 a 12 meses, revisada mensalmente — padrão de gestão financeira de empresa desse porte. Confirme e ajuste.

### (f) Quem passou em processo após sua preparação — Clube de Consultoria

**Onde recuperar:** você conhece as pessoas. Pergunte a duas ou três.

**Isso vale o esforço:** "acompanhei X pessoas que passaram em processo de consultoria" é resultado verificável e humano. Se não tiver, a versão sem número já é forte: **240+ alunos alcançados em três edições** é escala real.

### (g) Alunos que você formou para atender no seu lugar

**Versão sem número (e é a melhor formulação disponível):**
> "Eu orientei os membros mais novos a responderem as dúvidas dos alunos. Foi mais lento no começo e algumas respostas saíram piores que as minhas — mas no fim o clube tinha vários instrutores em vez de um gargalo em mim."

---

## 9.4 As inferências — por que ficam rotuladas, e a pergunta que converte cada uma

> **Não "preencha" inferência.** O rótulo existe para te proteger: se você afirmar como fato algo que eu deduzi, e a pessoa te corrigir, você perde credibilidade por uma informação que nem era sua. Abaixo, o raciocínio de cada uma e a **pergunta** que a transforma em fato durante a conversa — o que é infinitamente mais forte.

| # | Inferência | Base do raciocínio | Pergunta que converte |
|---|---|---|---|
| 1 | **Equipe de 3 a 8 pessoas** | 3 perfis públicos; site com 1 bio; fundação recente | "Como está estruturado o time hoje?" |
| 2 | **Gilberto é sócio-fundador e face comercial** | Única bio no site; e-mail direto `gvolpe@`; LinkedIn ativo | Não pergunte. Apenas trate-o como interlocutor principal. |
| 3 | **Aramis = case de pricing de +7 p.p.** | Aramis é moda masculina premium; case descreve "varejo de moda"; André cita "luxury fashion" | "Vi que a Aramis é cliente. Pelo case de pricing em varejo de moda, imagino que coleção, markdown e sazonalidade apareçam bastante. É assim?" |
| 4 | **Kraft Heinz = market sizing / categoria** | CPG global; case cita "bens de consumo" e projeção de mercado | "Em CPG, o trabalho de vocês entra mais por gestão de categoria no PDV ou por projeção e go-to-market?" |
| 5 | **Vero = telecom/ISP** | Nome compatível com ISP brasileiro; André cita telecom | "Vi a Vero entre os clientes — vocês atuam em telecom também? Imagino que churn e previsão sejam os temas." |
| 6 | **Databricks + dbt + Power BI é o stack padrão** | Declarado no perfil do André | "Qual é o stack padrão de vocês num projeto novo? Vi dbt e Databricks no perfil do André." |
| 7 | **Contratação é para alavancagem júnior** | Nicole entrou 7 meses após os sócios; boutique em crescimento | "Qual é o nível da posição e como ela se encaixa no time hoje?" |
| 8 | **Processo estruturado em 5 fases** (diagnóstico → quantificação → modelagem → validação → implementação) | Reconstrução a partir dos 3 valores e dos cases | Não pergunte — **use** a estrutura ao responder um case. Se for próxima da deles, o efeito é ótimo. |
| 9 | **Maravilhas do Lar tem relação de longo prazo** | Gilberto foi à inauguração da 5ª loja e postou com admiração | "Vi que vocês acompanham a Maravilhas do Lar. Trabalhar com rede em expansão de lojas muda o tipo de problema analítico?" |
| 10 | **Site desatualizado quanto ao time** | André e Nicole no LinkedIn, ausentes no site | **Não comente.** Use a pergunta nº 1. |

---

## 9.5 Plano de recuperação — 90 minutos

| Ordem | Ação | Tempo |
|---|---|---|
| 1 | Procurar o repositório/notebook dos modelos preditivos. Achando o código, os itens 4, 5, 6 e 7 se resolvem em minutos | 30 min |
| 2 | Pedir ao Clube de Consultoria o material dos projetos de Saúde e Transporte | 10 min |
| 3 | Procurar nos seus arquivos da V4 o aging de recebíveis ou o DSO mensal | 20 min |
| 4 | Verificar a data de fechamento antes/depois | 10 min |
| 5 | Perguntar a 2-3 alunos do Prep4Consulting se passaram em algum processo | 10 min |
| 6 | Decidir, para cada bullet, entre a versão com número e a versão sem | 10 min |

**Se nada for recuperável:** use integralmente as versões sem número. Elas são honestas, específicas e — no caso da inadimplência — **mais fortes que a versão com percentual**, porque demonstram o valor central da casa.

---

## 9.6 A regra de ouro, em uma frase

> **Nunca deixe no seu discurso uma afirmação que não sobreviva a três perguntas seguidas de aprofundamento.**

Teste cada número do seu CV assim:
1. "Como você chegou nesse número?"
2. "Comparado com o quê?"
3. "Como você sabe que foi a sua intervenção que causou isso?"

Se a terceira te deixa sem resposta, **você tem duas opções legítimas**: qualificar a afirmação (como na fala da inadimplência) ou removê-la. As duas são melhores que sustentar o número e cair.
