# Feedback do Zé sobre o deck de vagas — avaliação e respostas

> Separei em: (A) ajustes de design diretos, (B) os pontos que pedem decisão ou
> alinhamento de conceito e (C) as respostas às perguntas dele, já com os dados.
> Tudo conferido na planilha de vagas (21/10) e na base de setembro.

---

## A. Ajustes de design (diretos, sem discussão)

1. **Remover os dois textos de baixo** (as caixas de leitura/rodapé que ele apontou).
   Concordo, não estavam agregando e competiam com os gráficos.
2. **Aumentar os gráficos e a fonte.** Com os dois textos fora, sobra espaço vertical
   para os três gráficos crescerem e a fonte subir, melhora a leitura à distância.
3. **Tirar os valores financeiros.** Remover a coluna/caixa de custo das vagas. O foco
   dele é quadro e ocupação, não R$.

---

## B. Pontos que precisam de alinhamento antes de eu alterar

**1. "Colchão são vagas para crescer e demais são reposição" — cuidado, são dois
campos diferentes na planilha.**
O que o Zé descreveu não bate com a estrutura do arquivo. Existem duas colunas
distintas:
- **Folha/Colchão**: entre as 49 vagas abertas, só **1 é Colchão**, 44 são Folha e 4
  Aprendiz/Estágio. Se "crescer = Colchão", só teríamos 1 vaga de crescimento, o que
  não faz sentido.
- **Ocupante/Vaga**: é o campo que separa de verdade **Aumento de Quadro (30)** de
  **Vaga Substituição (19)**.

O conceito dele de "crescer vs repor" está certo, mas o campo correto é o
**Ocupante/Vaga**, não o Colchão. Preciso confirmar com ele qual definição vale antes
de rotular os gráficos, senão o número muda.

**2. "Temos 14 vagas de reposição, isso é problema" — pela planilha são 19, não 14.**
Pelo campo Ocupante/Vaga, as vagas de substituição abertas são **19**. O número 14 do
Zé provavelmente vem de outra régua (talvez só Folha, excluindo os 4 estágios e algo
mais). Vale alinhar: se reposição é tudo que é "Vaga Substituição", são 19; se ele
exclui estágios, cai para 15. **Preciso que ele confirme a régua** para o gráfico
fechar com a cabeça dele.
- Se o ponto é "reposição é problema", o argumento se sustenta: são ~19 saídas que a
  operação já absorveu e precisa repor só para manter o nível atual, antes mesmo de
  crescer.

---

## C. Respostas às perguntas dele (com dados)

**"Validar quais são as vagas, se são de USA/Europa."**
Separei as 49 vagas abertas por geografia, lendo o marcador no cargo
(INLAND USA/AMERICAS = USA, INLAND EUROPA/EUROPA = Europa, resto = Geral/Brasil):

| Geografia | Vagas abertas |
|---|---|
| Geral / Brasil | 34 |
| USA | 9 |
| Europa | 6 |

As **19 de reposição** se dividem em **17 Geral/Brasil e 2 Europa** (nenhuma de
reposição é dos EUA, lá é tudo aumento de quadro). As reposições de Europa são as duas
`AIR OPS ANALYST INLAND EUROPA` / `AIR RD ANALYST INLAND EUROPA`.

**"No gráfico da direita, considera separar USA x Europa x Geral."**
Dá para fazer, e melhora. Hoje o gráfico da direita quebra as vagas do COO por área;
a sugestão é transformar em **três grupos: USA (9), Europa (6) e Geral/Brasil (34)**,
cada um podendo abrir em crescer vs repor. Fica mais acionável para a conversa dele,
porque é assim que ele pensa a operação (por praça). Vou refazer o gráfico da direita
com esse corte.

**"Os que estão em Warehouse, conseguimos saber qual é?"**
Sim, os 5 estão identificados na base, todos em DMS América (EUA), área Overland, sob
Possidônio Dantas:

| Nome | Cargo | Nível |
|---|---|---|
| Jesus Guillermo Ledi Mendoza | WH TL | Team Leader |
| Marcelo de Jesus Cedeño Diaz | WH Clerk Analyst | Analyst |
| Daniel Marcelino Cedeño Rodríguez | WH Clerk Analyst | Analyst |
| Jorge Correa Varela | WH Clerk Assist | Assistant |
| Luis Carlos Coronado Barrera | WH Clerk Assist | Assistant |

Observação: são 1 TL + 2 analistas + 2 assistentes para cobrir MIA, Houston e NY. A
base não separa por praça (só diz EUA), então **não dá para dizer quantos em cada
cidade** — isso é o que precisa ser confirmado com a Operação. É o mesmo ponto que já
está nas pendências do slide 4 sobre Nova York.

---

## Resumo do que vou alterar no deck

- Remover os dois textos de baixo, ampliar os três gráficos e a fonte.
- Tirar os valores financeiros.
- Refazer o gráfico da direita com o corte USA / Europa / Geral.
- **Travado até o Zé confirmar:** a régua de reposição (14, 15 ou 19) e se "crescer"
  usa o campo Ocupante/Vaga ou Folha/Colchão. Assim que ele responder, fecho os
  rótulos dos gráficos.
