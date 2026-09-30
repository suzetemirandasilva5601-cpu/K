# Parte 11 — Perguntas sobre Ferramentas

> **Por que este documento existe.** Seu CV declara **Excel e VBA, Python, SQL, Power BI**. Tudo que está declarado será testado — é a parte mais fácil de verificar numa entrevista e a que mais derruba candidato. Este documento traz as perguntas prováveis por ferramenta, com respostas no nível que você pode **sustentar honestamente**.

> ### Regra de ouro
> **Nunca declare nível maior que o real.** "Avançado" em Excel promete PROCX, tabela dinâmica, Power Query e função matricial. "Avançado" em Python promete mais do que você provavelmente quer prometer.
>
> Calibragem sugerida para o seu CV:
> - **Excel/VBA:** avançado ✔ (você tem certificação e uso real)
> - **SQL:** intermediário
> - **Python:** intermediário
> - **Power BI:** básico-intermediário
>
> Rebaixar o rótulo custa zero e te protege de tudo. Um entrevistador nunca reprovou ninguém por ter escrito "intermediário" e demonstrado intermediário.

---

## 11.1 O argumento que amarra seu stack — decore este

Há um fato aritmético que explica, de forma perfeitamente defensável, **por que você saiu do Excel para Python e SQL**:

```
Limite de linhas de uma planilha Excel  =  1.048.576
Sua base nos projetos de Saúde/Transporte  >  1.200.000 registros
```

> **"A base não cabia no Excel — 1,2 milhão de linhas passa do limite de pouco mais de um milhão da planilha. Foi literalmente por isso que o trabalho foi para SQL e Python: não era escolha estética, era restrição. No SQL eu filtrava e agregava, e trazia para o Python o que já estava no grão da análise."**

Por que essa fala é forte:
- É **verificável** — qualquer um confere o limite do Excel
- Explica sua transição de ferramenta por **necessidade**, não por moda
- Demonstra que você escolhe ferramenta por restrição do problema — que é exatamente o julgamento que se espera
- E abre para o ponto seguinte: 1,2M linhas **cabe** em pandas, então não precisava de Spark. Dimensionamento correto nas duas direções.

---

## 11.2 Excel e VBA

> Sua ferramenta mais forte. **Não a minimize** — em consultoria, Excel é onde metade do trabalho acontece, e um sócio sabe disso. Mas esteja pronto para o "e quando o Excel não serve?".

### P1. Qual a diferença entre PROCV, ÍNDICE+CORRESP e PROCX?

> "PROCV só procura à direita da coluna de busca e quebra se alguém insere coluna no meio, porque o índice é posicional. ÍNDICE+CORRESP resolve os dois problemas: busca em qualquer direção e referencia a coluna explicitamente, então é robusto a mudança de estrutura. PROCX unifica isso numa função só, com busca bidirecional e tratamento nativo de não-encontrado.
>
> Na prática eu usava ÍNDICE+CORRESP em planilha que outras pessoas iam editar, justamente pela robustez, e PROCV só em coisa descartável."

### P2. Como você somaria valores com múltiplos critérios?

> "`SOMASES` para múltiplos critérios — é o padrão. `SOMARPRODUTO` quando o critério é uma expressão que `SOMASES` não aceita, ou quando preciso multiplicar duas colunas antes de somar, tipo quantidade × preço unitário com filtro. E tabela dinâmica quando a análise é exploratória, porque aí eu quero pivotar e não manter fórmula."

### P3. Quando você usa tabela dinâmica e quando usa fórmula?

> "Tabela dinâmica para explorar e para recortar de várias formas rapidamente. Fórmula quando o resultado tem que ser estável e auditável — relatório que vai para a diretoria todo mês precisa de célula rastreável, e tabela dinâmica se reorganiza e o número muda de lugar.
>
> No fechamento eu preferia fórmula com referência estruturada, porque eu precisava que cada número fosse rastreável até a origem. Isso era requisito de auditoria, não preferência."

### P4. Você usou Power Query?

**Responda com honestidade.** Se usou:
> "Para consolidar arquivos de origens diferentes e padronizar antes da análise — o que antes eu fazia copiando e colando. A vantagem é que a transformação fica registrada em passos, então o próximo mês é só atualizar, e dá para ver o que foi feito."

Se não usou:
> "Não cheguei a usar. Sei que resolve o problema de ETL repetitivo dentro do Excel e é o caminho natural entre planilha e ferramenta de dados de verdade — inclusive é o mesmo conceito de transformação em camadas que o dbt faz no warehouse."

### P5. Quando você escolhe VBA e quando escolhe Python?

> "VBA quando o resultado tem que viver **dentro** da planilha e a pessoa que vai usar só tem Excel — automatizar um relatório recorrente que o time já opera, por exemplo. O custo de tirar alguém do Excel é alto e frequentemente não vale.
>
> Python quando o volume passa do que a planilha aguenta, quando preciso de biblioteca estatística, ou quando quero versionar o código. VBA em arquivo compartilhado vira caixa-preta rápido: ninguém sabe qual versão é a boa."

### P6. Como você trataria uma base grande no Excel?

> "A primeira pergunta é se ela deveria estar no Excel. Acima de algumas centenas de milhares de linhas o arquivo fica instável e o recálculo trava. A saída é agregar antes: trazer do banco já no grão da análise, ou usar Power Query e carregar só o resultado, não a base inteira.
>
> Nos projetos de 1,2 milhão de registros nem havia decisão a tomar: passa do limite de linhas da planilha."

### P7. Como você garante que uma planilha não tem erro?

> "Três coisas que eu fazia no fechamento. Primeira, **reconciliação contra fonte independente** — o total da minha planilha fecha com o que a contabilidade reporta? Se não fecha, nada mais importa. Segunda, célula de verificação: soma de conferência, checagem de que o rateio fecha em 100%, `SE.ERRO` sinalizando em vez de esconder. Terceira, separar entrada de cálculo de saída, para ninguém digitar por cima de fórmula.
>
> Isso é o que virou a base documental que sustentou a auditoria e a Due Diligence: cada número rastreável até o comprovante."

---

## 11.3 SQL

> Aqui você precisa conseguir **escrever**, não só descrever. Se declarou SQL, espere caneta e papel.

### P8. Explique os tipos de JOIN.

> "`INNER` traz só o que casa nas duas tabelas. `LEFT` traz tudo da esquerda e preenche com nulo o que não casou — é o que eu uso quando a tabela da esquerda é a base da análise e eu não quero perder linha. `RIGHT` é o espelho, e na prática eu reescrevo como LEFT invertendo a ordem, porque é mais legível. `FULL` traz tudo dos dois lados.
>
> O erro que mais acontece: usar INNER e perder linha sem perceber. Eu comparo a contagem antes e depois do join. Se mudou e eu não esperava, tem problema — ou de chave ou de premissa."

### P9. Qual a diferença entre WHERE e HAVING?

> "`WHERE` filtra linha antes da agregação; `HAVING` filtra o resultado depois. Então `WHERE` não consegue usar `SUM()` porque a agregação ainda não aconteecu, e `HAVING` é onde eu digo 'só clientes com faturamento acima de X'.
>
> E por performance, sempre que possível eu filtro no `WHERE`: reduzir linha antes de agregar é mais barato que agregar tudo e descartar depois."

### P10. Escreva uma query que traga o top 3 produtos por margem em cada categoria.

```sql
WITH ranqueado AS (
    SELECT
        categoria,
        produto,
        SUM(margem) AS margem_total,
        ROW_NUMBER() OVER (
            PARTITION BY categoria
            ORDER BY SUM(margem) DESC
        ) AS posicao
    FROM vendas
    WHERE data BETWEEN '2026-01-01' AND '2026-12-31'
    GROUP BY categoria, produto
)
SELECT categoria, produto, margem_total, posicao
FROM ranqueado
WHERE posicao <= 3
ORDER BY categoria, posicao;
```

**Explique ao escrever:** "preciso do CTE porque não posso filtrar por `ROW_NUMBER()` no mesmo nível em que ele é calculado — a função de janela é avaliada depois do `WHERE`."

### P11. Diferença entre GROUP BY e window function?

> "`GROUP BY` colapsa linhas: eu perco o detalhe e fico com o agregado. Window function calcula o agregado **e mantém a linha**, então eu consigo ter o valor do produto e o total da categoria na mesma linha — o que é exatamente o que eu preciso para calcular participação.
>
> Na prática, `share = valor / SUM(valor) OVER (PARTITION BY categoria)` resolve em uma linha o que com `GROUP BY` exigiria uma subquery e um join."

### P12. Como você encontraria e trataria duplicatas?

```sql
-- Diagnóstico: a chave é realmente única?
SELECT id_pedido, COUNT(*) AS n
FROM pedidos
GROUP BY id_pedido
HAVING COUNT(*) > 1;
```

> "Primeiro eu diagnostico, não removo. Duplicata geralmente é sintoma: chave mal definida, ou o grão da tabela é diferente do que eu supunha — o 'pedido' duplicado pode ser um pedido com dois itens, e aí não é duplicata, é o grão sendo item e não pedido.
>
> Se for duplicata real, `ROW_NUMBER()` particionado pela chave e ordenado por data de atualização, mantendo a posição 1. Mas antes eu entendo por que existe."

### P13. Como o NULL se comporta?

> "NULL não é zero nem vazio, é ausência de informação, e ele propaga: qualquer operação com NULL dá NULL, e comparação com `=` nunca é verdadeira — tem que ser `IS NULL`. Isso pega gente desprevenida em `WHERE campo <> 'X'`, que **exclui** as linhas com NULL sem avisar.
>
> Em agregação, `COUNT(*)` conta linha e `COUNT(campo)` ignora NULL — diferença que já causou divergência de número que eu tive que investigar. `SUM` e `AVG` também ignoram, e aí a média pode estar sendo calculada sobre uma base menor do que você pensa."

### P14. Uma query está lenta. O que você faz?

> "Não tenho experiência de tuning em produção, então vou pelo que entendo do conceito. Primeiro eu olho o volume: estou trazendo mais linha ou mais coluna do que preciso? `SELECT *` numa tabela larga é desperdício. Segundo, onde está o filtro — filtrar antes de juntar é melhor que juntar tudo e filtrar. Terceiro, se há índice na coluna de join e de filtro, porque sem índice o banco varre a tabela inteira. E função aplicada na coluna dentro do `WHERE` costuma invalidar o índice.
>
> Se fosse aprofundar, eu leria o plano de execução — mas aí já é território em que eu ia precisar de ajuda."

☝️ **Admitir o limite e mostrar o raciocínio correto vale mais que recitar algo decorado.**

---

## 11.4 Python

### P15. Como você carrega e inspeciona uma base nova?

```python
import pandas as pd

df = pd.read_csv("base.csv", sep=";", decimal=",", encoding="utf-8")

df.shape                       # dimensão
df.dtypes                      # tipo por coluna
df.isna().sum()                # nulos por coluna
df.describe()                  # distribuição dos numéricos
df["chave"].duplicated().sum() # a chave é única?
df["categoria"].value_counts() # cardinalidade dos categóricos
```

> "Esse é o meu ritual antes de qualquer análise. `dtypes` pega o problema mais comum em base brasileira, que é número lendo como texto por causa de vírgula decimal e separador de milhar. E `duplicated` na chave testa se o grão da tabela é o que eu acho que é."

### P16. Diferença entre merge e concat?

> "`merge` junta por chave, é o equivalente do JOIN do SQL — e aceita `how='left'`, `'inner'` e assim por diante. `concat` empilha, seja por linha, seja por coluna, sem lógica de chave.
>
> Um cuidado no `merge`: se a chave não for única no lado direito, o resultado multiplica linhas. Eu confiro `shape` antes e depois, e uso `validate='m:1'` quando espero muitos-para-um — aí o pandas levanta erro em vez de silenciosamente duplicar a base."

### P17. Como você agrupa e agrega?

```python
resumo = (
    df.groupby(["categoria", "loja"])
      .agg(
          receita=("valor", "sum"),
          pedidos=("id_pedido", "nunique"),
          ticket=("valor", "mean"),
      )
      .reset_index()
)

# participação dentro da categoria (equivalente a window function)
resumo["share"] = resumo["receita"] / resumo.groupby("categoria")["receita"].transform("sum")
```

> "O `transform` é o análogo da window function do SQL: devolve no formato original em vez de colapsar, então dá para calcular participação sem fazer merge de volta."

### P18. Apply ou operação vetorizada?

> "Vetorizada sempre que possível. `apply` roda linha a linha em Python e é ordens de magnitude mais lento; operação vetorizada desce para implementação otimizada. Em base de milhão de linhas a diferença deixa de ser detalhe.
>
> Para condicional eu uso `np.where` para dois casos e `np.select` para vários, em vez de `apply` com `if`."

### P19. Como você trataria valores faltantes?

> "Primeiro entendendo **por que** falta, porque isso decide o tratamento. Falta aleatória é um problema; falta sistemática é informação — se o campo 'renda' só falta para um tipo de cliente, a ausência é preditiva e eu criaria uma flag em vez de imputar.
>
> Opções: remover linha se for pouca coisa e não enviesar; imputar por mediana em numérico assimétrico, média em simétrico; imputar por moda ou criar categoria 'desconhecido' em categórico. E o cuidado que eu aprendi depois: **imputar usando estatística calculada no treino, não na base inteira** — senão vaza informação do teste para o treino."

### P20. Um pipeline simples de modelagem

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, classification_report

X = df.drop(columns=["alvo"])
y = df["alvo"]

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y   # stratify: preserva a proporção
)

modelo = LogisticRegression(max_iter=1000, class_weight="balanced")
modelo.fit(X_tr, y_tr)

prob = modelo.predict_proba(X_te)[:, 1]
print("AUC:", roc_auc_score(y_te, prob))
print(classification_report(y_te, modelo.predict(X_te)))
```

**Três coisas para comentar ao mostrar isso:**
- `stratify=y` preserva a proporção da classe no split — importante em base desbalanceada
- `class_weight="balanced"` é o primeiro recurso contra desbalanceamento, mais simples que SMOTE e sem distorcer o dado
- `random_state` fixo para o resultado ser reproduzível

### P21. Como você lidaria com uma base que não cabe na memória?

> "1,2 milhão de linhas cabe — então no meu caso eu não precisei. Se não cabendo: primeiro, agregar ou filtrar no banco antes de trazer, que é quase sempre a resposta certa. Depois, ler em `chunksize` e processar por pedaço. Reduzir tipo de dado ajuda bastante — categórico em vez de object, inteiro menor quando a faixa permite. E se nada disso resolve, aí sim é caso de ferramenta distribuída, que é onde entra Spark e Databricks.
>
> Mas eu tento não inventar complexidade: a maioria dos problemas que parecem exigir Spark se resolve com um `GROUP BY` no SQL."

---

## 11.5 Power BI

> Declare **básico-intermediário**. É a ferramenta declarada do André, então pode aparecer.

### P22. Diferença entre medida e coluna calculada?

> "Coluna calculada é materializada linha a linha na tabela, ocupa memória e é calculada no refresh. Medida é calculada na hora, no contexto do visual — filtro, linha, coluna.
>
> A regra prática: **agregação é medida**. Se eu criar 'margem %' como coluna e somar, eu somo percentual, o que não faz sentido. Como medida, `DIVIDE(SUM(margem), SUM(receita))` recalcula corretamente em qualquer nível de agregação."

### P23. O que é contexto de filtro?

> "É o conjunto de filtros ativos quando a medida é avaliada — vindo do visual, do slicer, da linha da matriz. A mesma medida devolve valores diferentes em contextos diferentes, e é isso que faz o Power BI funcionar.
>
> `CALCULATE` é a função que modifica esse contexto, e é onde eu diria que começa o DAX de verdade. Comparar com o ano anterior, por exemplo, é `CALCULATE` com `SAMEPERIODLASTYEAR` alterando o filtro de data."

### P24. Como você modelaria os dados?

> "Esquema estrela: tabela fato no centro com os eventos, dimensões ao redor com os atributos, ligadas por chave. Fato de vendas, dimensões de produto, loja, cliente e calendário.
>
> E tabela calendário dedicada, marcada como tabela de datas — sem ela as funções de inteligência temporal não funcionam direito. Eu aprendi isso do lado financeiro, onde comparação de período é o tempo todo."

### P25. Power Query ou DAX?

> "Power Query para transformar antes de carregar: limpar, tipar, juntar fonte, padronizar. DAX para calcular na hora da análise, em cima do modelo já limpo.
>
> A regra que eu sigo: **o que é estrutural vai o mais cedo possível** — idealmente no SQL, senão no Power Query. DAX resolvendo problema de dado sujo é remendo que fica caro depois."

---

## 11.6 O stack da ATY — Databricks e dbt

> **Você não conhece.** A única resposta que funciona é honestidade + conceito + curva de aprendizado. Blefar aqui é suicídio: André usa as duas no dia a dia.

### P26. Já usou Databricks?

> "Não em cliente. Rodei na Community Edition para não chegar zerado no conceito.
>
> Como eu entendo: é uma plataforma unificada sobre Spark, com notebook, job agendado, Delta Lake dando transação e versionamento sobre o data lake, e MLflow para rastrear experimento e registrar modelo. A organização em camadas — bronze com o dado cru, silver limpo, gold pronto para consumo — é o que chamam de arquitetura medallion.
>
> Sei que a diferença entre isso e operar em produção é grande, e não vou dizer que sei. Mas o vocabulário e a lógica eu tenho."

### P27. Sabe o que é dbt e por que se usa?

> "Sei o conceito e é a peça do stack de vocês que mais me interessou, porque a curva vindo de SQL me parece curta.
>
> É transformação dentro do warehouse com disciplina de engenharia de software: cada transformação é um `SELECT` versionado em Git, organizado em camadas — staging, intermediate, marts —, com testes automatizados de chave única e não-nulo, documentação e lineage.
>
> O que me atraiu tem a ver com a minha experiência: eu resolvi na mão, no fechamento contábil, o problema de rastreabilidade — deixar cada lançamento rastreável até o comprovante. O dbt é a versão madura disso em dados: o lineage mostra exatamente o que quebra quando você muda algo upstream. É o mesmo princípio, com ferramenta de verdade."

☝️ **Esta conexão é o melhor movimento disponível sobre uma ferramenta que você não domina:** você liga um gap técnico a uma experiência real sua, e mostra que entende *por que* a ferramenta existe.

### P28. Qual ferramenta do nosso stack você aprenderia primeiro?

> "dbt, por três razões. É a de curva mais curta para quem vem de SQL, que é o meu caso. É a que estrutura o trabalho de todo mundo — se eu entender a camada de transformação, entendo de onde vem cada número que aparece no Power BI. E é a que mais conversa com o que eu já sei fazer, que é rastreabilidade e controle.
>
> Databricks eu trataria como segundo passo, aprendendo no uso, porque plataforma se aprende operando e não lendo."

---

## 11.7 Versionamento e organização

### P29. Usa Git?

**Se não usa com fluência, diga — e mostre que entende para que serve:**
> "Uso o básico: commit, branch, push. Não tenho rotina de trabalho em equipe com pull request e revisão de código.
>
> Mas eu entendo bem o problema que o Git resolve, porque vivi a versão manual dele: no IME Jr eu padronizei um arquivo em 12 pastas com convenção de nome exatamente porque ninguém sabia qual era a versão boa de cada documento. Git é isso resolvido direito, com histórico e sem 'planilha_final_v3_revisado'."

### P30. Como você organiza um projeto de análise?

> "Separando o que é imutável do que é derivado. Dado bruto nunca é editado — ele é a fonte, e qualquer transformação gera arquivo novo. Script numerado na ordem de execução, para outra pessoa conseguir reproduzir. Saída em pasta separada.
>
> E documentação da decisão de tratamento, porque a escolha de como imputar ou excluir afeta o resultado e quem lê depois precisa saber o que foi feito. Isso é o mesmo princípio dos controles internos que eu documentei na V4."

---

## 11.8 Perguntas de escolha de ferramenta

> Estas são as mais reveladoras, porque testam julgamento e não memória. **Em toda resposta, o critério deve ser a restrição do problema — nunca a sofisticação da ferramenta.**

| Pergunta | Núcleo da resposta |
|---|---|
| **Excel ou Python para esta análise?** | Volume, recorrência e quem vai operar. Análise única que o cliente vai manter → Excel. Recorrente, volumosa ou que precisa versionar → Python |
| **SQL ou Python para transformar?** | O mais perto da fonte possível. Agregação e join no banco; estatística e modelo no Python |
| **Modelo simples ou complexo?** | Interpretabilidade exigida, ganho real medido, e quem mantém. Modelo que o cliente não entende não é usado |
| **Dashboard ou relatório estático?** | Frequência da decisão. Decisão diária → dashboard. Decisão trimestral → relatório, que é mais barato e mais controlado |
| **Precisa de agente de IA?** | Só se o caminho de investigação for ramificado e imprevisível. Se é determinístico, regra é mais barata, mais rápida e auditável |
| **Spark ou pandas?** | Cabe na memória? 1,2M linhas cabe. Não invente distribuído |

**A frase que resume seu critério, e ela é muito vendável numa consultoria:**
> "Eu escolho a ferramenta mais simples que resolve o problema e que o cliente consegue manter depois que eu saio. Solução que só funciona comigo presente não é solução — e vi que 'Solução Duradoura' é um dos valores de vocês, então imagino que a gente pense parecido nisso."

---

## 11.9 Se pedirem para escrever código ao vivo

**Verbalize antes de escrever.** *"Vou fazer em três passos: agregar por categoria, ranquear dentro de cada uma, e filtrar o top 3."* Isso te dá ponto mesmo se o código sair com erro de sintaxe.

**Erros de sintaxe são perdoáveis; erro de lógica não é.** Ninguém decora se é `nunique()` ou `n_unique()`. Mas confundir `WHERE` com `HAVING` mostra que você não entendeu agregação.

**Se travar, diga o que faria:** *"Aqui eu usaria uma window function, mas não lembro a sintaxe exata da cláusula de frame — no trabalho eu consultaria a documentação."* Honestidade > silêncio > invenção.

**Confira o resultado em voz alta.** *"Deixa eu validar: isso deve me devolver no máximo 3 linhas por categoria. Se vier mais, é empate no ranqueamento e eu teria que decidir o critério de desempate."* Essa checagem é mais impressionante que o código.

---

## 11.10 Checklist de 3 horas para não ser pego

| Tempo | O que fazer |
|---|---|
| 30 min | Escrever **à mão**, sem consultar: um JOIN com agregação, um CTE, uma window function com `PARTITION BY` |
| 30 min | Reescrever o pipeline de modelagem da seção 11.4 de memória e explicar cada linha em voz alta |
| 20 min | Revisar seu ritual de inspeção de base em pandas (`shape`, `dtypes`, `isna`, `duplicated`, `value_counts`) |
| 20 min | Decorar a diferença medida × coluna calculada e o que é contexto de filtro no Power BI |
| 20 min | Ler o *dbt Fundamentals* — só a parte de camadas, testes e lineage |
| 20 min | Criar conta na Databricks Community Edition e rodar um notebook, só para poder dizer que rodou |
| 20 min | Ensaiar em voz alta as respostas de gap: Databricks, dbt, Git, tuning de SQL |
| 20 min | **Reler seu CV e confirmar que cada ferramenta declarada tem nível honesto.** Rebaixe o que estiver inflado |

**A última linha é a mais importante da lista.** Todo o resto é otimização; essa é proteção.
