# =============================================================================
# reporte_asis.py
# Proyecto: ASIS Municipal - Salud Colombia
# Autor: Mauricio Sánchez
# Descripción: Generación de reporte ejecutivo ASIS en Excel
# =============================================================================

import pandas as pd
import numpy as np
import os
from datetime import datetime

MUNICIPIO       = "Ciudad Bolívar"
DEPARTAMENTO    = "Antioquia"
AÑO_ANALISIS    = 2023
RUTA_REPORTE    = "data/processed/reporte_asis.xlsx"


def generar_reporte():
    """Genera el reporte ASIS completo en Excel con múltiples hojas."""

    poblacion    = pd.read_csv("data/raw/poblacion_municipal.csv", encoding="utf-8")
    mortalidad   = pd.read_csv("data/raw/mortalidad_municipal.csv", encoding="utf-8")
    morbilidad   = pd.read_csv("data/raw/morbilidad_eventos.csv", encoding="utf-8")
    determinantes = pd.read_csv("data/raw/determinantes_sociales.csv", encoding="utf-8")

    mort_año  = mortalidad[mortalidad["año"] == AÑO_ANALISIS]
    morb_año  = morbilidad[morbilidad["año"] == AÑO_ANALISIS]
    det_año   = determinantes[determinantes["año"] == AÑO_ANALISIS]

    top_causas_muerte = (
        mort_año.groupby(["causa_muerte", "grupo_causa"])["numero_muertes"]
        .sum().reset_index()
        .sort_values("numero_muertes", ascending=False)
        .rename(columns={"causa_muerte": "Causa", "grupo_causa": "Grupo", "numero_muertes": "Defunciones"})
    )

    top_eventos_morbilidad = (
        morb_año.groupby(["evento", "codigo_sivigila"])["casos_confirmados"]
        .sum().reset_index()
        .sort_values("casos_confirmados", ascending=False)
        .rename(columns={"evento": "Evento", "codigo_sivigila": "Código SIVIGILA", "casos_confirmados": "Casos confirmados"})
    )

    mortalidad_sexo = (
        mort_año.groupby("sexo")["numero_muertes"]
        .sum().reset_index()
        .rename(columns={"sexo": "Sexo", "numero_muertes": "Defunciones"})
    )

    mortalidad_grupo = (
        mort_año.groupby("grupo_etario")["numero_muertes"]
        .sum().reset_index()
        .sort_values("numero_muertes", ascending=False)
        .rename(columns={"grupo_etario": "Grupo etario", "numero_muertes": "Defunciones"})
    )

    tendencia = (
        mortalidad.groupby("año")["numero_muertes"]
        .sum().reset_index()
        .rename(columns={"año": "Año", "numero_muertes": "Total defunciones"})
    )

    os.makedirs("data/processed", exist_ok=True)

    hojas = {
        "Portada"                   : pd.DataFrame({
            "Campo": ["Municipio", "Departamento", "Año de análisis", "Fecha de generación", "Autor"],
            "Valor": [MUNICIPIO, DEPARTAMENTO, AÑO_ANALISIS, datetime.today().strftime("%Y-%m-%d"), "Mauricio Sánchez"]
        }),
        "Determinantes sociales"    : det_año[["indicador", "valor", "unidad", "fuente"]].rename(columns={
            "indicador": "Indicador", "valor": "Valor", "unidad": "Unidad", "fuente": "Fuente"
        }),
        "Top causas de muerte"      : top_causas_muerte,
        "Mortalidad por sexo"       : mortalidad_sexo,
        "Mortalidad por grupo etario": mortalidad_grupo,
        "Top eventos morbilidad"    : top_eventos_morbilidad,
        "Tendencia mortalidad"      : tendencia,
        "Población histórica"       : poblacion.rename(columns={
            "municipio": "Municipio", "año": "Año",
            "poblacion_total": "Población total",
            "poblacion_urbana": "Urbana", "poblacion_rural": "Rural"
        })
    }

    with pd.ExcelWriter(RUTA_REPORTE, engine="openpyxl") as writer:
        for nombre, df in hojas.items():
            df.to_excel(writer, sheet_name=nombre, index=False)
            hoja = writer.sheets[nombre]
            for col in hoja.columns:
                max_ancho = max(
                    len(str(col[0].value)) if col[0].value else 0,
                    *[len(str(c.value)) if c.value else 0 for c in col[1:]]
                )
                hoja.column_dimensions[col[0].column_letter].width = min(max_ancho + 4, 50)

    print(f"Reporte ASIS generado en: {RUTA_REPORTE}")


if __name__ == "__main__":
    generar_reporte()
