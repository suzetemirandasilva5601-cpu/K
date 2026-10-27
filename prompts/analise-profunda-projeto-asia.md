# Projeto Ásia (China) — Análise profunda: próximos passos, recomendações e riscos

> Documento de trabalho interno (ATY). Vai além do briefing e do documento de board:
> destrincha o que precisa ser feito, em que ordem, o que pode dar errado e como mitigar.
> Base: Diagnóstico China (16/10), apresentação "DMS +Asia Investimento" e os três
> arquivos operacionais já analisados.

---

## 1. Onde o projeto está hoje (leitura de maturidade)

O projeto tem **duas camadas que andam juntas mas são distintas**, e é importante não
confundi-las:

| Camada | O que é | Status |
|---|---|---|
| **Estratégica** (apresentação) | Investir num headcount local via RS Logistics e migrar volume por gates | Pronta para o board decidir |
| **Operacional** (diagnóstico) | Trackers de tarifa, governança, NAC/Baskets, saneamento de dados | Depende de 8 decisões e de acesso a dados |

O ponto cego: a apresentação de board vende a **tese de negociação** (ganho de rate no
âncora), mas o diagnóstico mostra que a DMS ainda **não tem a infraestrutura de dados**
para provar esse ganho. O M2 (piloto no âncora) pressupõe comparar "rate real vs. hoje",
mas o próprio diagnóstico diz que falta histórico comparável de compra. **Essa é a maior
desconexão do projeto e precisa ser resolvida antes do gate crítico.**

---

## 2. Próximos passos — sequência recomendada

Organizei em três horizontes. O erro a evitar é tratar o headcount como primeiro passo
isolado; ele precisa chegar com a base de dados já em construção.

### Horizonte 0 — Pré-aprovação (antes de levar ao board)
1. **Fechar a taxa de estrutura da RS Logistics.** Sem isso o break-even de ~30% é
   fictício. É a informação que mais muda o caso e está faltando. Pedir proposta formal.
2. **Validar o número do pool (R$ 2,04 mi) e a parcela capturável.** Quanto dos R$ 2,04
   mi é negociação (substituível por 1 pessoa) vs. transacional (documentação/desembaraço,
   não substituível)? Sem isso, o ~30% de captura é chute.
3. **Confirmar quem é o armador-âncora e a origem dos 30,7%.** Toda a tese depende desse
   número; precisa estar auditado como fizemos com as vagas.
4. **Desenhar o perfil da vaga.** Sênior com relacionamento com armadores é diferente de
   um analista de pricing. O perfil define o salário e o que M1/M2 conseguem entregar.

### Horizonte 1 — Primeiros 90 dias pós-aprovação (M1 + fundação de dados)
5. **Rodar M1 (expansão no bloco secundário)** em paralelo com a **Etapa 1-2 do
   diagnóstico** (consolidar dados + construir trackers marítimo e aéreo). O profissional
   local alimenta o tracker com dados reais de compra — matando dois coelhos.
6. **Estabelecer a governança RD / FD / MI / Strategy / Operações / Financeiro.** O
   diagnóstico lista isso como decisão necessária; sem dono claro, o piloto M2 não terá
   quem valide margem e rate.
7. **Definir as 4 métricas de gate do M2 com baseline numérico.** "Rate real vs. hoje"
   exige um "hoje" medido — que só existe se o tracker estiver rodando. Conectar M1 ao
   tracker resolve isso.

### Horizonte 2 — Gate crítico e além (M2 → M3)
8. **Executar M2 (piloto no âncora)** com 15-20 embarques reais, não cotação. Decisão
   go/no-go nas 4 métricas.
9. **Só então** desenhar M3 (concentração parcial), com cláusulas de exclusividade, SLA e
   reversibilidade — e levar de volta ao board.
10. **M4 (LCL próprio)** roda em paralelo o tempo todo, acionado pelo gatilho de volume
    (20 CBM ou 5 emb./semana). Monitorar o gatilho desde o dia 1.

---

## 3. Recomendações estratégicas (além do "aprovar")

**R1 — Amarrar o headcount à construção do tracker, não só à negociação.** O maior risco
do projeto é o profissional chegar e não ter dados para provar ganho. Fazer dele o dono
do Rate Buying Tracker nos primeiros 60 dias transforma o M1 num período produtivo mesmo
que a negociação demore.

**R2 — Tratar o ganho de agente e o ganho de armador como dois business cases separados.**
O ganho de agente (R$ 2,04 mi, comprovável) justifica o headcount sozinho. O ganho de rate
no âncora é upside, não base. Vender os dois juntos infla a expectativa e cria pressão
para migrar volume cedo demais — exatamente o que o desenho em gates quer evitar.

**R3 — Proteger as contas que sustentam o volume antes de mexer nos agentes.** Top-5
clientes = 51,8% e 2 agentes = 69% do pool. A ordem importa: estabilizar relacionamento
com clientes e só então redimensionar agentes, nunca o inverso.

**R4 — Definir desde já o critério de reversibilidade.** Como é "posição em parceria" e
não entidade, a saída deve ser barata. Deixar explícito no acordo com a RS: aviso prévio,
propriedade dos dados/relacionamentos gerados e o que acontece com o volume migrado se a
parceria terminar. Isso é o que torna o investimento genuinamente de baixo risco.

**R5 — Comparar formalmente com Hamburgo na mesma moeda.** Board vai decidir os dois.
Montar um quadro lado a lado (CAPEX, prazo de retorno, reversibilidade, exposição) para a
decisão ser relativa e não isolada — são naturezas de investimento diferentes e o board
precisa ver isso explícito.

---

## 4. Mapa de riscos (probabilidade x impacto x mitigação)

| # | Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | Taxa da RS inviabiliza o break-even | Média | Alto | Fechar taxa antes de aprovar; renegociar escopo se > X% |
| 2 | Ganho de rate no âncora não se confirma em M2 | Média | Alto | É o próprio gate; não migrar volume sem go. Headcount se paga pelo ganho de agente mesmo sem isso |
| 3 | Falta de dados impede medir o gate do M2 | **Alta** | Alto | Conectar M1 ao tracker; não abrir M2 sem baseline medido |
| 4 | Transição dos 2 agentes (69%) quebra serviço | Média | Alto | Retaguarda ativa; migração gradual; nunca 100% |
| 5 | Perda de cliente do top-5 derruba a alavancagem | Baixa | Alto | Estabilizar contas antes de mexer em fornecedor (R3) |
| 6 | Dependência da RS (ponto único de falha) | Média | Médio | Cláusula de reversibilidade e posse de dados (R4) |
| 7 | Perfil contratado não tem acesso a armadores | Média | Alto | Perfil sênior com rede comprovada; validar em M1 |
| 8 | Exposição de informação / compliance China | Baixa | Médio | Governança formal; escala só em M5 com aprovação |
| 9 | Capacidade de 1 pessoa é limitada (pool é transacional) | **Alta** | Médio | Captura parcial assumida; dimensionar expectativa a parcela "intelectual" |
| 10 | GRI (reajuste geral de tarifa) apaga o ganho de M3 | Média | Médio | M3 exige sustentação do ganho além de 1 ciclo de GRI |

Os dois riscos de **probabilidade alta** (3 e 9) são de execução, não de estratégia — e
os dois têm a mesma raiz: a DMS está apostando numa capacidade (dados + 1 pessoa) que
ainda não tem instalada. Por isso a R1 e a R2 são as recomendações mais importantes.

---

## 5. Perguntas em aberto para fechar com o cliente

- Qual a taxa de estrutura da RS? (trava o break-even)
- Quem é o armador-âncora e como foi medido o 30,7%?
- Dos R$ 2,04 mi, quanto é negociação vs. transacional?
- Existe baseline de rate comparável hoje, ou será construído do zero?
- O perfil pretendido tem relacionamento com armadores ou é pricing/analista?
- Qual o prazo e o custo de Hamburgo, para a comparação lado a lado?
- Há exigência regulatória (WFOE, NVOCC) que muda se o volume crescer além de certo ponto?

---

## 6. O que entregar em seguida (sugestão de produtos)

1. **Quadro comparativo China x Hamburgo** — uma página, para o board decidir os dois juntos.
2. **Modelo financeiro editável** — break-even sensível à taxa da RS e ao % de captura,
   para testar cenários em vez de um número fixo.
3. **Plano de 90 dias do profissional** — unindo M1 (negociação) e Etapa 1-2 do
   diagnóstico (trackers), com entregáveis semanais.
4. **Termo de parceria com a RS** — com as cláusulas de reversibilidade e posse de dados.

---

## 7. Síntese

O projeto é **estrategicamente sólido e bem desenhado** — o modelo em gates é exatamente
o jeito certo de limitar exposição. O risco real não está na estratégia, está na
**lacuna de execução**: a DMS quer provar ganho de negociação sem ter ainda a base de
dados que torna a prova possível. A recomendação central é **aprovar o headcount, mas
amarrá-lo à construção da inteligência de dados desde o dia 1**, tratar o ganho de agente
(comprovável) como a justificativa e o ganho de armador (hipótese) como upside, e não
avançar nenhum volume sem o gate medido. Assim o investimento se mantém reversível e a
tese se prova com fato, não com expectativa.
