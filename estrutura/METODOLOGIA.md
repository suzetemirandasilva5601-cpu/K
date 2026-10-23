# Metodologia — como a estrutura foi montada e conferida

Documento de rastreabilidade. Cada número nos outros arquivos sai de um dos passos
abaixo, e cada passo diz exatamente de onde o dado veio.

**Arquivos gerados**

| Arquivo | Conteúdo |
|---|---|
| `Gestores_por_Level.md` | um bloco por level, com os gestores e quem cada um administra |
| `Gestores_por_Level.xlsx` | `Quem reporta a quem`, `Resumo por level`, uma aba por level e a aba `Divergencias` |
| `cross_check.py` | leitura das bases, dados lidos do draft e as rotinas de conferência |
| `gestores_por_level.py` | gera o `.md` e o `.xlsx` |

**Fontes usadas**

| Arquivo | Aba | Data de referência | Para que serviu |
|---|---|---|---|
| `Colaboradores-factorial (3).xlsx` | `level 4` a `level 8` | out/26, com admissões até 16/nov | hierarquia: quem reporta a quem |
| `Draft 23 Out 26.pptx` | 75 slides, 65 imagens | print anterior a 23/out | cargos do topo, caixas azuis, X e anotações |
| `Base_Setembro26 (1).xlsx` | `Setembro Unificado` | competência Set/26 | folha fechada: situação e tipo de custo |
| `Baseline DRE 26.2.xlsx` | `Baseline ativos agosto` | ativos de agosto | custo por pessoa e C-LEVEL |
| `Vagas 21-10.xlsx` | `Vagas` | 21/out | explicar as admissões recentes |

---

## Passo 1 — Entender o formato da planilha do Factorial

A planilha não tem uma coluna de "gestor". Ela tem **uma aba por level**, e em cada
aba duas colunas de gestor:

```
aba 'level 4':  [Nível de gerente 2] [Nível de gerente 3] [Nome] [Sobrenome] [Função] ...
aba 'level 5':  [Nível de gerente 3] [Nível de gerente 4] [Nome] [Sobrenome] [Função] ...
```

Logo: **a pessoa da linha está no level da aba, e a coluna B é o gestor direto dela.**
A coluna A é o gestor do gestor.

As colunas A e B vêm **em células mescladas** — um nome vale para todo o bloco de
linhas abaixo dele. Confirmei isso lendo os intervalos de merge da aba `level 4`:

```
A3:A35   B3:B7   B8:B9   B10:B16   B17:B24   B25:B30   B31:B35
```

Por isso a leitura faz *forward fill*: guarda o último valor não vazio de A e de B e
aplica nas linhas seguintes.

**Validação.** Para cada pessoa, o gestor declarado na coluna A tem de ser igual ao
gestor do gestor dela, buscado na aba de cima. Rodei essa checagem nas 329 linhas:

```
linhas incoerentes entre abas: 0 de 329
```

Também confirmei que o `Total de liderados` da planilha bate com o total recalculado
a partir da própria árvore, nas 329 linhas, sem nenhuma divergência.

## Passo 2 — Reconstruir os levels 2 e 3

Os levels 1 a 3 **não têm linha própria** na planilha: aparecem só como nome nas
colunas de gestor. Então:

- os nomes distintos na coluna B da aba `level 4` são os **L3** → 6 pessoas
- o nome distinto na coluna A da aba `level 4` é o **L2** → Jose Luiz de Oliveira Belixior Junior
- não existe aba de level 1 nem referência a "Nível de gerente 1", então **não há
  ninguém acima do Jose Luiz** nesta base

Como essas 7 pessoas não têm linha, **não têm cargo na planilha**. Esse gap foi
preenchido no passo 4.

Total reconstruído: **1 + 6 + 329 = 336 pessoas**.

## Passo 3 — Extrair as 65 imagens do draft

Os organogramas do draft são imagens, não texto: `python-pptx` não devolve nenhum
nome a partir delas. Então extraí cada imagem nomeada pelo slide de origem,
percorrendo também o interior dos grupos de formas:

```python
for i, slide in enumerate(prs.slides, 1):
    for j, shape in enumerate(imagens_do_slide(slide), 1):
        open(f"s{i:02d}_{j}.png", "wb").write(shape.image.blob)
```

Resultado: **65 imagens em 62 slides** (três slides têm mais de uma). Li todas,
uma por uma. A imagem da linha do CEO se repete em 7 slides (2, 15, 22, 27, 35, 41, 44)
— é o mesmo arquivo, conferido pelo hash.

## Passo 4 — Ler os cargos do topo no slide 2

O slide 2 mostra o CEO e os seis reportes com cargo, unidade e número de liderados.
Daí saíram os cargos que faltavam:

| Nome | Cargo lido | Liderados no print |
|---|---|---|
| Jose Luiz de Oliveira Belixior Junior | **Co-Chief Executive Officer** | 330 |
| Raioni De Oliveira Santos | Chief Operating Officer | 199 |
| Cleyton Cardoso Esteves | Chief Information & Tec… *(cortado)* | 47 |
| Ana Carolina Botelho Caldeira Vasconcellos | Chief Strategy Finance … *(cortado)* | 33 |
| Carolina Karnakis de Nobrega | Head of Talent | 23 |
| Andre Lemos Tavares | Chief Commercial Officer | 17 |
| Luis Fernando Santos Muniz | Head of Services | 5 |

Os dois cargos cortados foram confirmados pelas siglas do DRE: **CITO** e **CFSO**.

## Passo 5 — Achar tudo que foi desenhado em cima dos prints

Em vez de procurar a olho, listei **todas as formas que não são imagem** nos 75
slides, com posição, tamanho, cor de preenchimento e texto. Isso pega qualquer
anotação manual. O que apareceu:

| Tipo | Onde | O que é |
|---|---|---|
| 2 caixas + 3 conectores | slides 2, 15, 22, 27, 35, 41, 44 | `Prod / Aéreo / Sampaio` e `Prod / Marítimo / Filipe` na linha do CEO |
| 4 linhas cruzadas | slide 46 | dois **X** sobre caixas do organograma do COO |
| 2 linhas cruzadas | slide 48 | um **X** sobre uma caixa sob Carolina Bento Mendoza |
| 4 linhas cruzadas | slide 54 | dois **X** sobre caixas sob Daniela Bueno dos Reis Craig |
| 3 retângulos + rótulos | slide 20 | agrupa Vertical / Auto / High Tech e marca uma `Vaga de TL` |
| 2 retângulos + rótulos | slide 75 | agrupa o time em `KAM` e `Capacity` |
| caixas de texto | 6, 7, 8, 13, 14, 24, 29, 37, 46 | observações escritas |

## Passo 6 — Descobrir quais caixas os X riscam

Os X são linhas do PowerPoint, em coordenadas da página. As caixas estão dentro de
uma imagem. Para cruzar os dois, converti a posição de cada linha para pixel da
imagem:

```
x_pixel = (x_forma − x_imagem) × largura_em_pixels / largura_desenhada
```

Depois recortei a faixa da imagem em volta de cada ponto e olhei o recorte. Resultado:

| Slide | x na imagem | Caixa riscada | Cargo |
|---|---|---|---|
| 46 | ≈307 | **Filipe Carneiro De Oliveira** | Head of Ocean Product (18 liderados) |
| 46 | ≈1525 | **Filipe Teixeira Sampaio** | Head of Air Product (28 liderados) |
| 48 | ≈501 | **Magno Bezerra Rocha** | Airport Operations Manager (0 liderados) |
| 54 | ≈466 | **Gabriella De Melo Pereira** | Air Freight Operations TL (16 liderados) |
| 54 | ≈770 | **Pamela Iris Gregorio Ibarra** | Air Freight Operations TL (21 liderados) |

## Passo 7 — Aplicar a correção da estrutura

Os dois primeiros X riscam exatamente as duas pessoas que aparecem nas caixas azuis
da linha do CEO: **Sampaio** (Air Product) e **Filipe** (Ocean Product). Os dois
sinais juntos — tirado de um lugar, colocado no outro — significam que **Produto
Aéreo e Produto Marítimo reportam ao CEO**, não ao COO.

Aplicado isso:

| | Planilha Factorial | Com a correção do draft |
|---|---|---|
| Reportes diretos do CEO | 6 | **8** |
| Pessoas sob o COO | 202 | 154 |
| Level de Sampaio e Filipe | L4 | **L3** |
| Pessoas que mudam de level | — | 46 |

O level é a profundidade a partir do CEO, então o time dos dois subiu um nível
junto. A planilha guarda as duas versões: as colunas `Level na planilha Factorial` e
`Gestor na planilha Factorial` preservam o original, e `Observação do draft` registra
o motivo da mudança.

Os outros três X (Magno, Gabriella, Pamela) **não têm caixa de destino** no deck.
Estão marcados com `✗` no documento e na planilha, com o slide e a posição, sem
inferir para onde vão.

## Passo 8 — Conferir os 64 gestores contra o draft

Para cada gestor, comparei o `liderados` impresso no organograma com o total
calculado na árvore. Importante: a comparação usa a **árvore da planilha pura**, sem
a correção do passo 7, porque é essa a estrutura que estava no print.

Resultado: **12 gestores com diferença**, todos pela mesma causa — cinco pessoas com
data de início posterior ao draft. A diferença aparece em 12 gestores porque sobe pela
cadeia: a mesma pessoa conta para o TL, para o Head e para o C-level.

| Pessoa | Level | Início | Gestor |
|---|---|---|---|
| Danielle Vaz Faustino | L5 | 03/11/2026 | Vivian Ramalho De Assumpçao |
| Thalita Carnevale Sodre | L6 | 03/11/2026 | Danielle Moreira Rabelo Machado |
| Isabelle Oliveira Rattes | L7 | 03/11/2026 | Adriane Borel Cordeiro Impagliazzo |
| Poliana de Jesus Guedes | L8 | 03/11/2026 | Thais Espindola Oliveira Mathias |
| Fernanda Porto Lima | L7 | 16/11/2026 | Pamela Iris Gregorio Ibarra |

Fecha no topo: CEO com **330** no print e **335** na planilha, diferença de 5.

Nenhum outro gestor divergiu. Os outros 52 batem caixa por caixa, inclusive os nomes
dos liderados.

## Passo 9 — Casar os nomes entre as bases

As bases escrevem os nomes de formas diferentes: `MARIA CLARA FERREIRA DE SANTANA`
na folha, `Maria Clara Ferreira de Santana Rodrigues da Silva` no Factorial,
`CONSULTOR - LUCIMAR DESASSO DE CARVALHO ROCHA` em outra.

A primeira versão casava cada nome com a **primeira** correspondência encontrada, e
isso gerou erro: quando há três "Maria Clara", a primeira rouba o par da segunda.
Troquei por **atribuição pelo melhor score global**:

1. normaliza: remove acento, pontuação e as partículas `de/da/do/dos/das/e/junior/neto`
2. para cada par possível, calcula um score:
   - exige que o **primeiro nome ou o último sobrenome** seja igual
   - exige **2 tokens em comum**, ou que um nome seja subconjunto do outro
   - pontua `10 × tokens em comum`, com bônus para primeiro e último iguais e para
     subconjunto, e desconto pela diferença de tamanho
3. ordena todos os pares por score e atribui de cima para baixo, cada nome uma vez só

Isso corrigiu os falsos positivos. Exemplo: `Pamela Iris Gregorio Ibarra` aparecia
como "ausente do organograma" na primeira versão; o motivo real é que ela tem **duas
linhas na folha** (um contrato `OFF LETTER` e um `CLT`), e a segunda ficava sem par.

## Passo 10 — Classificar cada divergência

Nenhuma das bases tem a mesma data de corte, então sobra diferença por construção.
Cada linha sem par recebe uma causa automática:

**Está no organograma e não na base**
- nome é `Colaborador Teste` → registro de teste
- level 2 → o CEO não entra na folha nem no DRE
- início posterior ao corte da base → admissão nova, não poderia estar lá
- resto → **sem custo na base, verificar**

**Está na base e não no organograma**
- nome com mais de uma linha na folha → linha duplicada, a pessoa está no organograma
- situação `AVISO PREVIO V` ou `OFF BOARDING` → saindo, já retirada do organograma
- tipo de custo `Sócios` → sócio / conselho, fora do organograma
- contrato `CONSULTOR` ou área terminando em `Consultoria` → contrato, não pessoa
- não está na folha de setembro → estava no baseline de agosto e saiu
- resto, com situação `ATIVO` → **gap real**

Resultado na aba `Divergencias`: 397 linhas, com tudo classificado.

| Comparação | Casaram | Só no organograma | Só na base |
|---|---|---|---|
| Organograma × Baseline DRE 26.2 (agosto) | 304 | 32 | 24 |
| Organograma × Folha Set/26 | 311 | 25 | 12 |

Depois de descontar tudo que tem explicação, sobram **3 pessoas ativas com custo
lançado e sem posição no organograma**: Bruno Felipe Dias, Dhauan Derito e
Eduardo Bandeira Da Rocha Oliveira.

## Passo 11 — Checar os estagiários

A lista de gestores não tem nenhum estagiário porque **ela só traz quem tem
liderado**, e nenhum estagiário lidera alguém. Eles estão nos blocos por level,
dentro do time de cada gestor.

Conferência por fonte, usando fronteira de palavra no filtro (`\bintern\b` — sem
isso, *International* entra como *intern* e o número sai errado):

| Fonte | Estagiários / aprendizes |
|---|---|
| Organograma Factorial (out/26) | 29 |
| Folha Set/26, `POSIÇÃO` = INTERN ou APPRENTICE | 28 |
| Baseline DRE, `Folha/Colchão` = Aprendiz/Estagiário | 31 |

As diferenças:
- 6 entraram em out/26, depois do fechamento da folha de setembro
- 4 viraram efetivos e no organograma já constam como *Assistant* — na folha de
  setembro estão com situação `TRANSIÇÃO DE CONTRATO` (Irlam da Silva Fernandes,
  Julia Gonçalves Cruz Ramos, Livia dos Santos Martins, Felipe Sodre de Freitas)
- 4 estavam no DRE de agosto e saíram até outubro
- 1 está na folha e no DRE e não no organograma: Dhauan Derito

## Passo 12 — Ligar as vagas às admissões novas

A planilha de vagas tem 65 linhas, 14 com nome de contratado. **13 desses 14 nomes
estão no organograma**, nas posições e datas certas — é isso que explica as
admissões de outubro e novembro que não aparecem na folha de setembro.

Sobraram **8 vagas abertas e publicadas**, sendo a mais relevante para a estrutura
`OVERLAND HEAD (Europa)`, no mesmo nível dos Heads de hoje.

---

## O que ficou em aberto

1. **Cleyton e Ana Carolina** têm o cargo cortado no print. As siglas do DRE (CITO,
   CFSO) indicam *Chief Information & Technology Officer* e *Chief Strategy & Finance
   Officer*, mas o texto completo não aparece em nenhuma imagem.
2. **Os X em Magno, Gabriella e Pamela** não têm destino desenhado no deck.
3. **O time de Victor Telles Gonzaga** — 27 reportes diretos e 37 pessoas, o maior da
   empresa — não está aberto no draft. O slide 26 mostra só a caixa dele.
4. **Quatro diretorias** (Tecnologia, Finanças, RH e Operações) trazem, no próprio
   draft, o aviso de que a estrutura foi mexida depois do print.
5. **Produto Aéreo e Marítimo no DRE** continuam dentro de COO. Se a mudança do draft
   já valer, o rateio de custo precisa acompanhar.

## Como regerar

```bash
pip install openpyxl pillow python-pptx
python3 estrutura/gestores_por_level.py
```
