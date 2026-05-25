# =============================================================================
# asis_analisis.py
# Proyecto: ASIS Municipal - Salud Colombia
# Autor: Mauricio Sánchez
# Descripción: Análisis de Situación de Salud municipal con indicadores
#              de mortalidad, morbilidad y determinantes sociales
# =============================================================================

import pandas as pd
import numpy as np
import os
from datetime import datetime

# -----------------------------------------------------------------------------
# CONFIGURACIÓN
# -----------------------------------------------------------------------------

MUNICIPIO       = "Ciudad Bolívar"
DEPARTAMENTO    = "Antioquia"
AÑO_ANALISIS    = 2023

RUTAS = {
    "poblacion"       : "data/raw/poblacion_municipal.csv",
    "mortalidad"      : "data/raw/mortalidad_municipal.csv",
    "morbilidad"      : "data/raw/morbilidad_eventos.csv",
    "determinantes"   : "data/raw/determinantes_sociales.csv",
    "salida_asis"     : "data/processed/asis_consolidado.csv",
    "salida_resumen"  : "data/processed/resumen_ejecutivo.csv"
}


# -----------------------------------------------------------------------------
# CARGA DE DATOS
# -----------------------------------------------------------------------------

def cargar_datos() -> dict:
    """Carga todos los datasets del ASIS."""
    dataframes = {}
    for nombre, ruta in RUTAS.items():
        if "salida" not in nombre:
            if os.path.exists(ruta):
                dataframes[nombre] = pd.read_csv(ruta, encoding="utf-8")
                print(f"  {nombre:<20} {len(dataframes[nombre])} registros cargados")
            else:
                print(f"  ADVERTENCIA: No se encontró {ruta}")
    return dataframes


# -----------------------------------------------------------------------------
# ANÁLISIS DEMOGRÁFICO
# -----------------------------------------------------------------------------

def analisis_demografico(df_pob: pd.DataFrame) -> dict:
    """Calcula indicadores demográficos básicos."""
    ultimo_año = df_pob[df_pob["año"] == AÑO_ANALISIS].iloc[0] if len(df_pob[df_pob["año"] == AÑO_ANALISIS]) > 0 else df_pob.iloc[-1]

    return {
        "poblacion_total"       : int(ultimo_año["poblacion_total"]),
        "indice_masculinidad"   : round(ultimo_año["poblacion_masculina"] / ultimo_año["poblacion_femenina"] * 100, 2),
        "porcentaje_urbano"     : round(ultimo_año["poblacion_urbana"] / ultimo_año["poblacion_total"] * 100, 2),
        "porcentaje_rural"      : round(ultimo_año["poblacion_rural"] / ultimo_año["poblacion_total"] * 100, 2),
        "porcentaje_menor5"     : round(ultimo_año["poblacion_menor5"] / ultimo_año["poblacion_total"] * 100, 2),
        "porcentaje_60_mas"     : round(ultimo_año["poblacion_60_mas"] / ultimo_año["poblacion_total"] * 100, 2),
        "indice_envejecimiento" : round(ultimo_año["poblacion_60_mas"] / ultimo_año["poblacion_menor5"] * 100, 2)
    }


# -----------------------------------------------------------------------------
# ANÁLISIS DE MORTALIDAD
# -----------------------------------------------------------------------------

def analisis_mortalidad(df_mort: pd.DataFrame, poblacion: int) -> dict:
    """Calcula indicadores de mortalidad."""
    df_año = df_mort[df_mort["año"] == AÑO_ANALISIS]

    total_muertes   = df_año["numero_muertes"].sum()
    tasa_mortalidad = round(total_muertes / poblacion * 100000, 2)

    primeras_causas = (
        df_año.groupby("causa_muerte")["numero_muertes"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    muertes_externas = df_año[
        df_año["grupo_causa"] == "Causas externas"
    ]["numero_muertes"].sum()

    muertes_cardiovascular = df_año[
        df_año["grupo_causa"] == "Enfermedades cardiovasculares"
    ]["numero_muertes"].sum()

    return {
        "total_muertes"             : int(total_muertes),
        "tasa_mortalidad_general"   : tasa_mortalidad,
        "muertes_causas_externas"   : int(muertes_externas),
        "muertes_cardiovasculares"  : int(muertes_cardiovascular),
        "primera_causa"             : primeras_causas.iloc[0]["causa_muerte"] if len(primeras_causas) > 0 else "N/D",
        "primeras_causas"           : primeras_causas
    }


# -----------------------------------------------------------------------------
# ANÁLISIS DE MORBILIDAD
# -----------------------------------------------------------------------------

def analisis_morbilidad(df_morb: pd.DataFrame) -> dict:
    """Calcula indicadores de morbilidad y eventos de interés en salud pública."""
    df_año = df_morb[df_morb["año"] == AÑO_ANALISIS]

    total_casos = df_año["casos_confirmados"].sum()

    top_eventos = (
        df_año.groupby("evento")["casos_confirmados"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
        .reset_index()
    )

    casos_dengue        = df_año[df_año["evento"] == "Dengue"]["casos_confirmados"].sum()
    casos_desnutricion  = df_año[df_año["evento"] == "Desnutrición aguda"]["casos_confirmados"].sum()
    casos_tuberculosis  = df_año[df_año["evento"] == "Tuberculosis pulmonar"]["casos_confirmados"].sum()

    return {
        "total_casos_notificados"   : int(total_casos),
        "casos_dengue"              : int(casos_dengue),
        "casos_desnutricion_aguda"  : int(casos_desnutricion),
        "casos_tuberculosis"        : int(casos_tuberculosis),
        "top_eventos"               : top_eventos
    }


# -----------------------------------------------------------------------------
# ANÁLISIS DE DETERMINANTES SOCIALES
# -----------------------------------------------------------------------------

def analisis_determinantes(df_det: pd.DataFrame) -> dict:
    """Extrae los indicadores clave de determinantes sociales."""
    df_año = df_det[df_det["año"] == AÑO_ANALISIS]

    def obtener_valor(indicador):
        fila = df_año[df_año["indicador"].str.contains(indicador, case=False, na=False)]
        return round(float(fila["valor"].values[0]), 2) if len(fila) > 0 else None

    return {
        "ipm"                       : obtener_valor("pobreza multidimensional"),
        "cobertura_acueducto"       : obtener_valor("acueducto"),
        "cobertura_alcantarillado"  : obtener_valor("alcantarillado"),
        "tasa_analfabetismo"        : obtener_valor("analfabetismo"),
        "cobertura_vacunacion_dpt"  : obtener_valor("DPT"),
        "mortalidad_infantil"       : obtener_valor("mortalidad infantil"),
        "mortalidad_materna"        : obtener_valor("mortalidad materna"),
        "desnutricion_cronica"      : obtener_valor("desnutrición crónica"),
        "desnutricion_aguda"        : obtener_valor("desnutrición aguda")
    }


# -----------------------------------------------------------------------------
# GENERACIÓN DEL RESUMEN EJECUTIVO
# -----------------------------------------------------------------------------

def generar_resumen_ejecutivo(demografico: dict, mortalidad: dict,
                               morbilidad: dict, determinantes: dict) -> pd.DataFrame:
    """Consolida todos los indicadores en una tabla resumen."""
    indicadores = []

    # Demográficos
    indicadores += [
        {"dimension": "Demografía", "indicador": "Población total", "valor": demografico["poblacion_total"], "unidad": "habitantes"},
        {"dimension": "Demografía", "indicador": "Porcentaje urbano", "valor": demografico["porcentaje_urbano"], "unidad": "%"},
        {"dimension": "Demografía", "indicador": "Índice de envejecimiento", "valor": demografico["indice_envejecimiento"], "unidad": "adultos mayores x100 menores 5"},
    ]

    # Mortalidad
    indicadores += [
        {"dimension": "Mortalidad", "indicador": "Total muertes", "valor": mortalidad["total_muertes"], "unidad": "defunciones"},
        {"dimension": "Mortalidad", "indicador": "Tasa de mortalidad general", "valor": mortalidad["tasa_mortalidad_general"], "unidad": "x 100.000 hab"},
        {"dimension": "Mortalidad", "indicador": "Muertes por causas externas", "valor": mortalidad["muertes_causas_externas"], "unidad": "defunciones"},
        {"dimension": "Mortalidad", "indicador": "Primera causa de muerte", "valor": mortalidad["primera_causa"], "unidad": "causa"},
    ]

    # Morbilidad
    indicadores += [
        {"dimension": "Morbilidad", "indicador": "Total casos notificados", "valor": morbilidad["total_casos_notificados"], "unidad": "casos"},
        {"dimension": "Morbilidad", "indicador": "Casos de dengue", "valor": morbilidad["casos_dengue"], "unidad": "casos confirmados"},
        {"dimension": "Morbilidad", "indicador": "Casos desnutrición aguda", "valor": morbilidad["casos_desnutricion_aguda"], "unidad": "casos confirmados"},
        {"dimension": "Morbilidad", "indicador": "Casos tuberculosis pulmonar", "valor": morbilidad["casos_tuberculosis"], "unidad": "casos confirmados"},
    ]

    # Determinantes
    indicadores += [
        {"dimension": "Determinantes sociales", "indicador": "Índice de pobreza multidimensional", "valor": determinantes["ipm"], "unidad": "%"},
        {"dimension": "Determinantes sociales", "indicador": "Cobertura acueducto", "valor": determinantes["cobertura_acueducto"], "unidad": "%"},
        {"dimension": "Determinantes sociales", "indicador": "Cobertura alcantarillado", "valor": determinantes["cobertura_alcantarillado"], "unidad": "%"},
        {"dimension": "Determinantes sociales", "indicador": "Cobertura vacunación DPT", "valor": determinantes["cobertura_vacunacion_dpt"], "unidad": "%"},
        {"dimension": "Determinantes sociales", "indicador": "Tasa mortalidad infantil", "valor": determinantes["mortalidad_infantil"], "unidad": "x 1.000 NV"},
        {"dimension": "Determinantes sociales", "indicador": "Prevalencia desnutrición crónica", "valor": determinantes["desnutricion_cronica"], "unidad": "%"},
    ]

    return pd.DataFrame(indicadores)


# -----------------------------------------------------------------------------
# IMPRESIÓN EN CONSOLA
# -----------------------------------------------------------------------------

def imprimir_resumen(demografico, mortalidad, morbilidad, determinantes):
    """Imprime el resumen ejecutivo del ASIS en consola."""
    print("\n" + "=" * 60)
    print(f"   ASIS — {MUNICIPIO}, {DEPARTAMENTO} — {AÑO_ANALISIS}")
    print("=" * 60)

    print("\n  DEMOGRAFÍA")
    print(f"  Población total          : {demografico['poblacion_total']:,} habitantes")
    print(f"  Porcentaje urbano        : {demografico['porcentaje_urbano']}%")
    print(f"  Porcentaje rural         : {demografico['porcentaje_rural']}%")
    print(f"  Índice de envejecimiento : {demografico['indice_envejecimiento']}")

    print("\n  MORTALIDAD")
    print(f"  Total muertes            : {mortalidad['total_muertes']}")
    print(f"  Tasa mortalidad general  : {mortalidad['tasa_mortalidad_general']} x 100.000 hab")
    print(f"  Primera causa de muerte  : {mortalidad['primera_causa']}")
    print(f"  Muertes causas externas  : {mortalidad['muertes_causas_externas']}")

    print("\n  MORBILIDAD")
    print(f"  Casos notificados        : {morbilidad['total_casos_notificados']}")
    print(f"  Casos dengue             : {morbilidad['casos_dengue']}")
    print(f"  Casos desnutrición aguda : {morbilidad['casos_desnutricion_aguda']}")
    print(f"  Casos tuberculosis       : {morbilidad['casos_tuberculosis']}")

    print("\n  DETERMINANTES SOCIALES")
    print(f"  IPM                      : {determinantes['ipm']}%")
    print(f"  Cobertura acueducto      : {determinantes['cobertura_acueducto']}%")
    print(f"  Mortalidad infantil      : {determinantes['mortalidad_infantil']} x 1.000 NV")
    print(f"  Desnutrición crónica     : {determinantes['desnutricion_cronica']}%")
    print("=" * 60 + "\n")


# -----------------------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# -----------------------------------------------------------------------------

def ejecutar_asis():
    print(f"\nIniciando ASIS — {MUNICIPIO} — {AÑO_ANALISIS}")
    print("Cargando datos...\n")

    datos = cargar_datos()

    demografico     = analisis_demografico(datos["poblacion"])
    mortalidad      = analisis_mortalidad(datos["mortalidad"], demografico["poblacion_total"])
    morbilidad      = analisis_morbilidad(datos["morbilidad"])
    determinantes   = analisis_determinantes(datos["determinantes"])

    resumen = generar_resumen_ejecutivo(demografico, mortalidad, morbilidad, determinantes)

    os.makedirs("data/processed", exist_ok=True)
    resumen.to_csv(RUTAS["salida_resumen"], index=False, encoding="utf-8")

    imprimir_resumen(demografico, mortalidad, morbilidad, determinantes)
    print(f"Resumen exportado en: {RUTAS['salida_resumen']}")


if __name__ == "__main__":
    ejecutar_asis()
