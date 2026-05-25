# 📖 Diccionario de Datos — ASIS Municipal

## Tabla: poblacion_municipal

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| municipio | Texto | Nombre del municipio | Ciudad Bolívar |
| codigo_divipola | Texto | Código DIVIPOLA del municipio | 05154 |
| departamento | Texto | Nombre del departamento | Antioquia |
| año | Entero | Año de la proyección poblacional | 2023 |
| poblacion_total | Entero | Población total proyectada | 48234 |
| poblacion_masculina | Entero | Población masculina proyectada | 23890 |
| poblacion_femenina | Entero | Población femenina proyectada | 24344 |
| poblacion_urbana | Entero | Población en zona urbana | 28940 |
| poblacion_rural | Entero | Población en zona rural | 19294 |

---

## Tabla: mortalidad_municipal

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| causa_muerte | Texto | Descripción de la causa de muerte | Enfermedades isquémicas del corazón |
| codigo_cie10 | Texto | Código CIE-10 de la causa | I20-I25 |
| grupo_causa | Texto | Agrupación de la causa | Enfermedades cardiovasculares |
| sexo | Texto | Sexo (M/F) | M |
| grupo_etario | Texto | Grupo de edad | 60 años y más |
| numero_muertes | Entero | Número de defunciones | 12 |
| tasa_mortalidad_x100mil | Decimal | Tasa por 100.000 habitantes | 24.88 |

---

## Tabla: morbilidad_eventos

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| semana_epidemiologica | Entero | Semana epidemiológica (1-52) | 1 |
| evento | Texto | Nombre del evento de notificación | Dengue |
| codigo_sivigila | Texto | Código del evento en SIVIGILA | 210 |
| casos_confirmados | Entero | Casos con diagnóstico confirmado | 3 |
| casos_probables | Entero | Casos con diagnóstico probable | 2 |
| tasa_incidencia_x100mil | Decimal | Tasa de incidencia x 100.000 hab | 6.22 |

---

## Tabla: determinantes_sociales

| Variable | Tipo | Descripción | Ejemplo |
|----------|------|-------------|---------|
| indicador | Texto | Nombre del indicador de determinante | Índice de pobreza multidimensional |
| valor | Decimal | Valor numérico del indicador | 42.3 |
| unidad | Texto | Unidad de medida | porcentaje |
| fuente | Texto | Entidad que reporta el indicador | DANE |

---

## Fuentes de información

| Fuente | Descripción |
|--------|-------------|
| DANE | Departamento Administrativo Nacional de Estadística — proyecciones de población |
| MSPS | Ministerio de Salud y Protección Social — estadísticas vitales y coberturas |
| SIVIGILA | Sistema Nacional de Vigilancia en Salud Pública — eventos de notificación obligatoria |
| ICBF | Instituto Colombiano de Bienestar Familiar — indicadores nutricionales |
| DANE-CNPV | Censo Nacional de Población y Vivienda — NBI e IPM |

---

## Marco normativo del ASIS

| Norma | Descripción |
|-------|-------------|
| Resolución 1536 de 2015 | Disposiciones sobre el proceso de planeación para la salud |
| Resolución 518 de 2015 | Directrices para la elaboración, ejecución y seguimiento del Plan de Salud Territorial |
| Plan Decenal de Salud Pública 2022-2031 | Marco estratégico nacional para la salud pública en Colombia |
| Ley 1751 de 2015 | Ley Estatutaria de Salud — derecho fundamental a la salud |

---

## Notas

- Todos los datos son registros de prueba creados por el autor para representar escenarios reales.
- No contienen información real de pacientes ni de instituciones de salud.
- Este proyecto cumple con la Ley 1581 de 2012 — Habeas Data de Colombia.
