# Fuentes de Datos para Entrenamiento — Sistema de Triaje Multimodal IA (Colombia)

> Corresponde a la sección 5 de `01-CONTEXTO-MAESTRO-CONSOLIDADO.md` y a la sección 11 de
> `CONTEXTO_TRIAJE.txt`. URLs verificadas por búsqueda web el 13 de agosto de 2026. Antes de
> descargar, revisar siempre la página oficial por si la versión/URL cambió.

## 1. MIMIC-IV-ED (PhysioNet) — entrenamiento base / preentrenamiento

| Campo | Valor |
|---|---|
| Dataset | MIMIC-IV-ED v2.2 — 422.500 admisiones de urgencias, EE. UU. |
| URL de la página del dataset | https://physionet.org/content/mimic-iv-ed/2.2/ |
| Tablas incluidas | `edstays`, `diagnosis`, `medrecon`, `pyxis`, `triage`, `vitalsign` |
| Acceso | **Credencializado** — no es descarga directa |
| Requisitos previos | 1) Crear cuenta en https://physionet.org/ · 2) Completar el curso **CITI "Data or Specimens Only Research"** · 3) Firmar el **PhysioNet Credentialed Health Data Use Agreement 1.5.0** |
| Licencia | PhysioNet Credentialed Health Data License 1.5.0 |
| DOI (referencia para citar) | https://doi.org/10.13026/1cjn-2370 |
| Relacionados útiles | `MIMIC-IV` (core, demográficas/admisión): https://physionet.org/content/mimiciv/3.1/ · `MIMIC-IV-Note` (notas clínicas en texto libre, para el módulo NLP/BERT): https://physionet.org/content/mimic-iv-note/2.2/ |
| Demo sin credencial (para prototipar el pipeline antes de tener acceso completo) | https://physionet.org/content/mimic-iv-demo/2.2/ — subconjunto público, útil solo para probar el código, no para resultados finales del TFM |
| Código de referencia para cargar en PostgreSQL/BigQuery | https://github.com/MIT-LCP/mimic-code |

⚠️ El trámite de credencialización + curso CITI puede tardar días — iniciarlo cuanto antes si aún no está hecho, es la dependencia más larga de todo el pipeline de datos.

## 2. Registro clínico Hospital San Juan de Dios — adaptación al contexto colombiano

| Campo | Valor |
|---|---|
| Rol | Fine-tuning obligatorio (mitiga el sesgo geográfico de MIMIC, que es de EE. UU.) |
| Acceso | No es un dataset público — se obtiene directamente de la institución, bajo la autorización del Comité de Ética de la Investigación (Art. 2.7 del Reglamento UNIR) |
| Estado según el contexto del proyecto | `CONTEXTO_TRIAJE.txt` v2.0 (16 jul 2026) reporta **aprobación** del comité de ética — verificar que el PDF del TFM y la evidencia documental formal (carta/acta del comité) estén realmente en mano antes de usarlo, ver `05-PENDIENTES-PARA-DIRECTORA.md` |
| No hay URL de descarga | Coordinar directamente con la institución/directora del TFM |

## 3. "Clasificación en Triage Urgencias" — Min. Salud, Datos Abiertos Colombia

| Campo | Valor |
|---|---|
| Rol | Distribución real de niveles de triaje I-V en Colombia (contraste/calibración) |
| Página del dataset | https://www.datos.gov.co/en/Salud-y-Protecci-n-Social/Clasificaci-n-en-Triage-Urgencias/vt5n-eu2r |
| Descarga directa (CSV vía API Socrata) | `https://www.datos.gov.co/resource/vt5n-eu2r.csv` |
| Descarga directa (JSON vía API Socrata) | `https://www.datos.gov.co/resource/vt5n-eu2r.json` |
| Formato | Socrata Open Data (SODA) — permite además exportar Excel desde la interfaz web |
| Acceso | Público, sin autenticación |

## 4. BDUA (ADRES) — variables demográficas y régimen de afiliación

| Campo | Valor |
|---|---|
| Rol | Variables demográficas y régimen de afiliación (contributivo/subsidiado) para enriquecer `ENT-001 Paciente` |
| Portal institucional (ADRES) | https://www.adres.gov.co/eps/procesos/bdua |
| Catálogo en Datos Abiertos Colombia (buscar "BDUA" — está fragmentado por régimen/entidad territorial, no es un único CSV nacional) | https://www.datos.gov.co/browse?q=BDUA |
| Ejemplos de conjuntos específicos ya publicados | Régimen contributivo: `https://www.datos.gov.co/Salud-y-Protecci-n-Social/Poblaci-n-Base-de-Datos-nica-de-Afiliados-BDUA-del/tq4m-hmg2` · Régimen subsidiado: `https://www.datos.gov.co/Salud-y-Protecci-n-Social/Poblaci-n-Base-de-Datos-nica-de-Afiliados-BDUA-del/d7a5-cnra` |
| Acceso | Público, sin autenticación, vía API Socrata (agregar `.csv` o `.json` al ID del recurso, igual que en la sección 3) |
| Nota | Los conjuntos de datos.gov.co suelen estar particionados por entidad territorial/EPS — para una muestra nacional agregada, revisar el buscador del portal por fecha de publicación más reciente antes de descargar, ya que se actualizan periódicamente |

## 5. Datos Abiertos Supersalud — desempeño operativo EPS/IPS

| Campo | Valor |
|---|---|
| Rol | Contexto operativo (no es dato clínico de paciente — solo análisis exploratorio/contexto en el TFM, según `03-CATALOGO-DATOS-Y-VARIABLES.md`) |
| Portal de Datos Abiertos de la Supersalud | https://www.supersalud.gov.co/es-co/transparencia-y-acceso-a-la-informacion-publica/datos-abiertos/seccion-de-datos-abiertos |
| Información financiera EPS (serie histórica) | https://www.supersalud.gov.co/es-co/paginas/delegada%20supervision%20de%20riesgos/informacion-financiera-eps-emp-sap-regimenes-de-excepcion-y-especiales.aspx |
| Estadísticas financieras IPS | https://www.supersalud.gov.co/es-co/Paginas/Delegada%20Supervisi%C3%B3n%20Institucional/Estad%C3%ADsticas-Financieras-IPS.aspx |
| Acceso | Público, sin autenticación — formatos varían (XLSX/CSV según el recurso, no todo vía API Socrata) |

## 6. Marco normativo de referencia (no es dataset, pero se cita en Cap. 2/3 del TFM)

| Documento | URL |
|---|---|
| Resolución 5596 de 2015 (Min. Salud) — define los 5 niveles de triaje | https://www.minsalud.gov.co/sites/rid/Lists/BibliotecaDigital/RIDE/DE/DIJ/resolucion-5596-de-2015.pdf |
| Página informativa oficial sobre Triage | https://www2.minsalud.gov.co/salud/emergencias-y-desastres/Paginas/triage.aspx |

## 8. Estado de descarga local — 2026-08-14 (validado contra `datasets/`)

Todo lo descargado queda en `datasets/` (local, **no** versionado en GitHub por contener datos reales). Validación del 14 de agosto: inventario de `datasets/` + integración al pipeline (`triaje-ia/ml/pipeline.py`).

| Fuente | Archivo local | Estado | Rol real en el modelo |
|---|---|---|---|
| Clasificación en Triage Urgencias (MinSalud, `vt5n-eu2r`) | `datasets/clasificacion_triage_urgencias_20260813.csv` (89.453 filas, 13,1 MB) | ✅ Descargado | **Calibración**: distribución real medida I 0.227% · II 3.030% · III 88.536% · IV 7.752% · V 0.456% — valida el sintético |
| **Registro Hospital San Juan de Dios (cohorte real)** | `datasets/dataset_urgencias_san_juan_de_dios_custom.csv` (43.594 filas, 6,8 MB) | ✅ Descargado | **Entrenamiento real**: triaje I–V + CIE-10 + diagnóstico → entrena el submodelo de texto de la fusión tardía (fine-tuning colombiano) |
| BDUA Régimen Contributivo (`tq4m-hmg2`) | `datasets/bdua_contributivo.csv` (97,3 MB) | ✅ Descargado | Calibración poblacional de Régimen (agregado — no join a paciente) |
| BDUA Régimen Subsidiado (`d7a5-cnra`) | `datasets/bdua_subsidiado.csv` (214,4 MB) | ✅ Descargado | Ídem |
| Morbilidad Urgencias (nacional + Pitalito) | `MORBILIDAD_*.csv`, `Morbilidad_Urgencias_2019_*.csv` | ✅ Descargado | Contraste de diagnósticos CIE-10 (agregado, sin etiqueta) |
| RIPS Urgencias con observación (`xveb-6jax`) | — | ❌ 403 Forbidden (SODA y CSV) | Pendiente: buscar resource ID republicado |
| Línea 123 Bogotá (CKAN) | `datasets/linea123_llamadas_salud_2026-06.csv` (1 mes) | ⏳ Parcial (1/100 meses) | Contexto narrativo (agregado) |
| MIMIC-IV-ED v2.2 (completo) | — | 🔒 Requiere credencial CITI + DUA firmado | **Pendiente**: fuente definitiva de signos vitales (TT-E3-01) |
| MIMIC-IV-Demo 2.2 | — | ⏳ Open access (sin tablas ED — no sirve) | No aplica |
| Supersalud | — | ⏳ Portal propio, descarga manual | Contexto operativo |

**Conclusión de la validación:** los datasets que realmente alimentan el modelo y su precisión están descargados e integrados — SJdD (43.594 eventos reales con etiqueta) entrena el submodelo de texto y el nacional MinSalud calibra la distribución de niveles. La única fuente clínica faltante de alto valor es **MIMIC-IV-ED** (credenciales PhysioNet: dependencia del usuario).

## 7. Checklist antes de empezar la ingesta (`src/data/ingesta.py`)

- [ ] Cuenta PhysioNet creada y curso CITI completado (dependencia más larga — iniciar ya).
- [ ] DUA de PhysioNet firmado para MIMIC-IV-ED y MIMIC-IV-Note.
- [ ] Confirmación documental formal (no solo verbal/de contexto) de la aprobación del Comité de
      Ética del Hospital San Juan de Dios, con fecha y referencia citable en el TFM.
- [ ] Verificar en el portal de datos.gov.co si el ID de recurso (`vt5n-eu2r`, etc.) sigue vigente
      antes de automatizar la descarga — los portales Socrata a veces republican con nuevo ID.
- [ ] Todas las fuentes anteriores pasan por el proceso de anonimización (Ley 1581 de 2012) antes
      de cualquier paso de `src/data/limpieza.py` — ya cubierto en `RNS-009/RNS-010/RNGD-*` del
      documento funcional y en `src/data/anonimizacion.py` según la guía de implementación del kit.
