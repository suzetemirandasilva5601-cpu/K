// Conteúdo dos três materiais: casebook do FemVest, template de case e ficha de avaliação.
const { W, C, el, box, header, footer } = require('./motor');

const L = 0.35, LW = 6.2, R = 6.7, RW = 6.3;   // grade de duas colunas

// ---------- peças comuns ----------
function capa(o) {
  return [
    el.rect(0, 0, W, 7.5, { fill: C.red }),
    el.image(0.6, 0.55, 2.62, 0.33, 'logo_branco.png'),
    el.table(9.0, 0.45, 3.9, [1.3, 1.3, 1.3], [
      [{ t: 'Geral', fill: C.red, align: 'center' }, { t: 'Quant', fill: C.red, align: 'center' }, { t: 'Criatividade', fill: C.red, align: 'center' }],
      [{ t: o.geral, fill: C.red, color: C.white, align: 'center' }, { t: o.quant, fill: C.red, color: C.white, align: 'center' }, { t: o.criat, fill: C.red, color: C.white, align: 'center' }],
    ], { size: 12, rowH: 0.32 }),
    el.text(9.0, 1.12, 3.9, 0.3, 'Dificuldade de 1 (introdutório) a 3 (avançado)', { size: 9, color: C.white, align: 'center' }),
    el.text(0.6, 2.85, 12, 0.85, `**${o.titulo}**`, { size: 36, color: C.white, valign: 'bottom', inset: 0 }),
    el.rect(0.6, 3.82, 12.1, 0.035, { fill: C.white }),
    el.text(0.6, 4.0, 6.6, 3.0, o.descricao, { size: 14, color: C.white, inset: 0, paraAfter: 1 }),
    el.rect(7.7, 4.05, 5.0, 0.45, { line: C.white, dash: true }),
    el.text(7.7, 4.05, 5.0, 0.45, `**${o.selo}**`, { size: 13, color: C.white, align: 'center', valign: 'middle' }),
    el.text(7.7, 6.55, 5.0, 0.5, o.aviso, { size: 10, color: C.white, align: 'right', valign: 'bottom', inset: 0 }),
  ];
}

function cabecalhoAbertura(o) {
  return [
    el.rect(0, 0, W, 1.3, { fill: C.red }),
    el.text(L, 0.28, 7.8, 0.6, `**${o.titulo}**`, { size: 24, color: C.white, valign: 'bottom', inset: 0 }),
    el.rect(L, 0.92, 5.7, 0.31, { line: C.white, dash: true }),
    el.text(L, 0.92, 5.7, 0.31, `**${o.selo}**`, { size: 10, color: C.white, valign: 'middle', inset: 4 }),
    el.table(8.25, 0.3, 4.75, [1.58, 1.58, 1.59], [
      [{ t: o.nivel, colspan: 3, fill: C.white, color: C.dark, bold: true, align: 'center' }],
      [{ t: 'Tipo de case', fill: C.tab, bold: true, align: 'center' }, { t: 'Indústria', fill: C.tab, bold: true, align: 'center' }, { t: 'Cliente', fill: C.tab, bold: true, align: 'center' }],
      [{ t: o.tipo, align: 'center' }, { t: o.industria, align: 'center' }, { t: o.cliente, align: 'center' }],
    ], { head: false, size: 9, rowH: 0.24 }),
  ];
}

function avaliacao(x, y, w, h, nota) {
  const crit = ['Estrutura', 'Análise e resolução de problemas', 'Comunicação e postura', 'Síntese e recomendação'];
  const items = [box(x, y, w, h, 'Avaliação do case', null)];
  items.push(el.text(x + 0.1, y + 0.29, w - 0.2, 0.22, nota, { size: 8.5, color: C.grey, inset: 0 }));
  crit.forEach((c, i) => {
    const cy = y + 0.58 + i * 0.6;
    items.push(el.text(x + 0.25, cy, w - 0.4, 0.22, `_ ${c}`, { size: 9, inset: 0 }));
    items.push(el.balls(x + 0.3, cy + 0.23, 0.24, 0.42, { numbers: true }));
  });
  return items;
}

// ============================================================
// CASEBOOK FEMVEST
// ============================================================
function femvest() {
  const TOT = 7;
  const nome = 'Case 01: FemVest';
  const rod = 'Ciclo de cases · Case 01: FemVest · Material do entrevistador';
  const sl = [];
  let pg = 1;
  const t = n => `${nome} (${n}/${TOT})`;

  sl.push(capa({
    titulo: nome, geral: '2', quant: '2', criat: '2',
    descricao: [
      '**Tipo de case:**', 'Market Entry (lançamento de produto)', '',
      '**Indústria:**', 'Serviços financeiros · fintech de investimentos', '',
      '**Conceitos testados:**',
      '• Dimensionamento de mercado',
      '• Margem de contribuição e ponto de equilíbrio',
      '• Business case de 3 anos',
      '• Priorização de produto e entrada no mercado',
    ].join('\n'),
    selo: 'CCU · Semana 1 · Conduzido pelo entrevistador',
    aviso: 'Material do entrevistador. Não compartilhe com o candidato antes da sessão. Dados fictícios, elaborados pelo CCU.',
  }));

  // 1/7 abertura
  pg++;
  sl.push([
    cabecalhoAbertura({ titulo: t(1), selo: 'CCU · Semana 1 · Conduzido pelo entrevistador', nivel: 'Nível quant: MÉDIO', tipo: 'Market Entry', industria: 'Fintech', cliente: 'Startup com VC' }),
    box(L, 1.45, 8.2, 1.85, 'Orientação ao entrevistador',
      'Este case testa se o candidato sai do tamanho de mercado e chega ao resultado, e se percebe que crescer não basta quando o custo de aquisição é alto. O case é conduzido por você: faça as perguntas na ordem das próximas páginas, entregue os dados só quando o candidato pedir ou quando a pergunta exigir, e avalie a capacidade dele de levar o case adiante.\n\n**Duração sugerida:** 30 a 35 minutos de case e 10 de devolutiva. Não mostre este material ao candidato.',
      { size: 10 }),
    box(L, 3.42, 8.2, 3.48, 'Enunciado do case (leia em voz alta)',
      'Nossa cliente é a FemVest, uma fintech alemã financiada por venture capital que quer lançar um neobroker, uma corretora de investimentos 100% pelo celular, na Alemanha em 2026.\n\nA tese das fundadoras é que as mulheres são mal atendidas no investimento de varejo: têm conta em corretora com menos frequência, aportam valores menores e começam a investir mais tarde do que os homens. Ao mesmo tempo, o peso financeiro desse público cresce, puxado por renda, mudança demográfica e herança.\n\nA empresa já tem aprovação regulatória, banco custodiante e parceiro de execução. Falta a estratégia. O conselho contratou vocês para responder: **a FemVest deve lançar o produto e, se sim, como?**',
      { size: 11.5 }),
    box(8.7, 1.45, 4.3, 2.25, 'Desenvolvimento do case',
      '1. Estrutura\n2. Tamanho do mercado\n3. Receita do ano 1\n4. Economia unitária e ponto de equilíbrio\n5. Business case de 3 anos\n6. Estratégia de produto\n7. Entrada no mercado\n8. Recomendação',
      { size: 10.5, text: { paraAfter: 1 } }),
    avaliacao(8.7, 3.82, 4.3, 3.08, '1 = fraco · 5 = excelente · registre a nota na ficha, no fim do arquivo'),
    footer(pg, rod),
  ]);

  // 2/7 estrutura
  pg++;
  sl.push([
    header(t(2)),
    box(L, 1.2, LW, 5.7, 'Estrutura esperada',
      '__Hipótese de trabalho:__ a FemVest deve lançar, desde que cada usuária se pague e o caixa aguente até o ponto de equilíbrio. Para testar, eu olharia:\n\n• __O mercado vale a pena?__\n– Tamanho: mulheres elegíveis sem conta em neobroker\n– Crescimento e intensidade da concorrência\n– Regulação\n• __A FemVest consegue ganhar?__\n– Diferencial percebido pelo público\n– Acesso a canal e custo de aquisição\n– Reação dos neobrokers já estabelecidos\n• __A conta fecha?__\n– Receita: usuárias × receita por usuária\n– Custos: fixo, variável por usuária e de aquisição\n– Ponto de equilíbrio e caixa necessário até lá\n• __Como entrar?__\n– Segmento, proposta de valor, canal, preço e métricas',
      { size: 12 }),
    box(R, 1.2, RW, 5.7, 'Orientação ao entrevistador',
      'Bons candidatos separam as quatro perguntas ao lado antes de calcular. Se a estrutura ignorar custos ou regulação, pergunte: **"O que pode fazer esta tese não fechar?"**\n\nSe o candidato pedir, entregue as informações abaixo:\n\n__Regulação__\n• Licença, custódia e execução já estão resolvidas\n• O pagamento por direcionamento de ordens (PFOF) é proibido na União Europeia pelo artigo 39a do MiFIR. Na Alemanha, a proibição vale integralmente desde 1º de julho de 2026\n\n__Preferências do público__\n• Autosserviço no dia a dia, com apoio consultivo quando necessário\n• Segurança e confiança pesam muito. Taxa baixa é o principal critério de escolha de corretora\n• Necessidades específicas: transparência, ESG, comunidade e educação financeira sem jargão\n\n__Padrão do setor__\n• App em primeiro lugar, liderança de custo, elementos de jogo e execução rápida\n\n__Concorrência__\n• Há neobrokers consolidados, com preço baixo e marca forte, sem foco no público feminino',
      { size: 11 }),
    footer(pg, rod),
  ]);

  // 3/7 mercado e receita
  pg++;
  sl.push([
    header(t(3)),
    box(L, 1.2, LW, 2.95, 'Pergunta: tamanho do mercado',
      '_ Qual é o tamanho do mercado endereçável da FemVest na Alemanha?\n\nEntregue os dados quando o candidato pedir ou começar a estimar:\n• População da Alemanha: 83,5 milhões\n• Participação de mulheres: 50,5%\n• Mulheres de 25 a 50 anos e digitalmente ativas: 36% das mulheres\n• Dessas, sem conta em nenhum neobroker: 72%',
      { size: 10.5 }),
    box(R, 1.2, RW, 2.95, 'Orientação: tamanho do mercado', null),
    el.table(R + 0.1, 1.55, RW - 0.2, [2.9, 1.3, 1.9], [
      ['Etapa', 'Conta', 'Resultado'],
      ['População', '', '83,5 milhões'],
      ['Mulheres', '× 50,5%', '42,2 milhões'],
      ['25 a 50 anos e digitalmente ativas', '× 36%', '15,2 milhões'],
      ['Sem conta em neobroker', '× 72%', { t: '**10,9 milhões**' }],
    ], { size: 9.5, rowH: 0.23 }),
    el.text(R + 0.08, 2.83, RW - 0.16, 1.28, 'Mercado endereçável de ~10,9 milhões de mulheres. Aceite arredondamentos, como 11 milhões. Dê crédito extra se o candidato disser, sem ser perguntado, que o mercado é o gap de 72%, e não a população inteira.', { size: 10 }),

    box(L, 4.25, LW, 2.65, 'Pergunta: receita do ano 1',
      '_ Qual é a receita potencial da FemVest no ano 1?\n\nEntregue os dados quando o candidato pedir:\n• Penetração realista no ano 1: 1,2% do gap\n• Receita média anual por usuária ativa: 21 euros, entre taxa de ordem, repasse de gestoras de ETF e assinatura premium',
      { size: 10.5 }),
    box(R, 4.25, RW, 2.65, 'Orientação: receita do ano 1',
      '• Usuárias no ano 1: 10,9 milhões × 1,2% = ~**131 mil**\n• Receita no ano 1: 131 mil × €21 = ~**€2,75 milhões**\n\nProvoque: **"Isso é muito ou pouco para esta empresa?"** O candidato ainda não tem o custo fixo. O bom candidato pede o dado ou diz que precisa compará-lo com os custos antes de concluir. Passe para a próxima pergunta.',
      { size: 10 }),
    footer(pg, rod),
  ]);

  // 4/7 economia unitária e business case
  pg++;
  sl.push([
    header(t(4)),
    box(L, 1.2, LW, 2.4, 'Pergunta: economia unitária',
      '_ Agora vamos olhar a conta. Cada usuária se paga? Qual é o ponto de equilíbrio?\n\nEntregue os dados:\n• Custo fixo anual, entre plataforma, equipe e compliance: €5,2 milhões\n• Custo variável por usuária ao ano: €7\n• Custo de aquisição por usuária adquirida (CAC): €42',
      { size: 10.5 }),
    box(R, 1.2, RW, 2.4, 'Orientação: economia unitária',
      '• Margem de contribuição: €21 − €7 = **€14 por usuária por ano**\n• Equilíbrio operacional: €5,2 mi ÷ €14 = ~**371 mil usuárias ativas**, cerca de 3,4% do mercado endereçável\n• A usuária leva €42 ÷ €14 = **3 anos** para pagar a própria aquisição\n\nSe o candidato tratar o CAC como custo anual de todas as usuárias, pergunte: "O CAC se repete todo ano para a mesma usuária?"',
      { size: 10 }),

    box(L, 3.7, LW, 3.2, 'Pergunta: business case de 3 anos',
      '_ O conselho projeta 145 mil usuárias ativas no ano 1, 240 mil no ano 2 e 410 mil no ano 3. Qual é o resultado de cada ano? O que isso significa para uma empresa financiada por venture capital?\n\nSe o candidato notar que 145 mil é mais que as 131 mil calculadas antes (1,33% contra 1,2% de penetração), elogie e diga para seguir com a projeção do conselho.\n\nDepois da conta, provoque: **"O que precisaria mudar para o ano 3 fechar no zero?"**',
      { size: 10.5 }),
    box(R, 3.7, RW, 3.2, 'Orientação: business case de 3 anos', null),
    el.table(R + 0.1, 4.03, RW - 0.2, [2.8, 1.1, 1.1, 1.1], [
      [{ t: 'Em € milhões' }, { t: 'Ano 1', align: 'center' }, { t: 'Ano 2', align: 'center' }, { t: 'Ano 3', align: 'center' }],
      ['Usuárias ativas (mil)', { t: '145', align: 'center' }, { t: '240', align: 'center' }, { t: '410', align: 'center' }],
      ['Usuárias novas (mil)', { t: '145', align: 'center' }, { t: '95', align: 'center' }, { t: '170', align: 'center' }],
      ['Margem de contribuição (× €14)', { t: '2,03', align: 'center' }, { t: '3,36', align: 'center' }, { t: '5,74', align: 'center' }],
      ['Resultado antes da aquisição (− €5,2)', { t: '−3,17', align: 'center' }, { t: '−1,84', align: 'center' }, { t: '+0,54', align: 'center' }],
      ['Aquisição (novas × €42)', { t: '−6,09', align: 'center' }, { t: '−3,99', align: 'center' }, { t: '−7,14', align: 'center' }],
      [{ t: '**Resultado do ano**' }, { t: '**−9,26**', align: 'center' }, { t: '**−5,83**', align: 'center' }, { t: '**−6,60**', align: 'center' }],
      [{ t: '**Acumulado**' }, { t: '−9,26', align: 'center' }, { t: '−15,09', align: 'center' }, { t: '**−21,69**', align: 'center' }],
    ], { size: 8.5, rowH: 0.2 }),
    el.text(R + 0.08, 5.78, RW - 0.16, 1.1, 'A operação vira no ano 3, mas o crescimento consome caixa: a FemVest precisa captar pelo menos ~€22 milhões. Quem aplica o CAC sobre todas as ativas chega a −€37,9 milhões (erro). Para zerar o ano 3: receita de ~€30 por usuária e CAC de ~€25.', { size: 9.5 }),
    footer(pg, rod),
  ]);

  // 5/7 produto
  pg++;
  const lab = ['ETFs', 'Ações individuais', 'Poupança e renda fixa', 'Criptomoedas', 'Fundos temáticos e ESG', 'Imóveis', 'Commodities', 'Certificados', 'Títulos públicos'];
  sl.push([
    header(t(5)),
    box(L, 1.2, LW, 5.7, 'Pergunta: estratégia de produto',
      '_ A FemVest encomendou uma pesquisa de uso de produtos. Que estratégia de produto você recomenda? Organize em essencial, desejável e opcional.\n\nMostre o gráfico abaixo ao candidato.',
      { size: 10.5, bodyH: 1.1 }),
    el.chart(L + 0.15, 2.45, LW - 0.3, 4.15, {
      title: 'Uso declarado de produtos de investimento (investidores de até 35 anos, por gênero)',
      labels: lab,
      series: [
        { name: 'Mulheres', color: C.red, values: [79, 52, 36, 15, 34, 18, 10, 5, 8] },
        { name: 'Homens', color: C.blueGrey, values: [81, 71, 33, 41, 22, 21, 15, 11, 9] },
      ],
    }),
    el.text(L + 0.1, 6.6, LW - 0.2, 0.26, 'Dados fictícios, elaborados pelo CCU para este exercício.', { size: 8, color: C.grey }),
    box(R, 1.2, RW, 5.7, 'Orientação: estratégia de produto',
      'A armadilha é priorizar só pelo uso absoluto ou só pela diferença entre mulheres e homens. O bom candidato combina os dois e liga o produto ao modelo de receita sem PFOF.\n\n__Essencial__\n• ETFs com aporte mensal: maior uso nos dois públicos (79% e 81%) e fonte de receita pelo repasse das gestoras\n• Fundos temáticos e ESG: as mulheres usam mais que os homens (34% contra 22%) e o produto atende à necessidade de ESG\n• Poupança e renda fixa: porta de entrada segura (36% contra 33%)\n\n__Desejável__\n• Ações individuais: uso alto (52%), mas abaixo dos homens (71%). Oferecer sem colocar no centro\n• Educação e comunidade dentro do app: respondem à demanda por segurança e linguagem sem jargão\n\n__Opcional__\n• Criptomoedas: a maior diferença contra (15% contra 41%) e risco para a imagem de segurança\n• Imóveis, commodities, certificados e títulos públicos: uso baixo, de 5% a 21%\n\nProvoque: **"Como a FemVest ganha dinheiro sem PFOF?"** Resposta esperada: assinatura premium, repasse de ETF e taxa de ordem baixa.',
      { size: 9.5 }),
    footer(pg, rod),
  ]);

  // 6/7 entrada no mercado
  pg++;
  sl.push([
    header(t(6)),
    box(L, 1.2, 4.3, 5.7, 'Pergunta: entrada no mercado',
      '_ Como a FemVest deve estruturar a entrada no mercado?\n\nPeça que o candidato cubra cinco dimensões:\n• Segmento\n• Proposta de valor\n• Canal\n• Modelo de precificação\n• Métricas de sucesso\n\nDepois, provoque: **"Se o conselho só pudesse acompanhar uma métrica, qual seria?"**',
      { size: 10.5 }),
    box(4.8, 1.2, 8.2, 5.7, 'Orientação: entrada no mercado', null),
    el.table(4.9, 1.55, 8.0, [1.75, 6.25], [
      ['Dimensão', 'Resposta forte'],
      [{ t: '**Segmento**' }, 'Mulheres de 25 a 50 anos, digitalmente ativas e sem conta em neobroker. Começar pelas que já poupam, mas ainda não investem.'],
      [{ t: '**Proposta de valor**' }, 'Investir com segurança e sem jargão: ETFs e ESG no centro, educação dentro do app e apoio humano quando necessário.'],
      [{ t: '**Canal**' }, 'App próprio, comunidade e criadoras de conteúdo de finanças. Parcerias com empregadores, oferecendo a FemVest como benefício, para baixar o CAC de €42.'],
      [{ t: '**Precificação**' }, 'Sem PFOF. Plano gratuito com aporte em ETF, taxa de ordem baixa e assinatura premium (educação, consultoria e relatórios) para subir a receita acima de €21 por usuária.'],
      [{ t: '**Métricas**' }, 'CAC, ativação (primeiro aporte), receita por usuária, conversão ao premium, perda de usuárias por ano e patrimônio por usuária.'],
    ], { size: 9.5, rowH: 0.5 }),
    el.text(4.88, 4.7, 8.04, 1.6, '**Uma métrica para o conselho:** tempo para a usuária se pagar (CAC ÷ margem por usuária). Hoje são 3 anos. É o número que liga canal, preço e caixa.\n\nPenalize propostas que tentam entrar em vários segmentos ao mesmo tempo ou que dependem de receita de PFOF.', { size: 10 }),
    footer(pg, rod),
  ]);

  // 7/7 recomendação
  pg++;
  sl.push([
    header(t(7)),
    box(L, 1.2, LW, 5.7, 'Recomendação',
      '_ Peça ao candidato que resuma a recomendação para o conselho em até 1 minuto.\n\n__Resposta forte:__ lançar, com duas condições, porque o caso base não se paga em 3 anos.\n\n• O mercado é grande: ~10,9 milhões de mulheres endereçáveis. As 410 mil usuárias do ano 3 são só 3,8% delas\n• A operação vira no ano 3 (+€0,5 milhão), mas o custo de aquisição leva o acumulado a −€21,7 milhões\n• **Condição 1:** subir a receita por usuária de €21 para ~€30 com o premium\n• **Condição 2:** baixar o CAC de €42 para ~€25 com comunidade e parcerias com empregadores\n• Com as duas condições, o ano 3 fica perto do zero e o caixa necessário cai para ~€7,6 milhões\n• Captar pelo menos €22 milhões para cobrir o caso base\n\n__O que faria virar não:__ CAC acima de ~€35 ou baixa adesão ao premium depois do piloto.',
      { size: 10.5 }),
    box(R, 1.2, RW, 5.7, 'Riscos e próximos passos',
      '__Riscos__\n• O CAC não cair: cada usuária leva 3 anos para se pagar\n• Perda de usuárias: com 20% ao ano, o ponto de equilíbrio sobe de ~371 mil para ~929 mil ativas, porque parte da margem passa a repor quem saiu\n• Os neobrokers estabelecidos copiarem a proposta, com mais caixa e marca\n• Conversão ao premium abaixo do esperado\n\n__Próximos passos__\n• Testar a disposição a pagar pelo premium antes do lançamento\n• Fazer um piloto com 2 ou 3 empregadores para medir o CAC real\n• Definir um marco de corte, por exemplo rever o plano se o CAC passar de €35 depois de 6 meses\n\n_ Penalize riscos genéricos (crise, câmbio, concorrência em geral) que não se ligam aos números do case.',
      { size: 10.5 }),
    footer(pg, rod),
  ]);

  // padrão de correção
  pg++;
  sl.push([
    header(`${nome} · Padrão de correção`, { titleW: 12 }),
    el.table(L, 1.25, 12.63, [2.1, 3.51, 3.51, 3.51], [
      ['Critério', '1 · Fraco', '3 · Adequado', '5 · Excelente'],
      [{ t: '**Estrutura**' }, 'Lista solta de temas ou framework decorado, sem ligação com a pergunta.', 'Cobre mercado e conta, mas esquece regulação ou custo de aquisição.', 'Hipótese clara e os quatro blocos (mercado, ganhar, conta, entrada), com regulação e CAC previstos.'],
      [{ t: '**Análise e resolução de problemas**' }, 'Erra a cadeia do mercado ou apresenta número sem conta.', 'Acerta mercado, receita e margem, mas aplica o CAC sobre todas as ativas ou não chega ao acumulado.', 'Acerta toda a conta, percebe a diferença entre 131 mil e 145 mil e testa sensibilidade em receita por usuária e CAC.'],
      [{ t: '**Comunicação e postura**' }, 'Calcula em silêncio, perde o fio e reage mal à provocação.', 'Explica as contas, mas o entrevistador precisa puxar os próximos passos.', 'Anuncia o plano antes de calcular, resume a cada etapa e conduz o case.'],
      [{ t: '**Síntese e recomendação**' }, 'Sem recomendação, ou recomendação sem número.', 'Recomenda lançar com números, mas sem condições ou com riscos genéricos.', 'Recomendação condicionada, com o que faria virar não, riscos específicos e próximos passos.'],
    ], { size: 9.5, rowH: 0.55 }),
    box(L, 4.6, LW, 2.3, 'Regras de corte',
      '• Número sem conta à vista: no máximo 2 em Análise\n• CAC aplicado sobre todas as ativas: no máximo 3 em Análise\n• Recomendação sem número: no máximo 2 em Síntese\n• Precificação que depende de PFOF: no máximo 3 em Síntese\n\nNotas 2 e 4 ficam para quem está entre os níveis descritos.',
      { size: 10 }),
    box(R, 4.6, RW, 2.3, 'Marcos do case (já estão na ficha de avaliação)',
      '1. Estrutura com mercado, capacidade de ganhar, conta e entrada\n2. Mercado endereçável ~10,9 milhões, com a cadeia visível\n3. Receita do ano 1 ~€2,75 milhões\n4. Margem de €14 e equilíbrio em ~371 mil ativas\n5. CAC sobre usuárias novas e acumulado de cerca de −€21,7 milhões\n6. Produto priorizado por uso e por diferença, com receita sem PFOF\n7. Recomendação condicionada, com número e riscos específicos',
      { size: 10, text: { paraAfter: 1 } }),
    footer(pg, rod),
  ]);

  const f = ficha({ caseNome: '01 · FemVest', semana: '1', marcos: MARCOS_FEMVEST, pgInicial: pg + 1, rodape: rod });
  sl.push(...f.slides);
  return { title: 'Case 01: FemVest · Casebook do entrevistador', slides: sl };
}

// ============================================================
// FICHA DE AVALIAÇÃO
// ============================================================
const MARCOS_FEMVEST = [
  'Estrutura com mercado, capacidade de ganhar, conta e entrada, incluindo regulação e CAC',
  'Mercado endereçável ~10,9 milhões, com a cadeia visível',
  'Receita do ano 1 ~€2,75 milhões (~131 mil usuárias × €21)',
  'Margem de €14 por usuária e equilíbrio em ~371 mil ativas',
  'CAC aplicado só às usuárias novas e acumulado de cerca de −€21,7 milhões em 3 anos',
  'Produto priorizado por uso e por diferença entre mulheres e homens, com receita sem PFOF',
  'Recomendação condicionada, com número, riscos específicos e o que faria virar não',
];

function ficha(o = {}) {
  const caseNome = o.caseNome ?? '';
  const semana = o.semana ?? '';
  const marcos = o.marcos ?? Array(7).fill('[[Copie aqui um marco do padrão de correção do case]]');
  const rod = o.rodape ?? 'Ciclo de cases · Ficha de avaliação do entrevistador';
  const p0 = o.pgInicial ?? 1;
  const ck = { t: '', align: 'center' };
  const crit = [
    ['**Estrutura**', 'Organiza o problema antes de calcular e cobre o que importa'],
    ['**Análise e resolução de problemas**', 'Pede os dados certos, acerta as contas e interpreta o resultado'],
    ['**Comunicação e postura**', 'Pensa em voz alta, resume a cada etapa e lida bem com provocação'],
    ['**Síntese e recomendação**', 'Fecha com recomendação, número, riscos e próximos passos'],
  ];
  const slide1 = [
    header('Ficha de avaliação do entrevistador', { titleW: 12 }),
    el.table(L, 1.2, 12.63, [3.0, 1.2, 2.6, 2.6, 1.6, 1.63], [
      ['Case', 'Semana', 'Entrevistador(a)', 'Candidato(a)', 'Data', 'Duração'],
      [caseNome, semana, '', '', '', ''],
    ], { size: 10, rowH: 0.3 }),
    el.text(L, 1.82, 12.63, 0.26, 'Escala: 1 fraco · 2 abaixo do esperado · 3 adequado · 4 acima do esperado · 5 excelente. Use o padrão de correção do case para decidir a nota e marque um X na coluna.', { size: 9, color: C.grey, inset: 0, valign: 'middle' }),
    el.table(L, 2.12, 12.63, [3.1, 0.5, 0.5, 0.5, 0.5, 0.5, 7.03], [
      [{ t: 'Critério' }, { t: '1', align: 'center' }, { t: '2', align: 'center' }, { t: '3', align: 'center' }, { t: '4', align: 'center' }, { t: '5', align: 'center' }, { t: 'Evidência: o que o candidato fez ou deixou de fazer' }],
      ...crit.map(c => [{ t: `${c[0]}\n${c[1]}`, size: 9.5 }, ck, ck, ck, ck, ck, '']),
    ], { size: 10, rowH: 0.7 }),
    box(L, 5.72, 4.0, 1.18, 'Nota geral', '[[Média dos 4 critérios, com uma casa decimal]]', { size: 10 }),
    box(4.5, 5.72, 8.48, 1.18, 'Decisão do entrevistador',
      '( ) Avançaria para a próxima fase   ·   ( ) Avançaria com ressalvas   ·   ( ) Não avançaria\n\n[[Em uma frase: por que essa decisão?]]',
      { size: 10.5 }),
    footer(p0, rod),
  ];
  const slide2 = [
    header('Ficha de avaliação do entrevistador (2/2)', { titleW: 12 }),
    el.table(L, 1.2, 12.63, [6.6, 0.8, 0.8, 0.8, 3.63], [
      [{ t: 'Marco do case' }, { t: 'Sim', align: 'center' }, { t: 'Parcial', align: 'center' }, { t: 'Não', align: 'center' }, { t: 'Observação' }],
      ...marcos.map(m => [m, ck, ck, ck, '']),
    ], { size: 9.5, rowH: 0.33 }),
    box(L, 4.1, LW, 1.5, 'Pontos fortes', '[[O que o candidato fez bem e deve repetir]]', { size: 10 }),
    box(R, 4.1, RW, 1.5, 'O que treinar para o próximo case', '[[No máximo três pontos, do mais importante para o menos importante]]', { size: 10 }),
    box(L, 5.72, LW, 1.18, 'Regras de corte aplicadas', '( ) Nenhuma  ·  ( ) Número sem conta  ·  ( ) Recomendação sem número\n( ) Outra do padrão de correção:', { size: 9.5 }),
    box(R, 5.72, RW, 1.18, 'Como enviar',
      'Salve em PDF e envie até **domingo, 23h59**, para **equipeccu@gmail.com**. No assunto: número do case, nome do entrevistador e nome do candidato.',
      { size: 10 }),
    footer(p0 + 1, rod),
  ];
  return { title: `Ficha de avaliação do entrevistador${caseNome ? ' · ' + caseNome : ''}`, slides: [slide1, slide2] };
}

// ============================================================
// TEMPLATE DE CASE
// ============================================================
function template() {
  const rod = 'Ciclo de cases · Case XX: [Nome] · Material do entrevistador';
  const P = s => `[[${s}]]`;
  const sl = [];

  sl.push(capa({
    titulo: 'Case XX: [Nome do case]', geral: '[1-3]', quant: '[1-3]', criat: '[1-3]',
    descricao: [
      '**Tipo de case:**', P('Ex.: Market Entry, Profitability, M&A, Pricing, Growth'), '',
      '**Indústria:**', P('Setor do cliente'), '',
      '**Conceitos testados:**',
      `• ${P('Conceito 1, ex.: dimensionamento de mercado')}`,
      `• ${P('Conceito 2, ex.: ponto de equilíbrio')}`,
      `• ${P('Conceito 3')}`,
    ].join('\n').replace(/\[\[/g, '').replace(/\]\]/g, ''),
    selo: 'CCU · Semana [X] · Conduzido pelo entrevistador',
    aviso: 'Material do entrevistador. Não compartilhe com o candidato antes da sessão. Dados fictícios, elaborados pelo CCU.',
  }));

  sl.push([
    cabecalhoAbertura({ titulo: 'Case XX: [Nome] (1/N)', selo: 'CCU · Semana [X] · Conduzido pelo entrevistador', nivel: 'Nível quant: [BAIXO / MÉDIO / ALTO]', tipo: '[Tipo]', industria: '[Indústria]', cliente: '[Tipo de cliente]' }),
    box(L, 1.45, 8.2, 1.85, 'Orientação ao entrevistador',
      P('O que este case testa, em 2 ou 3 frases. Ex.: "Este case testa se o candidato chega do tamanho de mercado ao resultado."') + '\n\n' + '**Duração sugerida:** 30 a 35 minutos de case e 10 de devolutiva. Não mostre este material ao candidato.',
      { size: 10 }),
    box(L, 3.42, 8.2, 3.48, 'Enunciado do case (leia em voz alta)',
      P('Quem é o cliente, qual é a situação e o que mudou.') + '\n\n' + P('Os fatos que o candidato precisa saber desde o começo. Os dados numéricos ficam para as perguntas.') + '\n\n' + P('A pergunta central do cliente, em negrito. Ex.: "O cliente deve entrar neste mercado e, se sim, como?"'),
      { size: 11.5 }),
    box(8.7, 1.45, 4.3, 2.25, 'Desenvolvimento do case',
      `1. Estrutura\n2. ${P('Pergunta 1')}\n3. ${P('Pergunta 2')}\n4. ${P('Pergunta 3')}\n5. ${P('Pergunta 4')}\n6. Recomendação`,
      { size: 10.5, text: { paraAfter: 1 } }),
    avaliacao(8.7, 3.82, 4.3, 3.08, '1 = fraco · 5 = excelente · registre a nota na ficha, no fim do arquivo'),
    footer(1, rod),
  ]);

  sl.push([
    header('Case XX: [Nome] (2/N)'),
    box(L, 1.2, LW, 5.7, 'Estrutura esperada',
      `__Hipótese de trabalho:__ ${P('a resposta provável para a pergunta do cliente e a condição para ela ser verdade')}\n\n• ${P('Bloco 1 da estrutura')}\n– ${P('O que olhar')}\n– ${P('O que olhar')}\n• ${P('Bloco 2')}\n– ${P('O que olhar')}\n– ${P('O que olhar')}\n• ${P('Bloco 3')}\n– ${P('O que olhar')}\n• ${P('Bloco 4')}\n– ${P('O que olhar')}`,
      { size: 10.5 }),
    box(R, 1.2, RW, 5.7, 'Orientação ao entrevistador',
      `${P('O que diferencia uma estrutura boa de uma fraca neste case, e qual provocação fazer se faltar algo.')}\n\nSe o candidato pedir, entregue as informações abaixo:\n\n${P('Tema, ex.: Regulação')}\n• ${P('Informação qualitativa')}\n\n${P('Tema, ex.: Concorrência')}\n• ${P('Informação qualitativa')}\n\n${P('Tema, ex.: Clientes')}\n• ${P('Informação qualitativa')}`,
      { size: 10 }),
    footer(2, rod),
  ]);

  const perguntaSlide = (n, a, b) => [
    header(`Case XX: [Nome] (${n}/N)`),
    box(L, 1.2, LW, 2.8, `Pergunta: ${a}`,
      `_ ${P('A pergunta, como você vai falar.')}\n\nEntregue os dados quando o candidato pedir:\n• ${P('Dado 1 com unidade')}\n• ${P('Dado 2 com unidade')}`,
      { size: 10.5 }),
    box(R, 1.2, RW, 2.8, `Orientação: ${a}`, null),
    el.table(R + 0.1, 1.55, RW - 0.2, [2.6, 1.8, 1.7], [
      ['Etapa', 'Conta', 'Resultado'],
      [P('Etapa 1'), P('× dado'), P('valor')],
      [P('Etapa 2'), P('× dado'), P('valor')],
      [P('Etapa 3'), P('× dado'), { t: `${P('resposta')}` }],
    ], { size: 9.5, rowH: 0.23 }),
    el.text(R + 0.08, 2.6, RW - 0.16, 1.35, `${P('Leitura do resultado, erros comuns e o que aceitar como arredondamento.')}\n\nProvoque: ${P('"pergunta de provocação"')}`, { size: 10 }),
    box(L, 4.1, LW, 2.8, `Pergunta: ${b}`,
      `_ ${P('A pergunta, como você vai falar.')}\n\nEntregue os dados quando o candidato pedir:\n• ${P('Dado 1')}\n• ${P('Dado 2')}`,
      { size: 10.5 }),
    box(R, 4.1, RW, 2.8, `Orientação: ${b}`,
      `• ${P('Conta 1')} = ${P('resultado')}\n• ${P('Conta 2')} = ${P('resultado')}\n\n${P('O que o candidato precisa perceber. Use tabela quando houver mais de 3 contas.')}\n\nProvoque: ${P('"pergunta de provocação"')}`,
      { size: 10 }),
    footer(n, rod),
  ];
  sl.push(perguntaSlide(3, '[tema da pergunta 1]', '[tema da pergunta 2]'));
  sl.push(perguntaSlide(4, '[tema da pergunta 3]', '[tema da pergunta 4]'));

  sl.push([
    header('Case XX: [Nome] (N/N)'),
    box(L, 1.2, LW, 5.7, 'Recomendação',
      `_ Peça ao candidato que resuma a recomendação para o cliente em até 1 minuto.\n\n__Resposta forte:__ ${P('a decisão em uma frase, com o número que a sustenta')}\n\n• ${P('Argumento 1 com número')}\n• ${P('Argumento 2 com número')}\n• ${P('Condição ou ressalva')}\n\n__O que faria virar não:__ ${P('a condição que inverteria a recomendação')}`,
      { size: 10.5 }),
    box(R, 1.2, RW, 5.7, 'Riscos e próximos passos',
      `__Riscos__\n• ${P('Risco específico da recomendação, ligado a um número do case')}\n• ${P('Risco específico')}\n\n__Próximos passos__\n• ${P('O que testar ou validar primeiro')}\n• ${P('Marco de decisão')}\n\n_ Penalize riscos genéricos (crise, câmbio, concorrência em geral) que não se ligam aos números do case.`,
      { size: 10.5 }),
    footer(5, rod),
  ]);

  sl.push([
    header('Case XX: [Nome] · Padrão de correção', { titleW: 12 }),
    el.table(L, 1.25, 12.63, [2.1, 3.51, 3.51, 3.51], [
      ['Critério', '1 · Fraco', '3 · Adequado', '5 · Excelente'],
      [{ t: '**Estrutura**' }, P('Ex.: lista solta de temas, sem ligação com a pergunta'), P('Ex.: cobre o principal, mas esquece um bloco importante deste case'), P('Ex.: hipótese clara e todos os blocos, com os riscos específicos já previstos')],
      [{ t: '**Análise e resolução de problemas**' }, P('Erro típico que derruba a conta deste case'), P('Acerta as contas principais, mas não chega à conta que decide'), P('Acerta tudo e testa sensibilidade nas duas variáveis que mais pesam')],
      [{ t: '**Comunicação e postura**' }, 'Calcula em silêncio, perde o fio e reage mal à provocação.', 'Explica as contas, mas o entrevistador precisa puxar os próximos passos.', 'Anuncia o plano antes de calcular, resume a cada etapa e conduz o case.'],
      [{ t: '**Síntese e recomendação**' }, 'Sem recomendação, ou recomendação sem número.', P('Recomenda com números, mas sem condição ou com riscos genéricos'), P('Recomendação com número, condição, riscos específicos e próximos passos')],
    ], { size: 9.5, rowH: 0.55 }),
    box(L, 4.6, LW, 2.3, 'Regras de corte',
      `• Número sem conta à vista: no máximo 2 em Análise\n• Recomendação sem número: no máximo 2 em Síntese\n• ${P('Erro específico deste case')}: no máximo ${P('nota')} em ${P('critério')}\n\nNotas 2 e 4 ficam para quem está entre os níveis descritos.`,
      { size: 10 }),
    box(R, 4.6, RW, 2.3, 'Marcos do case (copie para a ficha de avaliação)',
      `1. ${P('Marco de estrutura')}\n2. ${P('Resultado numérico 1')}\n3. ${P('Resultado numérico 2')}\n4. ${P('A conta que decide')}\n5. ${P('Insight qualitativo esperado')}\n6. ${P('Recomendação esperada')}`,
      { size: 10, text: { paraAfter: 1 } }),
    footer(6, rod),
  ]);

  return { title: 'Template de case · Ciclo de cases CCU', slides: sl };
}

module.exports = { femvest, ficha, template, MARCOS_FEMVEST };
