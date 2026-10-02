-- =============================================================
-- Extração da base de modelagem — previsão de falta em consulta
--
-- Decisão de desenho: o histórico de faltas do paciente é calculado
-- AQUI, no banco, com window function. Dois motivos:
--   1) o banco é melhor que o Python em agregação sobre volume
--   2) a janela com ROWS ... PRECEDING garante que só entra informação
--      ANTERIOR à consulta — sem isso, haveria vazamento de dados
-- =============================================================

SELECT
    c.id_consulta,
    c.dias_espera,
    c.primeira_consulta,
    c.dia_semana,
    p.idade,

    -- turno e especialidade como variáveis binárias, já prontas para o modelo
    CASE WHEN c.turno = 'manha' THEN 1 ELSE 0 END          AS turno_manha,
    CASE WHEN c.especialidade = 'pediatria' THEN 1 ELSE 0 END AS esp_pediatria,
    CASE WHEN c.especialidade = 'ortopedia' THEN 1 ELSE 0 END AS esp_ortopedia,

    -- HISTÓRICO DO PACIENTE, olhando apenas o passado.
    -- A cláusula de frame exclui a linha atual (termina em 1 PRECEDING),
    -- então a consulta sendo prevista não entra no próprio histórico.
    COALESCE(
        AVG(CAST(c.faltou AS REAL)) OVER (
            PARTITION BY c.id_paciente
            ORDER BY c.data_agendamento
            ROWS BETWEEN 10 PRECEDING AND 1 PRECEDING
        ), 0.0
    ) AS hist_taxa_falta,

    COUNT(*) OVER (
        PARTITION BY c.id_paciente
        ORDER BY c.data_agendamento
        ROWS BETWEEN 10 PRECEDING AND 1 PRECEDING
    ) AS hist_qtd_consultas,

    c.data_agendamento,
    c.faltou                                                AS alvo

FROM consultas c
INNER JOIN pacientes p
        ON p.id_paciente = c.id_paciente

-- Filtro de qualidade aplicado no banco, antes de trazer para o Python:
-- espera negativa é erro de cadastro; acima de 180 dias é caso atípico.
WHERE c.dias_espera BETWEEN 0 AND 180
;
