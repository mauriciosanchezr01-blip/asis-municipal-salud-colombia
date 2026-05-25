# 🗺️ ASIS Municipal — Análisis de Situación de Salud

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791?style=flat-square&logo=postgresql)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat-square&logo=powerbi)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-green?style=flat-square)
![Licencia](https://img.shields.io/badge/Licencia-MIT-lightgrey?style=flat-square)

> Herramienta de análisis territorial de salud pública para municipios colombianos.
> Consolida indicadores de mortalidad, morbilidad, demografía y determinantes sociales
> para apoyar la toma de decisiones en secretarías de salud, hospitales públicos y gobernaciones.

---

## 📌 Problema que resuelve

Los equipos de salud pública municipal en Colombia deben elaborar anualmente el ASIS (Análisis de Situación de Salud), un documento técnico que requiere cruzar múltiples fuentes de información: DANE, SIVIGILA, MSPS, ICBF y registros propios. Este proceso se realiza manualmente, consume semanas de trabajo y los resultados quedan en documentos estáticos difíciles de actualizar.

Este proyecto automatiza la consolidación, análisis y visualización de todos esos indicadores.

---

## 🎯 Objetivo del proyecto

Construir un pipeline de análisis que permita a equipos de salud pública:

- Consolidar indicadores demográficos, de mortalidad, morbilidad y determinantes sociales
- Calcular tasas e índices ajustados según estándares del MSPS
- Detectar alertas tempranas en indicadores críticos
- Generar reportes automáticos en Excel listos para el documento ASIS
- Visualizar los resultados en un dashboard interactivo en Power BI

---

## 📁 Estructura del proyecto

```
asis-municipal-salud-colombia/
│
├── data/
│   ├── raw/                          # Datos fuente por componente
│   │   ├── poblacion_municipal.csv
│   │   ├── mortalidad_municipal.csv
│   │   ├── morbilidad_eventos.csv
│   │   └── determinantes_sociales.csv
│   └── processed/                    # Resultados del análisis
│
├── src/
│   ├── asis_analisis.py              # Pipeline principal de análisis
│   └── reporte_asis.py               # Generación de reporte en Excel
│
├── sql/
│   └── consultas_asis.sql            # Queries para PostgreSQL y Power BI
│
├── docs/
│   └── diccionario_datos.md          # Descripción de variables y fuentes
│
├── dashboard/
│   └── README.md                     # Instrucciones del dashboard Power BI
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Tecnologías utilizadas

| Herramienta | Uso |
|-------------|-----|
| Python 3.10+ | Análisis, cálculo de indicadores y automatización |
| Pandas / NumPy | Transformación y procesamiento de datos |
| PostgreSQL | Almacenamiento y consultas territoriales |
| Power BI + DAX | Dashboard ejecutivo interactivo |
| Excel (openpyxl) | Reporte automático exportable |
| Git / GitHub | Control de versiones |

---

## 📊 Indicadores que calcula el pipeline

| Componente | Indicadores |
|------------|-------------|
| Demografía | Población por grupo etario, índice de envejecimiento, razón urbano/rural |
| Mortalidad | Tasa de mortalidad general, primeras causas, mortalidad infantil, materna |
| Morbilidad | Incidencia por evento SIVIGILA, canal endémico dengue, desnutrición aguda |
| Determinantes | IPM, cobertura servicios públicos, vacunación, analfabetismo |

---

## 🗂️ Contexto normativo

- Resolución 1536 de 2015 — proceso de planeación en salud
- Resolución 518 de 2015 — Plan de Salud Territorial
- Plan Decenal de Salud Pública 2022-2031
- Protocolo de vigilancia epidemiológica — SIVIGILA
- Clasificación Internacional de Enfermedades CIE-10

---

## 🚀 Cómo ejecutar el proyecto

```bash
# 1. Clonar el repositorio
git clone https://github.com/mauriciosanchezr01-blip/asis-municipal-salud-colombia.git

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el análisis ASIS
python src/asis_analisis.py

# 4. Generar el reporte en Excel
python src/reporte_asis.py
```

---

## 📈 Resultados esperados

- Resumen ejecutivo con indicadores clave del municipio
- Reporte Excel con 8 hojas temáticas listo para el documento ASIS
- Base de datos estructurada para análisis en Power BI
- Alertas automáticas en indicadores críticos (mortalidad infantil, vacunación, desnutrición)

---

## ⚠️ Aviso de privacidad

Todos los datos utilizados en este proyecto son registros de prueba creados por el autor para representar escenarios reales del sector salud colombiano, sin comprometer información de pacientes ni instituciones reales. Este proyecto cumple con los principios de la Ley 1581 de 2012 — Habeas Data de Colombia.

---

## 👤 Autor

**Mauricio Sánchez**
Analista de Datos en Salud | Especialista en Ciencia de Datos
Estudiante de Maestría en TIC en Salud — Universidad CES
📍 Medellín, Antioquia, Colombia
🔗 [GitHub](https://github.com/mauriciosanchezr01-blip)

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
