# Prompt: apresentação "Vagas em aberto x Ocupação nas Operações"

> Prompt pronto para colar. Todos os números abaixo foram conferidos contra
> `CIS_20261013_ORDERS.parquet`, `Base_Setembro26 (1).xlsx` e `Vagas 21-10.xlsx`.
> Quem executar o prompt **não deve recalcular nem inventar números**: usar
> exatamente os valores do Anexo A.

---

## PROMPT

Você é analista de consultoria e vai montar uma apresentação executiva em PowerPoint
para o Zé, cujo interesse é **a operação**. O recorte de liderança deve girar em torno
do **COO**: heads e team leaders das Operações.

### Arquivo e template

Use obrigatoriamente o template:
`20261020 - ATY - Diligenciamento Fase 1 - Estrutura e Job Description vZé - Template DMS (1).pptx`

Características a respeitar:

- Formato 16:9, 13,33 x 7,50 polegadas.
- Layout de conteúdo: **`DMS_Conteudo`**, com os placeholders já existentes:
  - `Title 1`: título de ação, uma frase completa que entrega a conclusão do slide.
  - `Text Placeholder 2`: kicker da seção, no padrão `Operações – <tema>`.
  - `Text Placeholder 3`: subtítulo explicativo curto.
  - `Text Placeholder 4`: fonte, no padrão
    `Fonte: CIS, ORDERS.parquet (13/10/2026); Base Setembro/26; Vagas 21/10`.
  - `Disclaimer_Box`: manter o selo `Para discussão`.
- Capa: layout `Blank_Analytics`, igual ao slide 1 existente (manter a arte e os
  logos, trocar apenas o texto).
- Encerramento: layout `EndWhite_Analytics` ou `EndColor_Analytics`.
- Não altere cores, fontes, logos nem posições dos elementos de marca.

### Estrutura: 5 slides (capa + 3 de conteúdo + encerramento)

#### Slide 1 — Capa (`Blank_Analytics`)

Texto, no mesmo bloco do slide 1 atual:
```
Projeto Diligenciamento
Vagas em aberto x ocupação nas Operações
Outubro de 2026
```

#### Slide 2 — Panorama: onde a operação está mais descoberta

- **Kicker:** `Operações – Ocupação x vagas`
- **Título de ação sugerido:** "Operações opera com 19,6% do quadro em aberto, e a
  descoberta se concentra em Inland Freight Europa e Operações America"
- **Conteúdo:** tabela dos 7 blocos com as colunas
  `Bloco | Ativos | TL+ | Vagas | % quadro aberto | Embarques/mês | Embarques por ativo | Dono`
  usando o Anexo A1. Ordenar por `% quadro aberto` decrescente.
- **Destaque visual:** barras de `% quadro aberto`, com Inland Freight Europa (55,6%)
  e Operações America (50,0%) em cor de alerta; Warehouses em cor neutra com rótulo
  "sem vaga aberta".
- **Rodapé analítico:** "Volume por ativo é ordem de grandeza por bloco, não
  produtividade individual: o CIS mostra quem executou cada etapa, não o headcount,
  e o Customer Care do Brasil atende embarques de Miami."

#### Slide 3 — Os pontos de atenção e a camada de liderança

- **Kicker:** `Operações – Pontos de atenção`
- **Título de ação sugerido:** "Três frentes concentram o risco: Europa sem team
  leader, Operações America com metade do time e Exportação com a maior carga por
  pessoa"
- **Conteúdo:** quatro blocos curtos, um por ponto de atenção, cada um com o número
  que o sustenta (Anexo A2):
  1. **Quadro mais vazio:** Inland Freight Europa, 55,6% em aberto, 4 ativos e 5
     vagas, e **nenhum team leader** no bloco.
  2. **Liderança descoberta:** Operações America, 50,0% em aberto, 7 ativos e 7
     vagas, das quais **3 são de team leader** (`AIR OPS TL AMERICAS`) com apenas
     1 TL hoje. Há ainda uma vaga de `OVERLAND HEAD` aberta e publicada.
  3. **Maior carga por pessoa:** Exportação Brasil, ~99 embarques por ativo ao mês
     com 3 pessoas e 25,0% do quadro em aberto. Customer Care vem depois, ~62 por
     ativo, porém com 37 pessoas, 7 TLs e só 2,6% em aberto.
  4. **Risco silencioso:** Warehouses MIA/Houston/NY, 5 pessoas para 3 praças e
     **zero vaga**, enquanto Houston saltou de ~19 para 169 embarques/mês
     (média abr–set de 94). Nova York não existe como escritório no CIS.
- **Caixa lateral "Liderança sob o COO":** 193 ativos, 7 heads, 28 team leaders e
  2 senior team leaders. Mostrar o span por área (Anexo A3), destacando
  Air Operations com 78 pessoas sob uma única head.

#### Slide 4 — Plano de ação para a agenda de 30 minutos com o RH

- **Kicker:** `Operações – Plano de ação`
- **Título de ação sugerido:** "Cada frente crítica sai da agenda com ação, dono e
  prazo definidos"
- **Conteúdo:** tabela `Frente crítica | % quadro aberto | Ação | Dono | Prazo de efeito`
  com as 8 linhas do Anexo A4. Ordenar por criticidade (% em aberto e carga).
- **Faixa inferior "Pendências para fechar na reunião":**
  - 12 das 19 vagas de Operações estão **sem estágio de processo informado**; a base
    traz apenas o mês de início do ciclo, não a data de abertura. Sem isso não é
    possível medir dias em aberto nem acionar a regra de headhunter acima de 45 dias.
  - A vaga mais antiga de toda a empresa é `PER DEP ANALYST` (Talent Management Team),
    ciclo iniciado em março, cerca de 7 meses em aberto.
  - Confirmar com a Operação o volume próprio de Nova York e quantas pessoas do bloco
    de Warehouses atendem a praça.
  - O número de ativos precisa vir do RH; o CIS não informa headcount por área.

#### Slide 5 — Encerramento (`EndWhite_Analytics` ou `EndColor_Analytics`)

Sem conteúdo analítico novo. Manter a arte do template.

### Regras de conteúdo

1. **Não recalcule nem invente números.** Use exclusivamente o Anexo A.
2. Percentuais com **vírgula decimal** e valores em **R$ com ponto de milhar**.
3. **Sem travessões** (— ou –) em nenhum texto; use vírgula, dois pontos ou parênteses.
4. Títulos de ação: frase completa que entrega a conclusão, no padrão do template.
5. Máximo de 6 linhas de texto por bloco; o slide é de leitura rápida.
6. Toda tabela ou gráfico deve ter a fonte no `Text Placeholder 4`.
7. Separe sempre **aumento de quadro** de **vaga substituição**: só o primeiro
   expande a estrutura. Nas Operações são 16 de aumento e 3 de substituição.
8. Ao citar área, use a nomenclatura da base de setembro (caixa alta).
9. Não trate volume por ativo como produtividade individual.

### Glossário de equivalência entre as bases (necessário para o cruzamento)

- **Embarque** = `assembly_id` distinto no CIS, datado por `created_at`. Contar linhas
  do parquet superestima: Miami daria 1.212/mês em vez de 878.
- **Blocos operacionais** são identificados pelo **cargo** (`CARGO DRE 2026.2`), não
  pela área: termos como `INLAND`, `AMERICAS`, `EUROPA`, `WH`, `CC` e `EXPORT` só
  existem no cargo. Procurar "inland" na coluna de área não retorna nada.
- **C-Level:** `CCO` na planilha de vagas e na DRE de agosto equivale a `CMO` na base
  de setembro.
- **Área:** `Healthcare` nas vagas equivale a `HEALTHCARE INDUSTRY` na base.

---

## Anexo A — Dados verificados

### A1. Ocupação, vagas e volume por bloco

| Bloco | Ativos | TL+ | Vagas | % quadro aberto | Aumento | Subst. | Embarques/mês | Embarques por ativo | Custo vagas | Dono |
|---|---|---|---|---|---|---|---|---|---|---|
| Europa / Inland Freight Europa | 4 | 0 | 5 | 55,6% | 2 | 3 | 530 (bloco Europa) | 29 | R$ 64.277 | Carol Mendoza |
| EUA / Operações America | 7 | 1 | 7 | 50,0% | 7 | 0 | 1.110 (bloco EUA) | 56 | R$ 124.055 | Carol Mendoza, Filipe Sampaio |
| EUA / Inland Freight America | 8 | 1 | 3 | 27,3% | 3 | 0 | 1.110 (bloco EUA) | 56 | R$ 43.611 | Carol Mendoza, Filipe Sampaio |
| Brasil / Exportação | 3 | 1 | 1 | 25,0% | 1 | 0 | 298 | 99 | R$ 13.371 | Carol Mendoza |
| Europa / Operações Europa | 14 | 2 | 2 | 12,5% | 2 | 0 | 530 (bloco Europa) | 29 | R$ 20.666 | Carol Mendoza, Filipe Sampaio |
| Brasil / Customer Care | 37 | 7 | 1 | 2,6% | 1 | 0 | 2.287 | 62 | R$ 12.005 | Carol Mendoza, Natália Costa |
| EUA / Warehouses (MIA, Houston, NY) | 5 | 1 | 0 | 0,0% | 0 | 0 | 1.110 (bloco EUA) | 56 | R$ 0 | Possidônio Dantas |
| **TOTAL Operações** | **78** | **13** | **19** | **19,6%** | **16** | **3** | | | **R$ 277.985** | |

`TL+` = team leaders, senior team leaders, coordinators e heads do bloco.
`% quadro aberto` = vagas ÷ (ativos + vagas).

### A2. Volume do CIS por origem (média abr–set/26, conferido)

| Bloco | Origem no CIS | Aéreos/mês | Marítimos/mês | Status da conferência |
|---|---|---|---|---|
| EUA | DMS Miami | 878 | 139 | confere |
| EUA | DMS Houston | 94 | 0 | confere (jul–set: 169, confere) |
| EUA | Nova York | não existe | não existe | confirmado: não há escritório NY no CIS |
| Europa | DMS Frankfurt | 351 | 0 | confere |
| Europa | DMS Lisboa | 179 | 0 | confere |
| Brasil | Importação aérea (Customer Care) | 2.287 | | confere |
| Brasil | Exportação | 244 | 55 | confere |

Somatórios: EUA 971 aéreos/mês e Europa 530 aéreos/mês, ambos conferem com os
~970 e ~530 informados. Escritórios DMS existentes no CIS: Miami, Houston,
Frankfurt, Lisboa e Brasil.

Houston: a média abr–set de 94 esconde a aceleração. O trimestre jul–set roda a
169/mês, o que implica ~19/mês em abr–jun, salto de 8,9 vezes. Usando o ritmo
atual, o bloco EUA sobe de 56 para 59 embarques por ativo.

### A3. Liderança sob o COO (193 ativos: 7 heads, 28 TLs, 2 Sr. TLs, 1 coordinator)

| Área | Ativos | Head | TLs |
|---|---|---|---|
| AIR OPERATIONS | 78 | Carolina Bento Mendoza | 15 |
| OCEAN OPERATIONS | 38 | Natália Correia da Costa Parreira | 4 |
| AIR PRODUCT | 28 | Filipe Teixeira Sampaio | 5 |
| OCEAN PRODUCT | 19 | Filipe Carneiro de Oliveira | 3 |
| QUALITY & OPERATIONAL INTELLIGENCE | 13 | Marco Antonio Maraia Villa | 2 |
| OVERLAND | 9 | Possidônio Dantas de Almeida Neto | 2 |
| OPERATIONAL EXCELLENCE | 7 | Jonathas Amâncio Alves | 0 |
| OPERATIONS | 1 | sem head no nível | 0 |

Vagas de liderança nas Operações: 3 de `AIR OPS TL AMERICAS` (aumento de quadro),
1 de `AIR RD TL` (substituição) e 1 de `OVERLAND HEAD` (aumento, aberta e publicada).

### A4. Plano de ação

| Frente crítica | % quadro aberto | Ação | Dono | Prazo de efeito |
|---|---|---|---|---|
| Europa / Inland Freight Europa | 55,6% | Reaproveitar finalistas de processos recentes e indicação interna com bônus | Carol Mendoza + RH | 1 a 3 semanas |
| EUA / Operações America | 50,0% | Vaga pré-aprovada com faixa e budget definidos, processo enxuto e cobertura temporária pelo Brasil no back-office | Carol Mendoza, Filipe Sampaio + RH | Imediato |
| EUA / Inland Freight America | 27,3% | Indicação interna com bônus; as três vagas já estão publicadas | Carol Mendoza, Filipe Sampaio + RH | 2 a 3 semanas |
| Brasil / Exportação | 25,0% | Processo enxuto e busca de profissionais de contratos encerrados, verificando não aliciamento | Carol Mendoza + RH | Imediato a 4 semanas |
| Europa / Operações Europa | 12,5% | Processo enxuto: triagem em 48 h, entrevistas no mesmo dia e proposta em 24 h | Carol Mendoza, Filipe Sampaio + RH | Imediato |
| Brasil / Customer Care | 2,6% | Processo enxuto e acompanhamento do volume por ativo | Carol Mendoza, Natália Costa + RH | Imediato |
| EUA / Warehouses (MIA, Houston, NY) | 0,0% | Validar necessidade de abrir vaga e contratar temporários ou agência para as três praças | Possidônio Dantas + RH | 1 a 2 semanas |
| Talent Management Team (`PER DEP ANALYST`) | vaga mais antiga | Headhunter, por passar de 45 dias em aberto | Carolina Karnakis + RH | 3 a 4 semanas |

### A5. Playbook de ações (referência)

| Ação | Quando usar | Prazo de efeito |
|---|---|---|
| Reaproveitar finalistas de processos recentes | Cargo com processo parecido nos últimos 6 meses | 1 a 2 semanas |
| Processo enxuto: triagem em 48 h, entrevistas no mesmo dia, proposta em 24 h | Todas as vagas | Imediato |
| Vaga pré-aprovada, com faixa salarial e budget definidos antes de abrir | Vagas ainda em aprovação | Imediato |
| Cobertura temporária pelo Brasil | Back-office (cadastro, follow-up, documentos) de EUA e Europa | Imediato |
| Indicação interna com bônus | Todas, principalmente EUA e Europa | 2 a 3 semanas |
| Temporários ou agência | Warehouses de MIA, Houston e NY | 1 a 2 semanas |
| Profissionais vindos de contratos encerrados | Operações e Customer Care; verificar não aliciamento | 2 a 4 semanas |
| Headhunter | Liderança e vagas com mais de 45 dias | 3 a 4 semanas |
