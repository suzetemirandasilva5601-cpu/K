# Abertura da base NYC — Pontos a levantar, insights e perguntas

> Material de trabalho para você aprofundar a visão da operação. Tudo ancorado no que foi
> dito na reunião do dia 27/10 e no checklist. Dividido em: (1) insights que você pode
> trazer, (2) pontos/tensões a levantar, (3) perguntas por área, (4) os ângulos que
> ninguém puxou na reunião.

---

## 1. Insights que você pode trazer (leitura que agrega)

**I1 — O projeto está misturando duas coisas: abrir UMA base e criar o PADRÃO de abrir
bases.** A reunião oscilou o tempo todo entre "resolver o JFK" e "criar o SOP de abertura
de station". São entregáveis diferentes com donos e prazos diferentes. Separar os dois
evita que a urgência do JFK (1º embarque em novembro) atropele a construção do padrão
replicável — que é o ativo de maior valor no longo prazo. **Esse é o insight mais
estratégico: o JFK é o piloto; o produto é o método.**

**I2 — A escolha do parceiro está criando um trade-off de indústria que não foi
explicitado.** O CCSF é forte em aerospace mas não tem área refrigerada para healthcare.
Isso significa que **a escolha do parceiro define, na prática, qual indústria a base
atende primeiro** — e healthcare pode exigir um segundo parceiro ou uma estrutura
diferente. A decisão "qual parceiro" é, disfarçada, uma decisão "qual carga". Vale tornar
isso explícito.

**I3 — O gargalo real é interdependência, não lista de tarefas.** O Possidônio já intuiu
("quase um Gantt"). O TSA tem prazo próprio que trava o go-live; a SOP depende da visita;
o cadastro de pagamento depende da qualificação. Uma lista de checklist esconde isso. Um
diagrama de dependências mostra que a data do 1º embarque **não é uma escolha, é uma
consequência** do caminho crítico (provavelmente o TSA).

**I4 — A operacionalização no sistema é um ponto cego.** O próprio Possidônio disse "não
sei nem como que operacionaliza isso no sistema". Abrir a base fisicamente é uma coisa;
fazer o sistema reconhecer JFK como origem, com buying/selling charge, SOP clonada e
cadastro de pagamento, é outra — e ninguém assumiu isso. É onde um AOG real pode travar
no dia do teste.

**I4b — "Cargas que descem para Miami e podem subir para JFK" é uma tese de volume ainda
não quantificada.** A lógica existe (aerospace/healthcare do norte dos EUA), mas não
apareceu número: quantos embarques/mês, qual volume, qual faturamento. Sem isso, não dá
para dimensionar o analista nem justificar a base economicamente.

---

## 2. Pontos / tensões a levantar (apareceram e ficaram soltos)

**P1 — Homologação dupla de indústria é rara.** O Filipe foi direto: "é muito difícil ter
num custo competitivo alguém homologado nas duas indústrias". Ou seja, querer aerospace +
healthcare no mesmo parceiro pode ser inviável. Levantar: começamos só com aerospace e
tratamos healthcare como fase 2 com outro parceiro?

**P2 — O parceiro "não quis se desqualificar".** O Leonardo notou que o CCSF evitou se
comprometer com refrigeração para não reprovar na homologação. Isso é um sinal amarelo:
há risco de o parceiro aceitar escopo que não consegue cumprir. A visita do Tiago precisa
testar capacidade real, não declarada.

**P3 — O prazo está invertido.** Fala-se em "1º embarque em novembro" e "fechar tudo até
sexta", mas o Possidônio reconheceu que "talvez a conclusão seja dezembro" por causa do
TSA. A tensão: a data foi combinada com Zé e Fernando antes de mapear as dependências.
Levantar: a data é meta ou compromisso? Se o TSA atrasar, o que acontece?

**P4 — Donos órfãos.** Três itens sem responsável fechado: quem cadastra o parceiro no
pagamento, quem responde pela comunicação (TMT ou operação?), e quem faz o template de
faturamento. Em abertura de base, item sem dono = item que não acontece.

**P5 — Visto do Leonardo (RD) para os EUA.** Ele mencionou ter problema de visto. Se o RD
não consegue ir aos EUA homologar presencialmente, isso muda quem faz a validação local
e cria dependência do Tiago. Pequeno, mas é um ponto de operação real.

**P6 — Benchmark de concorrência não tem dono.** O João Rodrigues pediu para o Tiago
"identificar transportadoras e agentes rodando na região para benchmark", mas isso não
virou ação com entregável. Oportunidade perdida se não for registrado.

---

## 3. Perguntas relevantes por área (para a próxima reunião)

### Carga e volume (Produto / RD)
- Quantos embarques/mês de aerospace hoje passam por Miami e migrariam para JFK?
- Qual o faturamento e a margem estimados da 1ª onda?
- Healthcare entra quando — e com qual parceiro, dado que o CCSF não tem refrigeração?
- Além de aerospace e healthcare, há energy ou outra vertical com volume na região norte?

### Parceiro e estrutura (RD / Operação)
- O CCSF está homologado em aerospace de fato, ou só declarou? (a visita confirma?)
- Qual a capacidade de pico do parceiro para AOG (velocidade que Miami já exige)?
- Existe plano B de parceiro se a visita reprovar a estrutura?
- O contêiner refrigerado do parceiro atende que tamanho de carga?

### Sistema e processo (Operação / Qualidade)
- Como JFK é cadastrada no sistema como origem (buying/selling charge)?
- A SOP default de Houston está pronta para clonar hoje?
- Quem cria a SOP de abertura de station — Operação, Qualidade ou CAN?
- Qual o SLA de informação com o parceiro (pré-alerta, warehouse receipt, CCT, pesagem)?

### Prazo e governança (todos)
- Qual a data real de resposta do TSA — e ela é o caminho crítico?
- A data do 1º embarque é meta ou compromisso firmado com Zé/Fernando?
- Quem é o dono único de cada item órfão (cadastro, comunicação, faturamento)?
- Em que momento o RH entra (contratação do analista)? — pergunta que o Filipe já fez

### Financeiro e regulatório
- Como o pagamento ao parceiro no exterior é contabilizado (spread cambial, prepaid)?
- Há custo de overtime/fim de semana no parceiro que muda a conta de AOG?
- Quais requisitos regulatórios de exportação por indústria em JFK (além do TSA)?

---

## 4. Os ângulos que NINGUÉM puxou na reunião (seu diferencial)

**A1 — Qual o critério de SUCESSO da base?** Discutiu-se muito o "como abrir" e quase nada
o "como saber se deu certo". Propor métricas de go/no-go pós-abertura: % AOG no prazo,
volume migrado vs. previsto, margem realizada, custo por embarque JFK vs. Miami.

**A2 — Qual o custo de abrir vs. o ganho de migrar?** Ninguém colocou o caso econômico.
Se a carga já roda por Miami, qual a economia real de subir para JFK (frete, tempo, AOG)?
A base se paga? Esse é o número que falta para a decisão ser sólida — igual ao que fizemos
no projeto Ásia.

**A3 — Reversibilidade.** Se a base não performar, qual o custo de fechar? Como é parceria
(não entidade), deveria ser barato — mas isso precisa estar no acordo (aviso prévio, o que
acontece com o volume migrado). Mesmo princípio da China.

**A4 — O que o JFK tira de Miami?** Migrar carga de Miami para JFK pode desidratar a
station de Miami. Há impacto no dimensionamento de Houston/Miami? É um sistema de vasos
comunicantes, não uma adição isolada.

**A5 — Comunicação ao mercado como alavanca comercial, não só aviso.** O Possidônio tratou
a comunicação como "sair no radar de embarque". Mas abrir JFK é também um argumento
comercial (saída direta para aerospace) — pode ser usado pelos KAMs para ganhar conta, não
só como comunicado. Conecta com a estrutura de KAM que o Gilberto descreveu.

---

## 5. Como usar isto na prática
- **Para a próxima reunião:** leve a seção 3 (perguntas por área) como pauta — força cada
  dono a responder.
- **Para o Possidônio:** leve o I3 (Gantt de interdependências) e o P3 (data é meta ou
  compromisso?) — é o que ele mesmo intuiu e vai valorizar.
- **Para o Zé/Fernando:** leve a seção 4 (caso econômico, critério de sucesso,
  reversibilidade) — é a visão de board que eleva a conversa de "abrir a base" para
  "investir numa base com retorno medido".
