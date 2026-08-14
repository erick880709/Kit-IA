# Mapeo y Descarga de Datasets Públicos — Sistema de Triaje Multimodal IA (Colombia)

Extiende `03-CATALOGO-DATOS-Y-VARIABLES.md`. Aquí se fija, para cada fuente pública real identificada, su identificador técnico exacto (resource ID de Socrata), el endpoint de descarga, las columnas confirmadas (verificadas por consulta directa a la API, no por descripción del portal) y el mapeo a las entidades del dominio (`ENT-001` a `ENT-012`).

> **Nota de entorno:** este sandbox de ejecución solo tiene salida de red hacia dominios de paquetería (PyPI, npm, GitHub); `datos.gov.co` no está en la lista blanca. Por eso no pude ejecutar aquí la descarga masiva. Lo que sí hice fue verificar en vivo (vía búsqueda/fetch) el resource ID y el esquema real de columnas de cada dataset, para que el script de la sección 3 funcione sin ensayo y error cuando lo corras en tu máquina o en un notebook con salida a internet.

---

## 1. Tabla de mapeo dataset → catálogo → acceso

| # | Dataset | Entidad/campo del catálogo que resuelve | Resource ID (Socrata) | Endpoint SODA (JSON, paginable) | Endpoint CSV completo | Granularidad |
|---|---|---|---|---|---|---|
| 1 | Clasificación en Triage Urgencias (Min. Salud) | ENT-002 Evento de Triaje → `NivelSugeridoIA`/distribución real de niveles I-V | *(ya en tu CSV subido)* | — | — | Individual (evento) |
| 2 | Morbilidad en el Servicio de Urgencias (nacional) | ENT-004 Motivo de Consulta → diagnóstico CIE-10 | *(ya en tu CSV subido)* | — | — | Agregado (trimestre/diagnóstico/depto) |
| 3 | Morbilidad Urgencias 2019 Pitalito (Huila) | ENT-004, contraste regional | *(ya en tu CSV subido)* | — | — | Agregado (diagnóstico/grupo etario) |
| 4 | **BDUA — Régimen Contributivo** | ENT-001 Paciente → campo `Régimen` (hallazgo #2) | `tq4m-hmg2` | `https://www.datos.gov.co/resource/tq4m-hmg2.json` | `https://www.datos.gov.co/api/views/tq4m-hmg2/rows.csv?accessType=DOWNLOAD` | **Agregado** (conteo por combinación sexo/grupo etario/EPS/zona/depto/municipio/sisbén) |
| 5 | **BDUA — Régimen Subsidiado** | ENT-001 Paciente → campo `Régimen` | `d7a5-cnra` | `https://www.datos.gov.co/resource/d7a5-cnra.json` | `https://www.datos.gov.co/api/views/d7a5-cnra/rows.csv?accessType=DOWNLOAD` | Agregado (mismo esquema que #4) |
| 6 | **RIPS — Registro Prestación Servicios Médicos en Urgencia (con observación)** | ENT-002/ENT-004 → contraste nacional de diagnóstico y estancia | `xveb-6jax` | `https://www.datos.gov.co/resource/xveb-6jax.json` | `https://www.datos.gov.co/api/views/xveb-6jax/rows.csv?accessType=DOWNLOAD` | Individual (registro de atención) — sin signos vitales |
| 7 | Supersalud — Datos Abiertos (desempeño EPS/IPS, PQRD) | Contexto operativo (no entra al modelo) | *(portal propio, no Socrata — ver §2)* | — | — | Agregado |
| 8 | Línea 123 — Llamadas de Urgencias y Emergencias (Bogotá) | ENT-001 → aproximación de `ViaLlegada` (solo a nivel agregado/Bogotá) | *(Datos Abiertos Bogotá, CKAN — ver §2)* | — | — | Agregado mensual |

**Columnas confirmadas de BDUA (contributivo y subsidiado, mismo esquema)** — verificado por consulta directa:

```
tps_gnr_nombre        → Sexo (Masculino/Femenino)
tps_grp_etr_id         → Grupo etario (rangos: "< 1", "1 a 5", "5 a 15", "15 a 19", "19 a 45", "45 a 50"... "> 75")
ent_id                 → Código EPS
ent_nombre              → Nombre EPS
tps_rgm_nombre           → Régimen (Contributivo/Subsidiado)
tps_afl_nombre           → Tipo de afiliado (Cotizante/Beneficiario/Adicional)
tps_est_afl_nombre        → Estado de afiliación (Activo/Protección Laboral/...)
tps_cnd_bnf_nombre         → Condición del beneficiario (Estudiante/Discapacidad/No aplica)
zns_nombre                  → Zona (Urbana/Rural/Rural Dispersal/...)
dpr_nombre                   → Departamento
mnc_nombre                    → Municipio
tps_nvl_ssb_id                 → Nivel SISBÉN (si aplica)
tps_grp_pbl_id                  → Grupo poblacional especial (víctimas del conflicto, comunidades indígenas, etc.)
cantidad                         → Conteo de personas en esa combinación exacta
```

⚠️ **Importante para el pipeline:** BDUA es un dataset **agregado** (cada fila es un conteo, no una persona). Sirve para calibrar la **distribución poblacional de `Régimen`** por departamento/municipio/grupo etario (útil para ponderar el entrenamiento o para el análisis exploratorio de sesgo geográfico), pero **no se puede hacer join fila a fila contra un paciente individual de MIMIC o del Hospital San Juan de Dios**. Documentar esto explícitamente si lo usan en el Cap. 4/5: BDUA informa el prior poblacional de `Régimen`, no imputa el valor por paciente.

---

## 2. Fuentes sin resource ID de Socrata (portal propio)

- **Supersalud** publica su catálogo en un portal propio de transparencia, no en `datos.gov.co`. Punto de entrada: `https://www.supersalud.gov.co/es-co/transparencia-y-acceso-a-la-informacion-publica/datos-abiertos/seccion-de-datos-abiertos`. Desde ahí hay que navegar al dataset específico de desempeño EPS/IPS y descargar el Excel/CSV manualmente (no tiene API SODA pública confirmada).
- **Datos Abiertos Bogotá** usa CKAN, no Socrata. El dataset de la Línea 123 está en `https://datosabiertos.bogota.gov.co/dataset/llamadas-de-urgencias-y-emergencias-que-ingresan-a-traves-de-la-linea-123` — cada mes es un recurso CSV independiente (no un único endpoint versionado); hay que listar los recursos vía la API de CKAN (`/api/3/action/package_show?id=llamadas-de-urgencias-y-emergencias-que-ingresan-a-traves-de-la-linea-123`) y descargar el/los CSV de los meses que necesiten.

---

## 3. Script de descarga (correr en tu máquina / notebook con salida a internet)

Guárdalo como `download_datasets_colombia.py`. Usa la API SODA estándar de Socrata (paginación con `$limit`/`$offset`), sin necesidad de token para volúmenes moderados.

```python
"""
Descarga los datasets públicos colombianos mapeados en
07-MAPEO-Y-DESCARGA-DATASETS.md para el proyecto de Triaje Multimodal IA.

Requisitos: pip install requests pandas
Uso: python download_datasets_colombia.py
"""
import requests
import pandas as pd
from pathlib import Path
import time

OUT_DIR = Path("./datasets_colombia")
OUT_DIR.mkdir(exist_ok=True)

# Socrata resource IDs verificados
SOCRATA_DATASETS = {
    "bdua_contributivo": "tq4m-hmg2",
    "bdua_subsidiado": "d7a5-cnra",
    "rips_urgencias_observacion": "xveb-6jax",
}

BASE = "https://www.datos.gov.co/resource/{}.json"
PAGE_SIZE = 50000  # límite razonable por página SODA


def download_socrata(name: str, resource_id: str) -> None:
    """Descarga un dataset completo de datos.gov.co vía paginación SODA."""
    url = BASE.format(resource_id)
    offset = 0
    frames = []
    while True:
        params = {"$limit": PAGE_SIZE, "$offset": offset}
        resp = requests.get(url, params=params, timeout=60)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        frames.append(pd.DataFrame(batch))
        offset += PAGE_SIZE
        print(f"  {name}: {offset} filas descargadas...")
        time.sleep(0.5)  # cortesía con el servidor
        if len(batch) < PAGE_SIZE:
            break
    if frames:
        df = pd.concat(frames, ignore_index=True)
        out_path = OUT_DIR / f"{name}.csv"
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"✔ {name}: {len(df)} filas → {out_path}")
    else:
        print(f"⚠ {name}: sin datos devueltos, revisar resource_id")


def download_ckan_resource(package_slug: str, out_name: str) -> None:
    """Lista y descarga los recursos CSV de un dataset CKAN (Datos Abiertos Bogotá)."""
    api = f"https://datosabiertos.bogota.gov.co/api/3/action/package_show?id={package_slug}"
    resp = requests.get(api, timeout=60)
    resp.raise_for_status()
    resources = resp.json()["result"]["resources"]
    for r in resources:
        if r.get("format", "").upper() == "CSV":
            fname = OUT_DIR / f"{out_name}_{r['name'][:40].replace(' ', '_')}.csv"
            with requests.get(r["url"], stream=True, timeout=120) as rr:
                rr.raise_for_status()
                with open(fname, "wb") as f:
                    for chunk in rr.iter_content(chunk_size=8192):
                        f.write(chunk)
            print(f"✔ CKAN {out_name}: {fname.name}")


if __name__ == "__main__":
    print("=== Descargando datasets Socrata (datos.gov.co) ===")
    for name, rid in SOCRATA_DATASETS.items():
        download_socrata(name, rid)

    print("\n=== Descargando Línea 123 (CKAN, Datos Abiertos Bogotá) ===")
    download_ckan_resource(
        "llamadas-de-urgencias-y-emergencias-que-ingresan-a-traves-de-la-linea-123",
        "linea123_urgencias",
    )

    print("\nListo. Supersalud requiere descarga manual desde su portal propio (ver §2 del mapeo).")
```

**Notas de uso:**
- BDUA (contributivo + subsidiado) son datasets grandes (varios cientos de miles de filas agregadas); la paginación puede tardar varios minutos. Si solo necesitas un departamento/municipio, añade `params["$where"] = "dpr_nombre='QUINDIO'"` (sintaxis SoQL) para filtrar en el servidor y evitar traer todo.
- RIPS de Urgencias (`xveb-6jax`) puede ser el más pesado — revisa primero el conteo total con `params = {"$select": "count(*)"}` antes de descargar completo.
- Todos los archivos quedan en `./datasets_colombia/` en formato CSV UTF-8, listos para el paso 2 (Limpieza) del pipeline ya descrito en `02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §5.

---

## 4. Qué hacer con cada uno en el pipeline

| Dataset descargado | Paso del pipeline (`02-ESPECIFICACION-TECNICA-MODELOS-IA.md` §5) | Uso concreto |
|---|---|---|
| BDUA contributivo + subsidiado | Paso 1 (Ingesta) / análisis exploratorio | Calibrar distribución poblacional de `Régimen` por departamento — **no** join directo a paciente |
| RIPS Urgencias con observación | Paso 1 / Paso 12 (Comparación con benchmarks) | Contraste nacional de diagnósticos CIE-10 y tiempos de estancia frente a lo observado en San Juan de Dios |
| Línea 123 Bogotá | Cap. 2/6 del TFM (contexto, limitaciones) | Aproximación agregada de `ViaLlegada`, solo como referencia narrativa, no como feature de entrenamiento |
| Supersalud (manual) | Cap. 2 del TFM (estado del arte / contexto) | Desempeño operativo EPS/IPS, análisis exploratorio, no entra al modelo |

**Recordatorio de la limitación ya documentada:** ninguno de estos datasets aporta signos vitales por paciente. Siguen siendo MIMIC-IV-ED + fine-tuning con San Juan de Dios la única fuente para esa parte del vector de features.
