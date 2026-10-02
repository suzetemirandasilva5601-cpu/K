"""
Gera uma base sintética em SQLite para o projeto rodar de ponta a ponta.

Contexto: setor de Saúde — previsão de falta em consulta agendada (no-show).
Volume: 1,2 milhão de consultas, para reproduzir a escala real do projeto.

Rode uma vez:  python3 00_gerar_base.py
"""

import sqlite3
from pathlib import Path

import numpy as np

N_PACIENTES = 120_000
N_CONSULTAS = 1_200_000
DB = Path(__file__).parent / "saude.db"

rng = np.random.default_rng(42)

print(f"Gerando {N_PACIENTES:,} pacientes e {N_CONSULTAS:,} consultas...")

# ---------------------------------------------------------------- pacientes
pacientes = {
    "id_paciente": np.arange(1, N_PACIENTES + 1),
    "idade": rng.integers(1, 95, N_PACIENTES),
    "sexo": rng.choice(["F", "M"], N_PACIENTES),
    "bairro": rng.choice([f"B{i:02d}" for i in range(1, 31)], N_PACIENTES),
}

# ---------------------------------------------------------------- consultas
id_paciente = rng.integers(1, N_PACIENTES + 1, N_CONSULTAS)
dias_espera = rng.gamma(shape=2.0, scale=12.0, size=N_CONSULTAS).astype(int)
turno = rng.choice(["manha", "tarde"], N_CONSULTAS, p=[0.55, 0.45])
dia_semana = rng.integers(0, 5, N_CONSULTAS)          # 0=seg ... 4=sex
especialidade = rng.choice(
    ["clinica", "pediatria", "ortopedia", "cardio", "derma"],
    N_CONSULTAS, p=[0.35, 0.2, 0.2, 0.15, 0.10],
)
primeira_consulta = rng.choice([0, 1], N_CONSULTAS, p=[0.75, 0.25])

# Probabilidade de falta construída com relações reais e conhecidas da literatura:
# espera longa aumenta falta; primeira consulta falta mais; jovem falta mais.
idade_por_consulta = pacientes["idade"][id_paciente - 1]

# Efeito aleatório por paciente: alguns pacientes simplesmente faltam mais que
# outros, de forma persistente. É isso que torna o HISTÓRICO do paciente
# preditivo, e é o que se observa em base real de saúde.
propensao_paciente = rng.normal(0, 0.9, N_PACIENTES)
efeito_paciente = propensao_paciente[id_paciente - 1]

logito = (
    -1.9
    + 0.022 * np.clip(dias_espera, 0, 90)      # quanto mais espera, mais falta
    + 0.55 * primeira_consulta                 # primeira vez falta mais
    - 0.012 * idade_por_consulta               # idoso falta menos
    + 0.20 * (turno == "manha")                # manhã falta um pouco mais
    + 0.15 * (dia_semana == 0)                 # segunda-feira
    + efeito_paciente                          # propensão individual persistente
    + rng.normal(0, 0.45, N_CONSULTAS)         # ruído irredutível
)
prob = 1 / (1 + np.exp(-logito))
faltou = (rng.random(N_CONSULTAS) < prob).astype(int)

consultas = {
    "id_consulta": np.arange(1, N_CONSULTAS + 1),
    "id_paciente": id_paciente,
    "data_agendamento": 1 + rng.integers(0, 700, N_CONSULTAS),   # dia-índice
    "dias_espera": dias_espera,
    "turno": turno,
    "dia_semana": dia_semana,
    "especialidade": especialidade,
    "primeira_consulta": primeira_consulta,
    "faltou": faltou,
}

# ---------------------------------------------------------------- gravação
DB.unlink(missing_ok=True)
con = sqlite3.connect(DB)

con.execute("""
CREATE TABLE pacientes (
    id_paciente INTEGER PRIMARY KEY,
    idade       INTEGER,
    sexo        TEXT,
    bairro      TEXT
)""")
con.execute("""
CREATE TABLE consultas (
    id_consulta       INTEGER PRIMARY KEY,
    id_paciente       INTEGER,
    data_agendamento  INTEGER,
    dias_espera       INTEGER,
    turno             TEXT,
    dia_semana        INTEGER,
    especialidade     TEXT,
    primeira_consulta INTEGER,
    faltou            INTEGER
)""")

con.executemany(
    "INSERT INTO pacientes VALUES (?,?,?,?)",
    zip(pacientes["id_paciente"].tolist(), pacientes["idade"].tolist(),
        pacientes["sexo"].tolist(), pacientes["bairro"].tolist()),
)
con.executemany(
    "INSERT INTO consultas VALUES (?,?,?,?,?,?,?,?,?)",
    zip(consultas["id_consulta"].tolist(), consultas["id_paciente"].tolist(),
        consultas["data_agendamento"].tolist(), consultas["dias_espera"].tolist(),
        consultas["turno"].tolist(), consultas["dia_semana"].tolist(),
        consultas["especialidade"].tolist(), consultas["primeira_consulta"].tolist(),
        consultas["faltou"].tolist()),
)
con.execute("CREATE INDEX idx_consultas_paciente ON consultas(id_paciente)")
con.commit()

total, taxa = con.execute("SELECT COUNT(*), AVG(faltou) FROM consultas").fetchone()
con.close()

print(f"OK  {DB.name}")
print(f"    consultas      : {total:,}")
print(f"    taxa de falta  : {taxa:.1%}")
