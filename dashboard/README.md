# Dashboard Power BI — ASIS Municipal

## Páginas del dashboard

| Página | Contenido |
|--------|-----------|
| Resumen ejecutivo | KPIs principales del municipio con semáforo de alertas |
| Demografía | Pirámide poblacional, tendencia histórica, distribución urbano/rural |
| Mortalidad | Primeras causas, tasas por sexo y grupo etario, tendencia anual |
| Morbilidad | Top eventos SIVIGILA, canal endémico dengue, desnutrición aguda |
| Determinantes | IPM, coberturas de servicios, vacunación, indicadores nutricionales |

## Fuente de datos para Power BI

Conectar Power BI a:
- Archivo `data/processed/reporte_asis.xlsx` para análisis estático
- Vista `vw_asis_indicadores` en PostgreSQL para análisis dinámico

## Medidas DAX principales

```dax
Tasa Mortalidad General =
DIVIDE(
    SUM(mortalidad_municipal[numero_muertes]),
    SUM(poblacion_municipal[poblacion_total])
) * 100000

Indice Envejecimiento =
DIVIDE(
    SUM(poblacion_municipal[poblacion_60_mas]),
    SUM(poblacion_municipal[poblacion_menor5])
) * 100

Variacion Anual Muertes =
VAR añoActual = MAX(mortalidad_municipal[año])
VAR añoAnterior = añoActual - 1
VAR muertesActual = CALCULATE(SUM(mortalidad_municipal[numero_muertes]), mortalidad_municipal[año] = añoActual)
VAR muertesAnterior = CALCULATE(SUM(mortalidad_municipal[numero_muertes]), mortalidad_municipal[año] = añoAnterior)
RETURN DIVIDE(muertesActual - muertesAnterior, muertesAnterior) * 100
```
