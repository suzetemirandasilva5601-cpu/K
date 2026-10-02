# Frameworks de Case: Varejo

**Quatro estruturas para reproduzir na folha em 60 segundos**

> **Como usar.** Cada framework tem três camadas: a **árvore completa** (para estudar), a **versão de 30 segundos** (o que você realmente desenha na entrevista) e as **perguntas de clarificação** que você faz antes de desenhar.
>
> **Regra de ouro:** nunca desenhe a árvore completa na frente do entrevistador. Desenhe a versão curta, diga por qual ramo vai começar e por quê, e **expanda só o ramo que importa**. Árvore completa demonstra memória; árvore podada demonstra julgamento.

---

# 1. RETAIL PROFITABILITY FRAMEWORK

### Quando usar
"A rentabilidade caiu", "a margem está apertando", "como aumentar o lucro desta rede".

### A árvore completa

```
                              ┌──────────────┐
                              │    LUCRO     │
                              └──────┬───────┘
          ┌──────────────────────────┼──────────────────────────┐
          │                          │                          │
   ┌──────┴──────┐           ┌───────┴───────┐          ┌───────┴───────┐
   │   RECEITA   │           │  CMV / MARGEM │          │    DESPESA    │
   └──────┬──────┘           └───────┬───────┘          └───────┬───────┘
          │                          │                          │
   ┌──────┴──────┐           ┌───────┴───────┐          ┌───────┴───────┐
   │ Nº DE LOJAS │           │ Custo de      │          │ Loja          │
   │     ×       │           │ compra        │          │ (aluguel,     │
   │ RECEITA     │           │               │          │  pessoal,     │
   │ POR LOJA    │           │ Mix de        │          │  energia)     │
   └──────┬──────┘           │ categoria     │          │               │
          │                  │               │          │ Logística     │
          │                  │ Markdown e    │          │ (custo-servir)│
          │                  │ desconto      │          │               │
          │                  │               │          │ Marketing     │
          │                  │ Ruptura e     │          │               │
          │                  │ obsolescência │          │ Overhead      │
          │                  └───────────────┘          └───────────────┘
          │
          ▼
   ┌─────────────────────────────────────────────────┐
   │  RECEITA POR LOJA  =  a cadeia multiplicativa   │
   │                                                 │
   │   TRÁFEGO  ×  CONVERSÃO  ×  TICKET MÉDIO        │
   │  (visitantes)  (% compra)        │              │
   │                                  │              │
   │                        ┌─────────┴─────────┐    │
   │                        │ ITENS POR CESTA   │    │
   │                        │        ×          │    │
   │                        │ PREÇO POR ITEM    │    │
   │                        └───────────────────┘    │
   │                                                 │
   │   × FREQUÊNCIA DE RECOMPRA (se houver cadastro) │
   └─────────────────────────────────────────────────┘
```

### A versão de 30 segundos (desenhe esta)

```
LUCRO = RECEITA − CMV − DESPESA

RECEITA = Nº LOJAS × (TRÁFEGO × CONVERSÃO × TICKET)
                                               │
                                    ITENS × PREÇO

CMV      = custo de compra · mix · markdown · ruptura
DESPESA  = loja · logística · marketing · overhead
```

### Por que o primeiro corte é "nº de lojas × receita por loja"

Porque separa **crescimento por expansão** de **crescimento por produtividade**, e são problemas totalmente diferentes. Uma rede pode crescer receita total abrindo lojas enquanto a venda por loja desaba. Se você não separar, não vê.

> "Antes de atacar receita, eu quero saber se o problema é quantidade de lojas ou produtividade de loja. Vou olhar **venda em mesmas lojas**, porque aí eu isolo o efeito da expansão."

### Perguntas de clarificação

1. "Rentabilidade em valor absoluto ou em margem percentual? Pode cair em percentual e subir em absoluto."
2. "O problema é em todas as lojas ou concentrado em algumas? E em todas as categorias?"
3. "A receita total caiu, ou só a venda em mesmas lojas? Houve abertura ou fechamento no período?"
4. "O horizonte é um trimestre ruim ou uma tendência de dois anos?"

### Métricas que você deve citar

```
Venda em mesmas lojas (SSS)  cresce quanto, isolando expansão
Receita por m²               produtividade do espaço
Margem por m²                melhor que receita por m²
GMROI                        margem bruta ÷ estoque médio
Ruptura (%)                  ocasiões sem o produto
Conversão (%)                compradores ÷ visitantes
UPT                          unidades por transação
```

### A armadilha

**Confundir receita com margem.** Promoção sobe receita e pode destruir lucro. Sempre pergunte qual é a métrica, e quando houver dúvida **olhe margem absoluta**, não percentual nem receita.

**O segundo erro:** analisar no nível de SKU em vez de categoria. O SKU pode melhorar e a categoria piorar por canibalização.

---

# 2. OMNICHANNEL FRAMEWORK

### Quando usar
"Como integrar loja e online", "o e-commerce canibaliza a loja", "devemos unificar estoque e preço".

### A árvore completa

```
                         ┌─────────────────────┐
                         │    OMNICHANNEL      │
                         └──────────┬──────────┘
      ┌──────────────┬──────────────┼──────────────┬──────────────┐
      │              │              │              │              │
┌─────┴─────┐  ┌─────┴─────┐  ┌─────┴─────┐  ┌────┴──────┐       │
│  CLIENTE  │  │  OFERTA   │  │FULFILLMENT│  │ECONÔMICA  │       │
│ (demanda) │  │           │  │ (entrega) │  │           │       │
└─────┬─────┘  └─────┬─────┘  └─────┬─────┘  └────┬──────┘       │
      │              │              │              │              │
 Jornada por    Sortimento:    Ship from      Margem por     ┌────┴─────┐
 canal          igual ou       store          canal          │HABILITA- │
 (descobre      diferente?                                   │  DORES   │
  onde,                        Click &        Custo de       └────┬─────┘
  compra        Preço:         collect        servir              │
  onde)         paridade ou    (BOPIS)        por canal      Visão única
                diferenciado?                                de ESTOQUE
 Cliente                       Troca e        Custo de
 omni vs        Estoque:       devolução      devolução      Visão única
 mono canal     pool único     cross-canal    (crítico       de CLIENTE
 (LTV)          ou separado?                   no online)
                               Last mile                     ATRIBUIÇÃO
 Atrito na                                    Capex de       da venda
 passagem                                     integração     ◄── o ponto
 de canal                                                        cego
                                                             Tecnologia
```

### A versão de 30 segundos (desenhe esta)

```
                 OMNICHANNEL
                      │
   ┌──────────┬───────┼────────┬──────────┐
CLIENTE    OFERTA  ENTREGA  ECONÔMICA  HABILITADOR
   │          │        │         │          │
jornada   sortimento  BOPIS   margem    estoque único
LTV omni  preço       ship    custo     cliente único
atrito    estoque     from    servir    ATRIBUIÇÃO
                      store   devolução tecnologia
```

### O insight que decide o case

**Atribuição de venda é o bloqueio real, e é organizacional, não técnico.**

> "Na prática, o que trava omnichannel quase nunca é tecnologia. É incentivo. Se a loja é avaliada por venda da loja e a venda online atendida por ela não entra na meta dela, o gerente não vai priorizar aquele pedido. Ele vai atender o cliente que está na frente dele, e está certo do ponto de vista dele.
>
> Então antes de discutir integração de sistema eu perguntaria como a venda é creditada hoje. Se o modelo de incentivo não acompanhar, o projeto morre na adoção."

☝️ **Este é o argumento mais forte do framework.** Demonstra que você entende que solução precisa ser adotada, não só construída.

### Perguntas de clarificação

1. "Qual o objetivo: crescer receita total, proteger a loja física, ou melhorar margem?"
2. "Como a venda online é creditada hoje? Entra na meta da loja?"
3. "O estoque é um pool único ou cada canal tem o seu?"
4. "Preço é igual nos dois canais hoje? E o sortimento?"
5. "Tenho visão única de cliente, ou não sei se o comprador online é o mesmo da loja?"

### A conta que importa: margem por canal

```
                        LOJA        ONLINE
Ticket médio            100          100
Margem bruta (%)         55%          55%
Margem bruta (R$)        55           55
(−) Frete                 0          −12
(−) Devolução (×taxa)     −1          −8    ◄ online devolve muito mais
(−) Custo de servir      −20          −6     (moda: 20% a 30%)
                        ────         ────
MARGEM DE CONTRIBUIÇÃO    34           29
```

> "Online costuma ter margem de contribuição menor, não maior, por frete e devolução. O que justifica investir não é a margem do pedido, é o **LTV do cliente omnichannel**, que normalmente é maior porque ele compra mais vezes. Mas isso tem que ser medido, não presumido."

### A armadilha

**Tratar canibalização como perda.** Se o cliente ia comprar na loja e comprou online, a venda não se perdeu, mudou de lugar. A pergunta certa é se a **venda total do cliente** aumentou. Para responder, precisa de visão única de cliente — sem ela, a discussão é opinião.

---

# 3. RETAIL MARKET ENTRY FRAMEWORK

### Quando usar
"Devemos entrar nesta categoria", "vale abrir em outro estado", "entramos sozinhos ou compramos alguém".

### A árvore completa

```
                        ┌────────────────────────┐
                        │   ENTRAR OU NÃO?       │
                        └───────────┬────────────┘
         ┌─────────────┬────────────┼────────────┬─────────────┐
         │             │            │            │             │
    ┌────┴─────┐  ┌────┴─────┐ ┌────┴─────┐ ┌───┴──────┐      │
    │ 1        │  │ 2        │ │ 3        │ │ 4        │      │
    │ MERCADO  │  │ NÓS      │ │ COMO     │ │ VALE A   │      │
    │ É BOM?   │  │ GANHAMOS?│ │ ENTRAR?  │ │ PENA?    │      │
    └────┬─────┘  └────┬─────┘ └────┬─────┘ └───┬──────┘      │
         │             │            │           │             │
  Tamanho e      Direito de     Orgânico    Investimento  ┌───┴────┐
  crescimento    atuar          (loja       (capex por    │ RISCO  │
                 (marca,        própria)     loja +       └───┬────┘
  Rentabilidade  sortimento,                 estoque)         │
  típica         know-how)      Aquisição                 Cenário
                                             Curva de     pessimista
  Concorrência   Vantagem de    Franquia /   maturação
  (fragmentado   custo          parceria     da loja      Reversi-
   ou concen-    (escala,                                 bilidade
   trado?)       logística)     Digital      Payback e    (contrato
                                first        ponto de     de aluguel
  Barreira de    Acesso a                    equilíbrio   é longo)
  entrada        ponto e                                  
                 fornecedor     Teste em     CANIBALI-    Resposta do
  Por que        (no varejo,    1 praça      ZAÇÃO da     concorrente
  ninguém já     o ponto é a    antes        rede atual
  faz?           barreira)                   ◄── o erro
                                              mais comum
```

### A versão de 30 segundos (desenhe esta)

```
  ENTRAR?
     │
  ┌──┴───┬────────┬─────────┬────────┐
MERCADO  NÓS     COMO      VALE?    RISCO
é bom?  ganhamos? entrar?   
  │       │        │         │        │
tamanho  marca   orgânico  capex   pessimista
cresce   custo   M&A       payback reversível
margem   ponto   franquia  curva   concorrente
concorr. acesso  digital   CANIBAL.
```

### Os dois conceitos específicos de varejo

**1. Curva de maturação da loja** — loja nova não atinge regime no dia 1.

```
% da venda em regime
100% ┤                    ╭──────────────
     │              ╭─────╯
 75% ┤        ╭─────╯
     │    ╭───╯
 50% ┤ ╭──╯
     │╭╯
  0% ┼──────────────────────────────────
     0    6    12   18   24   meses
```
> "Projetar a loja nova com a venda média da rede desde o primeiro mês superestima o retorno e encurta o payback artificialmente. Em varejo a maturação costuma levar de 12 a 24 meses, então a conta tem que ser feita com a curva, não com a média."

**2. Canibalização** — abrir perto de loja existente transfere venda.

```
Venda da loja nova         = 100
(−) transferida da rede    = −30   (premissa a medir, não a chutar)
                             ────
Venda INCREMENTAL          =  70

→ O payback se calcula sobre 70, não sobre 100.
```

### A conta de viabilidade de uma loja

```
INVESTIMENTO
  Obra e equipamento                 R$ 600 mil
  Estoque inicial                    R$ 400 mil
                                     ──────────
  Capex total                        R$ 1,0 M

RETORNO ANUAL (em regime)
  Receita                            R$ 4,0 M
  Margem bruta (55%)                 R$ 2,2 M
  (−) despesa da loja                R$ 1,6 M
                                     ──────────
  Contribuição                       R$ 600 mil/ano

  (−) canibalização 30%              R$ 420 mil/ano incrementais

PAYBACK  =  1,0 M ÷ 420 mil  ≈  2,4 anos
           (e some ~1 ano de maturação → ~3,4 anos na prática)
```

### Perguntas de clarificação

1. "O objetivo é crescimento de receita, de lucro, ou defesa de posição contra um concorrente?"
2. "Qual o horizonte e qual o retorno mínimo exigido?"
3. "Existe restrição de capital, ou de capacidade de execução (quantas lojas por ano conseguem abrir)?"
4. "A marca já é conhecida nessa praça? Tem base de cliente ou é entrada a frio?"
5. "O que exatamente a empresa traz que o incumbente não tem?"

### A armadilha

**Responder "o mercado é grande" como se fosse a resposta.** Mercado grande e rentável atrai concorrência; se ninguém entrou ainda, tem motivo. Sempre pergunte **"por que ninguém já faz isso?"** e **"o que nos dá direito de ganhar aqui?"**. Sem resposta para a segunda, o tamanho do mercado é irrelevante.

---

# 4. RETAIL MARKET SIZING FRAMEWORK

### Quando usar
"Qual o tamanho do mercado de X", "quanto podemos vender", "dimensione a oportunidade".

### A estrutura: dois caminhos que se conferem

```
┌─────────────────────────────────────────────────────────────────┐
│                     TAMANHO DE MERCADO                          │
└───────────────────────────┬─────────────────────────────────────┘
          ┌─────────────────┴─────────────────┐
          │                                   │
┌─────────┴──────────┐              ┌─────────┴──────────┐
│    BOTTOM-UP       │              │     TOP-DOWN       │
│ (prefira este)     │              │   (use para        │
│                    │              │    conferir)       │
├────────────────────┤              ├────────────────────┤
│ População          │              │ Varejo total       │
│  ou domicílios     │              │  (ou PIB)          │
│      ×             │              │      ×             │
│ PENETRAÇÃO         │              │ % da categoria     │
│ (% que consome)    │              │      ×             │
│      ×             │              │ % do segmento      │
│ FREQUÊNCIA         │              │   endereçável      │
│ (vezes por ano)    │              │      =             │
│      ×             │              │   MERCADO          │
│ TICKET             │              │                    │
│ (R$ por compra)    │              │                    │
│      =             │              │                    │
│   MERCADO          │              │                    │
└─────────┬──────────┘              └─────────┬──────────┘
          └─────────────────┬─────────────────┘
                            ▼
              ┌──────────────────────────────┐
              │        RECONCILIAR           │
              │  diferença > 2x ⇒ premissa   │
              │  errada em algum dos dois    │
              └──────────────────────────────┘
```

### O funil de mercado (sempre explicite qual você está medindo)

```
┌────────────────────────────────────────────────────┐
│ TAM  Mercado total          todo mundo, todo canal │
│  │                                                 │
│  ▼   filtra geografia, canal, faixa de renda       │
│ SAM  Endereçável            quem eu consigo servir │
│  │                                                 │
│  ▼   filtra share realista no horizonte            │
│ SOM  Capturável             o que eu levo em N anos│
└────────────────────────────────────────────────────┘
```

### A versão de 30 segundos (desenhe esta)

```
MERCADO = DOMICÍLIOS × PENETRAÇÃO × FREQUÊNCIA × TICKET
              75 mi        %          x/ano        R$

CONFERIR por cima:  varejo 2 tri × % categoria

SANIDADE:  resultado ÷ população = R$/pessoa/ano → faz sentido?

TAM → SAM → SOM
```

### Âncoras do Brasil para conta de cabeça

```
População            ~215 milhões
Domicílios            ~75 milhões   (~2,8 pessoas cada)
População urbana          ~87%
Classes            AB ~20% · C ~50% · DE ~30%
PIB                   ~R$ 12 trilhões
Varejo (restrito)      ~R$ 2 trilhões
São Paulo        cidade ~12 mi · estado ~46 mi
```

### Exemplo completo, em 5 linhas

```
Mercado de ketchup no varejo brasileiro

  75 mi domicílios
  × 45% de penetração        =  34 mi domicílios consumidores
  × 0,5 frasco/mês × 12      =  204 mi frascos/ano
  × R$ 12 por frasco         =  R$ 2,45 bilhões/ano

  + food service (~30% do total)  →  ~R$ 3,5 bi

SANIDADE 1:  2,45 bi ÷ 215 mi  =  R$ 11/pessoa/ano  ✓ plausível
SANIDADE 2:  3,5 bi ÷ 2 tri    =  0,18% do varejo   ✓ plausível
```

### Perguntas de clarificação

1. "Mercado em valor ou em volume?"
2. "A preço de consumidor ou a preço de fabricante? A diferença é grande."
3. "Inclui food service e canal institucional, ou só varejo para consumo doméstico?"
4. "Geografia: Brasil todo, ou uma região?"
5. "Quer o mercado total ou o endereçável pelo cliente?"

### A armadilha

**Falsa precisão.** "R$ 2.447.328.000" quando a penetração é um chute vale menos que "da ordem de R$ 2,5 bilhões". Sempre termine declarando a premissa mais frágil:

> "Da ordem de R$ 2,5 bilhões no varejo. A premissa mais frágil é a penetração, que eu estimei em 45%. Se ela fosse 60%, o resultado subiria um terço. Para validar, eu usaria dado de painel de domicílio ou de retail measurement."

**O segundo erro:** não fazer teste de sanidade. Sempre divida por população ou compare com um agregado conhecido.

---

# FOLHA DE REFERÊNCIA

### Qual framework usar

| O enunciado diz | Use |
|---|---|
| "margem caiu", "como aumentar o lucro" | **Profitability** |
| "integrar loja e online", "e-commerce canibaliza" | **Omnichannel** |
| "entrar em", "abrir em outro estado", "comprar player" | **Market Entry** |
| "qual o tamanho", "quanto podemos vender" | **Market Sizing** |

**Combinações frequentes:** Market Entry quase sempre exige **Sizing** dentro dele (no ramo "mercado é bom?"), e termina numa conta de **Profitability** por loja.

### As 4 árvores, lado a lado

```
PROFITABILITY            OMNICHANNEL           MARKET ENTRY         SIZING
                                                                     
LUCRO                    OMNI                  ENTRAR?              MERCADO
├ RECEITA                ├ CLIENTE             ├ mercado é bom?     ├ BOTTOM-UP
│ └ lojas × (tráfego     ├ OFERTA              ├ nós ganhamos?      │ dom × pen
│    × conv × ticket)    ├ ENTREGA             ├ como entrar?       │ × freq
├ CMV                    ├ ECONÔMICA           ├ vale a pena?       │ × ticket
│ └ compra, mix,         └ HABILITADOR         └ risco              └ TOP-DOWN
│    markdown, ruptura     (atribuição!)         (canibalização!)     varejo × %
└ DESPESA                                                            
  loja, log, mkt, OH                                               → reconciliar
```

### A sequência de condução, qualquer que seja o framework

```
1. CLARIFICAR     4 a 6 perguntas. Inclua sempre: "que dado existe?"
2. ESTRUTURAR     desenhe a versão curta. Diga por onde começa E POR QUÊ
3. DIMENSIONAR    números redondos, verbalize a conta, teste de sanidade
4. BRAINSTORM     alavancas em grupos, priorize por impacto × esforço
5. SINTETIZAR     recomendação → número → risco → próximo passo
```

### Os 5 erros que derrubam

```
✗ Desenhar a árvore completa e não escolher um ramo
✗ Confundir receita com margem
✗ Não perguntar que dado existe
✗ Falsa precisão (número exato em cima de premissa chutada)
✗ Não fazer teste de sanidade no resultado
```

### Template em branco, para treinar

```
            ┌──────────────────┐
            │                  │   ← a métrica-objetivo
            └────────┬─────────┘
       ┌─────────────┼─────────────┐
   ┌───┴───┐     ┌───┴───┐     ┌───┴───┐
   │       │     │       │     │       │   ← 3 a 4 ramos MECE
   └───┬───┘     └───┬───┘     └───┬───┘
       │             │             │
    ───────       ───────       ───────
    ───────       ───────       ───────   ← drivers de cada ramo
    ───────       ───────       ───────

  Começo por: ______________  porque: ______________________
  Premissa mais frágil: _________________________________
  Teste de sanidade: ____________________________________
```
