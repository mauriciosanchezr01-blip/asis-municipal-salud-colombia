-- =============================================================================
-- consultas_asis.sql
-- Proyecto: ASIS Municipal - Salud Colombia
-- Autor: Mauricio Sánchez
-- Descripción: Consultas SQL para análisis de situación de salud municipal
-- =============================================================================


-- -----------------------------------------------------------------------------
-- 1. TABLAS PRINCIPALES
-- -----------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS poblacion_municipal (
    id                      SERIAL PRIMARY KEY,
    municipio               VARCHAR(100),
    codigo_divipola         VARCHAR(10),
    departamento            VARCHAR(100),
    año                     INTEGER,
    poblacion_total         INTEGER,
    poblacion_masculina     INTEGER,
    poblacion_femenina      INTEGER,
    poblacion_urbana        INTEGER,
    poblacion_rural         INTEGER,
    poblacion_menor5        INTEGER,
    poblacion_5_14          INTEGER,
    poblacion_15_44         INTEGER,
    poblacion_45_59         INTEGER,
    poblacion_60_mas        INTEGER
);

CREATE TABLE IF NOT EXISTS mortalidad_municipal (
    id                      SERIAL PRIMARY KEY,
    municipio               VARCHAR(100),
    codigo_divipola         VARCHAR(10),
    departamento            VARCHAR(100),
    año                     INTEGER,
    causa_muerte            VARCHAR(200),
    codigo_cie10            VARCHAR(20),
    grupo_causa             VARCHAR(100),
    sexo                    CHAR(1),
    grupo_etario            VARCHAR(50),
    numero_muertes          INTEGER,
    tasa_mortalidad_x100mil NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS morbilidad_eventos (
    id                      SERIAL PRIMARY KEY,
    municipio               VARCHAR(100),
    codigo_divipola         VARCHAR(10),
    departamento            VARCHAR(100),
    año                     INTEGER,
    semana_epidemiologica   INTEGER,
    evento                  VARCHAR(200),
    codigo_sivigila         VARCHAR(20),
    grupo_etario            VARCHAR(50),
    sexo                    CHAR(1),
    casos_confirmados       INTEGER,
    casos_probables         INTEGER,
    casos_descartados       INTEGER,
    tasa_incidencia_x100mil NUMERIC(10,2)
);

CREATE TABLE IF NOT EXISTS determinantes_sociales (
    id                      SERIAL PRIMARY KEY,
    municipio               VARCHAR(100),
    codigo_divipola         VARCHAR(10),
    departamento            VARCHAR(100),
    año                     INTEGER,
    indicador               VARCHAR(200),
    valor                   NUMERIC(10,2),
    unidad                  VARCHAR(50),
    fuente                  VARCHAR(100)
);


-- -----------------------------------------------------------------------------
-- 2. INDICADORES DEMOGRÁFICOS
-- -----------------------------------------------------------------------------

-- Pirámide poblacional del último año disponible
SELECT
    'Menor de 5 años'   AS grupo_etario, SUM(poblacion_menor5) AS total
    FROM poblacion_municipal WHERE año = 2023
UNION ALL SELECT '5 a 14 años',  SUM(poblacion_5_14)   FROM poblacion_municipal WHERE año = 2023
UNION ALL SELECT '15 a 44 años', SUM(poblacion_15_44)  FROM poblacion_municipal WHERE año = 2023
UNION ALL SELECT '45 a 59 años', SUM(poblacion_45_59)  FROM poblacion_municipal WHERE año = 2023
UNION ALL SELECT '60 años y más',SUM(poblacion_60_mas) FROM poblacion_municipal WHERE año = 2023
ORDER BY grupo_etario;


-- Índice de envejecimiento por municipio
SELECT
    municipio,
    año,
    ROUND(poblacion_60_mas::NUMERIC / NULLIF(poblacion_menor5, 0) * 100, 2) AS indice_envejecimiento,
    ROUND(poblacion_urbana::NUMERIC / NULLIF(poblacion_total, 0) * 100, 2)  AS porcentaje_urbano
FROM poblacion_municipal
WHERE año = 2023
ORDER BY indice_envejecimiento DESC;


-- -----------------------------------------------------------------------------
-- 3. ANÁLISIS DE MORTALIDAD
-- -----------------------------------------------------------------------------

-- Primeras causas de muerte con tasa ajustada
SELECT
    m.causa_muerte,
    m.grupo_causa,
    m.codigo_cie10,
    SUM(m.numero_muertes)                                           AS total_muertes,
    ROUND(SUM(m.numero_muertes)::NUMERIC / p.poblacion_total * 100000, 2) AS tasa_x100mil
FROM mortalidad_municipal m
JOIN poblacion_municipal p
    ON m.municipio = p.municipio AND m.año = p.año
WHERE m.año = 2023
GROUP BY m.causa_muerte, m.grupo_causa, m.codigo_cie10, p.poblacion_total
ORDER BY total_muertes DESC
LIMIT 10;


-- Mortalidad por grupo de causa y sexo
SELECT
    grupo_causa,
    sexo,
    SUM(numero_muertes)                                     AS total_muertes,
    ROUND(SUM(numero_muertes) * 100.0 / SUM(SUM(numero_muertes)) OVER(), 2) AS porcentaje
FROM mortalidad_municipal
WHERE año = 2023
GROUP BY grupo_causa, sexo
ORDER BY total_muertes DESC;


-- Tendencia de mortalidad por año
SELECT
    año,
    SUM(numero_muertes)             AS total_muertes,
    COUNT(DISTINCT causa_muerte)    AS causas_registradas
FROM mortalidad_municipal
GROUP BY año
ORDER BY año;


-- Mortalidad en menores de 5 años
SELECT
    año,
    SUM(numero_muertes) AS muertes_menores_5
FROM mortalidad_municipal
WHERE grupo_etario = 'Menor de 5 años'
GROUP BY año
ORDER BY año;


-- -----------------------------------------------------------------------------
-- 4. ANÁLISIS DE MORBILIDAD Y SIVIGILA
-- -----------------------------------------------------------------------------

-- Top eventos de notificación obligatoria
SELECT
    evento,
    codigo_sivigila,
    SUM(casos_confirmados)                                          AS total_confirmados,
    SUM(casos_probables)                                            AS total_probables,
    ROUND(AVG(tasa_incidencia_x100mil), 2)                          AS tasa_promedio_x100mil
FROM morbilidad_eventos
WHERE año = 2023
GROUP BY evento, codigo_sivigila
ORDER BY total_confirmados DESC;


-- Canal endémico: casos de dengue por semana epidemiológica
SELECT
    semana_epidemiologica,
    SUM(casos_confirmados)  AS casos_confirmados,
    SUM(casos_probables)    AS casos_probables
FROM morbilidad_eventos
WHERE evento = 'Dengue'
  AND año = 2023
GROUP BY semana_epidemiologica
ORDER BY semana_epidemiologica;


-- Desnutrición aguda en menores de 5 años por semana
SELECT
    semana_epidemiologica,
    sexo,
    SUM(casos_confirmados) AS casos
FROM morbilidad_eventos
WHERE evento = 'Desnutrición aguda'
  AND grupo_etario = 'Menor de 5 años'
  AND año = 2023
GROUP BY semana_epidemiologica, sexo
ORDER BY semana_epidemiologica;


-- -----------------------------------------------------------------------------
-- 5. DETERMINANTES SOCIALES
-- -----------------------------------------------------------------------------

-- Indicadores clave por año
SELECT
    año,
    indicador,
    valor,
    unidad,
    fuente
FROM determinantes_sociales
WHERE indicador IN (
    'Índice de pobreza multidimensional (IPM)',
    'Cobertura de acueducto',
    'Cobertura de alcantarillado',
    'Tasa de mortalidad infantil x1000',
    'Cobertura vacunación DPT',
    'Prevalencia de desnutrición crónica'
)
ORDER BY indicador, año;


-- Semáforo de indicadores críticos
SELECT
    indicador,
    valor,
    unidad,
    CASE
        WHEN indicador LIKE '%mortalidad infantil%' AND valor > 15  THEN 'CRÍTICO'
        WHEN indicador LIKE '%mortalidad infantil%' AND valor > 10  THEN 'ALERTA'
        ELSE 'ACEPTABLE'
    END AS semaforo_mortalidad_infantil,
    CASE
        WHEN indicador LIKE '%vacunación%' AND valor < 80  THEN 'CRÍTICO'
        WHEN indicador LIKE '%vacunación%' AND valor < 90  THEN 'ALERTA'
        ELSE 'ACEPTABLE'
    END AS semaforo_vacunacion
FROM determinantes_sociales
WHERE año = 2023
ORDER BY indicador;


-- -----------------------------------------------------------------------------
-- 6. VISTA CONSOLIDADA PARA POWER BI
-- -----------------------------------------------------------------------------

CREATE OR REPLACE VIEW vw_asis_indicadores AS
SELECT
    d.municipio,
    d.departamento,
    d.año,
    d.indicador,
    d.valor,
    d.unidad,
    d.fuente,
    CASE
        WHEN d.indicador LIKE '%pobreza%'           THEN 'Determinante social'
        WHEN d.indicador LIKE '%acueducto%'         THEN 'Determinante social'
        WHEN d.indicador LIKE '%vacun%'             THEN 'Salud pública'
        WHEN d.indicador LIKE '%mortalidad%'        THEN 'Mortalidad'
        WHEN d.indicador LIKE '%desnutrición%'      THEN 'Nutrición'
        ELSE 'Otro'
    END AS dimension_asis
FROM determinantes_sociales d
ORDER BY d.año DESC, d.indicador;
