"""
Modelo de previsão de falta em consulta (no-show) — versão mais simples que funciona.

Escolhas deliberadas, e cada uma tem defesa:
  - Regressão logística, não gradient boosting: o cliente precisa entender
    POR QUE um caso foi apontado, não só receber o score.
  - Split TEMPORAL, não aleatório: existe ordem no dado. Split aleatório
    colocaria consultas futuras no treino e inflaria a performance.
  - Avaliação contra BASELINE, não só métrica absoluta: o que importa é o
    ganho sobre a regra que o cliente já usa.

Rode:  python3 02_modelo.py
"""

import sqlite3
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler

AQUI = Path(__file__).parent

# ------------------------------------------------------------------ 1. CARGA
# A extração e a agregação ficam no SQL; o Python recebe a base já no grão
# da análise. Com 1,2 milhão de linhas isso cabe em memória sem problema —
# não há necessidade de ferramenta distribuída.
con = sqlite3.connect(AQUI / "saude.db")
df = pd.read_sql_query((AQUI / "01_extracao.sql").read_text(encoding="utf-8"), con)
con.close()

print(f"Linhas carregadas : {len(df):,}")
print(f"Taxa de falta     : {df['alvo'].mean():.1%}")

# ------------------------------------------------------- 2. CHECAGEM DE BASE
# Ritual mínimo antes de modelar. Problema encontrado aqui é barato;
# problema descoberto depois do modelo é caro.
print("\n--- Checagem ---")
print(f"Nulos            : {df.isna().sum().sum()}")
print(f"Chave duplicada  : {df['id_consulta'].duplicated().sum()}")

# ------------------------------------------------------- 3. SPLIT TEMPORAL
# Treina no passado, testa no futuro — é assim que o modelo vai ser usado.
corte = df["data_agendamento"].quantile(0.70)
treino = df[df["data_agendamento"] <= corte]
teste = df[df["data_agendamento"] > corte]

FEATURES = [
    "dias_espera", "primeira_consulta", "idade", "dia_semana",
    "turno_manha", "esp_pediatria", "esp_ortopedia",
    "hist_taxa_falta", "hist_qtd_consultas",
]

X_tr, y_tr = treino[FEATURES], treino["alvo"]
X_te, y_te = teste[FEATURES], teste["alvo"]

print(f"\nTreino : {len(X_tr):,} consultas")
print(f"Teste  : {len(X_te):,} consultas")

# ------------------------------------------------------------- 4. BASELINES
# A régua honesta. Um modelo que não bate isso não deveria ir para produção.
print("\n--- Baselines ---")

# Baseline 1: prever que ninguém falta (classe majoritária)
acerto_majoritaria = 1 - y_te.mean()
print(f"Classe majoritária  — acurácia : {acerto_majoritaria:.1%}")
print("  (observe: alta acurácia e inútil — não identifica ninguém)")

# Baseline 2: a regra de negócio plausível — espera longa = risco
regra = (X_te["dias_espera"] > 30).astype(int)
auc_regra = roc_auc_score(y_te, X_te["dias_espera"])
print(f"Regra 'espera > 30' — AUC      : {auc_regra:.3f}")

# --------------------------------------------------------------- 5. MODELO
# Padronização ajustada SÓ no treino e aplicada no teste.
# Ajustar na base inteira vazaria informação do teste para o treino.
scaler = StandardScaler().fit(X_tr)

modelo = LogisticRegression(max_iter=1000, class_weight="balanced")
modelo.fit(scaler.transform(X_tr), y_tr)

prob = modelo.predict_proba(scaler.transform(X_te))[:, 1]
auc = roc_auc_score(y_te, prob)

print("\n--- Modelo: regressão logística ---")
print(f"AUC no teste : {auc:.3f}")
print(f"Ganho sobre a regra de negócio : {auc - auc_regra:+.3f}")

print("\n" + classification_report(y_te, (prob > 0.5).astype(int),
                                   target_names=["compareceu", "faltou"],
                                   digits=3))

# ------------------------------------------------- 6. LEITURA DOS COEFICIENTES
# A razão de ter escolhido logística: o resultado é explicável.
# Coeficiente positivo = aumenta a chance de falta.
coef = (
    pd.DataFrame({"variavel": FEATURES, "coeficiente": modelo.coef_[0]})
    .assign(efeito=lambda d: d["coeficiente"].abs())
    .sort_values("efeito", ascending=False)
    .drop(columns="efeito")
)
print("--- Coeficientes (padronizados) ---")
print(coef.to_string(index=False))

# ------------------------------------------------------- 7. USO PRÁTICO
# Score sem regra de decisão não serve. A pergunta do cliente é:
# "a quem eu ligo para confirmar?" — e ele tem capacidade limitada.
teste_out = teste.copy()
teste_out["prob_falta"] = prob
capacidade = int(len(teste_out) * 0.10)       # consegue ligar para 10%
top = teste_out.nlargest(capacidade, "prob_falta")

precisao_top = top["alvo"].mean()
print(f"\n--- Priorização operacional (capacidade de 10%) ---")
print(f"Consultas priorizadas     : {capacidade:,}")
print(f"Taxa de falta no grupo    : {precisao_top:.1%}")
print(f"Taxa de falta geral       : {y_te.mean():.1%}")
print(f"Ganho (lift)              : {precisao_top / y_te.mean():.2f}x")
print("\nLeitura para o cliente: ligando para os 10% mais prováveis, a equipe")
print(f"encontra {precisao_top:.0%} de faltantes em vez de {y_te.mean():.0%} ligando ao acaso.")
