# Currículo Profissional

## 👤 Sobre Mim

[Insira aqui seu nome completo e título profissional]

---

## 📧 Contato

- **Email:** [seu.email@exemplo.com]
- **LinkedIn:** [linkedin.com/in/seu-perfil]
- **GitHub:** [github.com/seu-usuario]
- **Localização:** [Cidade, Estado]
- **Telefone:** [(XX) XXXXX-XXXX]

---

## 🎯 Elevator Pitch

### Versão 30 segundos
[Insira aqui um resumo executivo de 2-3 linhas destacando sua expertise principal e valor único]

### Versão 60 segundos
[Insira aqui um resumo de 4-6 linhas incluindo background, experiência chave e principais realizações]

### Versão 90 segundos
[Insira aqui um resumo mais detalhado de 8-10 linhas cobrindo trajetória completa, expertise técnica e impacto de negócio]

---

## 💼 Áreas de Expertise

- **[Área Principal 1]:** [Breve descrição]
- **[Área Principal 2]:** [Breve descrição]
- **[Área Principal 3]:** [Breve descrição]
- **[Área Principal 4]:** [Breve descrição]

---

## 🏆 Principais Realizações

1. **[Realização 1]:** [Descrição com métricas quantificadas]
2. **[Realização 2]:** [Descrição com métricas quantificadas]
3. **[Realização 3]:** [Descrição com métricas quantificadas]
4. **[Realização 4]:** [Descrição com métricas quantificadas]
5. **[Realização 5]:** [Descrição com métricas quantificadas]

---

## 📄 Briefing Pré-Entrevista (leia este primeiro)

**[Briefing-Pre-Entrevista-ATY.pdf](Briefing-Pre-Entrevista-ATY.pdf)** — 7 páginas de consulta rápida, para revisar na véspera. Quatro blocos: como responder sobre o projeto em Python/SQL, como responder sobre modelagem financeira, o projeto de malha logística da ATY (frentes, planilha de negociação, split payment) e o que se espera de um júnior. Termina com colinha de números e fórmulas.

Fonte em [briefing/](briefing/).

---

## 📐 Frameworks de Case — Varejo

**[Frameworks-Varejo-ATY.pdf](Frameworks-Varejo-ATY.pdf)** — 8 páginas com quatro frameworks em diagramas de caixa, desenháveis à mão em 60 segundos:

- **Retail Profitability** — lucro decomposto até a cadeia multiplicativa (tráfego × conversão × ticket)
- **Omnichannel** — cliente, oferta, entrega, econômica e habilitadores (com atribuição de venda como ponto cego)
- **Retail Market Entry** — mercado, direito de ganhar, forma de entrada, viabilidade e risco (com curva de maturação e canibalização)
- **Retail Market Sizing** — bottom-up e top-down reconciliados, funil TAM/SAM/SOM e âncoras do Brasil

Cada um traz a árvore completa, a versão de 30 segundos, as perguntas de clarificação e a armadilha típica. Fonte em [frameworks/](frameworks/).

---

## 🔧 Como regerar os PDFs

```bash
bash setup_build.sh          # dependências + fontes DejaVu

python3 build_pdf.py         # relatório completo (capa + índice + 13 capítulos)

python3 build_doc.py briefing/briefing-pre-entrevista.md \
    Briefing-Pre-Entrevista-ATY.pdf "Briefing Pré-Entrevista — ATY Consulting"

python3 build_doc.py frameworks/frameworks-varejo.md \
    Frameworks-Varejo-ATY.pdf "Frameworks de Case — Varejo"
```

---

## 🐍 Projeto Python + SQL (rodável)

**[projeto-python/](projeto-python/)** — implementação completa do projeto equivalente ao do currículo, na forma mais simples que funciona: previsão de falta em consulta sobre 1,2 milhão de registros, com extração em SQL (window function sem vazamento), regressão logística e comparação contra baseline.

```bash
pip install pandas numpy scikit-learn
python3 projeto-python/00_gerar_base.py   # base sintética, 1,2M consultas
python3 projeto-python/02_modelo.py       # AUC 0,681 vs 0,586 da regra
```

O [README do projeto](projeto-python/README.md) traz o roteiro de resposta em primeira pessoa para cada pergunta provável de entrevista.

---

## 📕 Relatório ATY Consulting

**[Relatorio-ATY-Consulting.pdf](Relatorio-ATY-Consulting.pdf)** — relatório de preparação para o processo seletivo da [ATY Consulting](https://www.atyconsulting.com/), com 91 páginas: análise da empresa (4 ofertas, 3 valores, 4 clientes), perfil dos sócios e pontos de conexão, diagnóstico de fit e gaps, 7 cases STAR, 45 perguntas (técnicas e de fit) com respostas, pitches e plano de 30 dias.

Os documentos-fonte em Markdown estão em **[preparacao-aty/](preparacao-aty/)**. Para regerar o PDF após editá-los:

```bash
pip install weasyprint markdown pygments
python3 build_pdf.py
```

---

## 📂 Estrutura do Repositório

- **[curriculo/experiencia.md](curriculo/experiencia.md)** - Histórico profissional detalhado
- **[curriculo/projetos/](curriculo/projetos/)** - Portfólio de projetos técnicos
- **[curriculo/cases/](curriculo/cases/)** - Cases estruturados no formato STAR
- **[curriculo/formacao.md](curriculo/formacao.md)** - Formação acadêmica e certificações
- **[curriculo/skills.md](curriculo/skills.md)** - Competências técnicas e ferramentas
- **[curriculo/certificacoes/](curriculo/certificacoes/)** - Certificados e cursos

---

## 🎓 Formação Resumida

**[Nome da Instituição]**
- [Grau] em [Curso] - [Ano Início] - [Ano Conclusão]

**[Nome da Instituição]**
- [Grau] em [Curso] - [Ano Início] - [Ano Conclusão]

---

## 🛠️ Stack Técnico Principal

**Linguagens:** [Python, R, SQL, etc.]

**Frameworks & Libraries:** [Scikit-learn, TensorFlow, Pandas, etc.]

**Ferramentas:** [Databricks, Power BI, Git, etc.]

**Cloud & Infra:** [AWS, GCP, Azure, Docker, etc.]

**Metodologias:** [Agile, MLOps, A/B Testing, etc.]

---

## 📊 Setores de Atuação

- [Setor 1]
- [Setor 2]
- [Setor 3]
- [Setor 4]

---

## 🌐 Idiomas

- **[Idioma 1]:** [Nível]
- **[Idioma 2]:** [Nível]
- **[Idioma 3]:** [Nível]

---

## 📫 Como me encontrar

[Breve parágrafo convidativo explicando como as pessoas podem entrar em contato]

---

*Última atualização: [Data]*
