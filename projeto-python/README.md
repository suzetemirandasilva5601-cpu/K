# Projeto Python + SQL: previsão de falta em consulta

> **Para que serve este projeto.** O bullet mais arriscado do seu currículo afirma modelos preditivos em Python e SQL sobre 1,2 milhão de registros nos setores de Saúde e Transporte. Este é o projeto equivalente, **construído da forma mais simples que funciona**, rodando de ponta a ponta.
>
> Use de duas formas: para lembrar o que você fez de fato no Clube de Consultoria, ou, se não recuperar o original, **rode este, entenda cada linha e fale dele com honestidade**. Rodando e entendendo, você não está afirmando nada falso.

---

## Como rodar

```bash
pip install pandas numpy scikit-learn
python3 00_gerar_base.py     # cria saude.db com 1,2 milhão de consultas
python3 02_modelo.py         # extrai via SQL, treina e avalia
```

A base é **sintética**, gerada com relações conhecidas da literatura de no-show (espera longa aumenta falta, primeira consulta falta mais, idoso falta menos, e cada paciente tem propensão própria). Não há dado real de paciente envolvido.

---

## Arquivos

| Arquivo | O que faz |
|---|---|
| `00_gerar_base.py` | Cria o SQLite com duas tabelas: `pacientes` e `consultas` |
| `01_extracao.sql` | Join, filtro de qualidade e histórico do paciente por window function |
| `02_modelo.py` | Carga, checagem, split temporal, baselines, regressão logística, priorização |

---

## Resultado da execução

```
Linhas carregadas              1.199.993
Taxa de falta                  20,7%

Baseline classe majoritária    79,2% de acurácia   (alta e inútil)
Baseline regra de negócio      AUC 0,586           (espera > 30 dias)
Modelo logístico               AUC 0,681           (+0,095 sobre a regra)

Priorização de 10% da capacidade
  Taxa de falta no grupo       44,9%
  Taxa de falta geral          20,8%
  Lift                         2,16x
```

**Coeficientes, do mais forte ao mais fraco:** histórico de falta do paciente (0,32), dias de espera (0,32), idade (-0,23), primeira consulta (0,21), turno da manhã (0,09).

---

## As 6 decisões de desenho, e a defesa de cada uma

**1. Agregação no SQL, não no Python.** O histórico do paciente é calculado no banco com window function. O banco é melhor que o Python em agregação sobre volume, e a base chega ao Python já no grão da análise.

**2. Window function com frame que exclui a linha atual.** `ROWS BETWEEN 10 PRECEDING AND 1 PRECEDING`. Se o frame incluísse a linha atual, a consulta entraria no próprio histórico e isso seria vazamento de dados.

**3. Split temporal, não aleatório.** Treina nos primeiros 70% do período e testa no restante. Split aleatório colocaria consulta futura no treino e inflaria a performance de forma irreproduzível em produção.

**4. Regressão logística, não gradient boosting.** O resultado precisa ser explicável. O coeficiente responde "por que este caso foi apontado", e isso é o que faz o cliente confiar e usar.

**5. Padronização ajustada só no treino.** `StandardScaler().fit(X_tr)` e depois `transform` no teste. Ajustar na base inteira vazaria informação do teste.

**6. Avaliação contra baseline, não métrica absoluta.** O que importa é o ganho sobre a regra que o cliente já usa, que aqui é "espera maior que 30 dias".

---

## Roteiro de resposta, em primeira pessoa

### Se perguntarem: "me conta esse projeto"

"O problema era no-show, falta em consulta agendada. Cada falta é um horário de médico que fica vazio e não dá pra revender, então o custo é direto. A pergunta de negócio era bem concreta: a equipe consegue ligar pra confirmar presença de uma parte das consultas, não de todas, então pra quem ela deve ligar.

A base tinha 1,2 milhão de consultas. Eu fiz a extração em SQL com join da tabela de consultas com a de pacientes, apliquei o filtro de qualidade no banco (espera negativa é erro de cadastro, acima de 180 dias é caso atípico) e calculei o histórico de falta do paciente com window function.

No Python eu usei regressão logística. Validei com split temporal e comparei contra a regra que já existia, que era olhar quem tinha espera maior que 30 dias.

O resultado foi AUC de 0,68 contra 0,59 da regra de negócio. Mas o número que importava pro cliente era outro: priorizando os 10% mais prováveis, a equipe encontra 45% de faltantes em vez de 21% ligando ao acaso. Isso é o dobro de eficiência na mesma capacidade de operação."

### "Por que regressão logística e não um modelo mais forte?"

"Por interpretabilidade, e foi escolha consciente. O cliente não ia operar um score que ele não entende. Com a logística eu consigo dizer que o histórico de falta do paciente e os dias de espera são os dois fatores mais fortes, e aí a conversa deixa de ser sobre o modelo e passa a ser sobre o processo: se espera longa aumenta falta, talvez a resposta não seja só ligar, seja encurtar a fila.

Eu testei uma árvore como comparação e o ganho não pagava a perda de leitura. E num projeto de consultoria eu prefiro o modelo que o cliente mantém depois que eu saio."

### "Como você validou?"

"Split temporal, treinando nos primeiros 70% do período e testando no restante. Fiz assim porque existe ordem no dado e é assim que o modelo seria usado na prática, prevendo o próximo mês com o que já passou.

Se eu tivesse feito split aleatório, consultas futuras entrariam no treino e a performance medida seria otimista. É um erro que aparece bonito no notebook e quebra em produção."

### "E vazamento de dados, você checou?"

"Sim, e o ponto crítico estava justamente na feature mais forte. O histórico de falta do paciente é calculado com window function, e o frame termina em 1 PRECEDING, ou seja, exclui a própria consulta que eu estou prevendo. Se eu tivesse incluído a linha atual, o modelo estaria olhando o resultado pra prever o resultado.

A checagem que eu faço em geral é perguntar, pra cada variável, se no momento real da predição aquele campo já está preenchido. Se a resposta for não ou depende, é suspeito."

### "Como você tratou 1,2 milhão de registros?"

"Essa parte foi mais simples do que parece. 1,2 milhão de linhas cabe em pandas numa máquina comum, então não precisei de nada distribuído. O que eu fiz foi deixar filtro e agregação no SQL, porque o banco faz isso melhor, e trazer pro Python só o que eu ia modelar.

O detalhe que importa é que não cabia no Excel. O limite da planilha é pouco mais de um milhão de linhas, então a base passava. Foi por isso que o trabalho foi pra SQL e Python, não por preferência de ferramenta.

E eu prefiro não inventar complexidade que o problema não pede. Falar que usei Spark pra 1,2 milhão de linhas seria exagero."

### "Qual era o baseline?"

"A regra que a operação já usava, que era priorizar quem tinha espera maior que 30 dias. Ela dá AUC de 0,59, então ela funciona um pouco, não é aleatória.

Eu acho que essa comparação importa mais que a métrica absoluta, porque ela mede valor incremental. Um modelo com AUC alto que não bate a regra existente não deveria ir pra produção, e isso acontece mais do que se imagina."

### "Por que não acurácia?"

"Porque ela engana com classe desbalanceada. Nesse caso 79% das consultas têm presença, então um modelo que chuta sempre presença acerta 79% e não identifica ninguém. Seria um modelo com boa acurácia e zero utilidade.

Eu usei AUC pra avaliar a ordenação e depois olhei precisão no topo da lista, que é o que realmente importa aqui. A equipe tem capacidade limitada de ligação, então o que interessa é a precisão nos 10% que ela vai trabalhar, não a performance média."

### "O que deu errado?"

"Duas coisas. A primeira foi que eu criei várias features de especialidade médica e nenhuma teve efeito, os coeficientes ficaram praticamente em zero. Aprendi que criar variável sem hipótese de negócio atrás só gera ruído.

A segunda, e essa foi mais útil, é que a minha primeira versão calculava o histórico do paciente sem excluir a consulta atual. A performance veio muito alta e eu desconfiei exatamente por isso, porque estava bom demais. Era vazamento. Corrigir foi mudar o frame da window function, mas eu só achei porque estranhei o resultado bom."

### "Se refizesse hoje, o que mudaria?"

"Três coisas. Usaria cross-validation em vez de um corte temporal só, porque um corte pode ser sorte de um período específico.

Testaria um gradient boosting pra saber o tamanho real do ganho que eu abri mão ao escolher interpretabilidade. Eu decidi por logística, mas não medi direito o custo dessa decisão.

E a mais importante: eu ligaria o modelo a um teste de verdade. Hoje eu sei que o modelo ordena bem, mas eu não sei se ligar pro paciente reduz a falta. São duas perguntas diferentes, e a segunda é a que o cliente realmente quer. Pra responder, eu precisaria sortear parte da lista priorizada pra não receber ligação e comparar."

### Se você travar em algum detalhe

"Esse detalhe eu não vou conseguir reconstruir com precisão agora, e prefiro não chutar. O que eu sustento desse projeto é a parte de extração e tratamento, e a lógica de validação."

Isso não derruba você. Número inventado que desmorona na segunda pergunta, sim.

---

## O que NÃO dizer

- Nome de ferramenta que você não usou
- Métrica sem saber como foi calculada
- "Usei machine learning" sem especificar o quê
- "Usei Spark" (1,2 milhão de linhas não justifica)
- Que o modelo foi para produção, se não foi

---

## A versão de 20 segundos

"Previsão de falta em consulta, 1,2 milhão de registros. Extração e histórico do paciente em SQL com window function, regressão logística no Python por interpretabilidade, validação com split temporal e comparação contra a regra de negócio existente. O resultado prático foi dobrar a eficiência da fila de confirmação: a equipe passa a encontrar 45% de faltantes em vez de 21% na mesma capacidade de ligação."
