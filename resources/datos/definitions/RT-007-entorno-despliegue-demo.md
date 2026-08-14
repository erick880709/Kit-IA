# RT-007: Entorno de Despliegue de la Demo Funcional

**Tipo:** Requisito técnico
**Categoría:** Infraestructura / Despliegue
**Fuente:** 04-ESPECIFICACION-APLICACION-DEMO.md; 01-CONTEXTO-MAESTRO-CONSOLIDADO.md §3; 05-PENDIENTES-PARA-DIRECTORA.md

## Descripción
El proyecto incluye una demo funcional interactiva como entregable. La demo no es un producto productivo, sino un prototipo para validar la viabilidad técnica y clínica de la solución ante el tribunal del TFM y potencialmente ante profesionales del Hospital San Juan de Dios. El entorno de despliegue debe ser ligero, portátil y ejecutable en una máquina local sin dependencia de servicios cloud.

## Especificación del entorno

### Alcance de la demo
- **No es un sistema productivo.** No se despliega en un servidor hospitalario ni maneja datos reales de pacientes en vivo.
- La demo opera con datos sintéticos o anonimizados precargados para demostrar el flujo completo.
- Los modelos se cargan desde archivos serializados (pickle/joblib/h5) pre-entrenados offline (RT-005).
- No se requiere conexión a internet para la inferencia (el modelo NLP también se carga localmente).

### Requisitos de despliegue
| Aspecto | Especificación |
|---|---|
| Ejecución | Máquina local (Windows/Mac/Linux), sin necesidad de GPU |
| Dependencias | Python 3.10+, librerías listadas en `requirements.txt` |
| Arranque | Un solo comando (ej. `streamlit run app.py` o `python app.py`) |
| Datos demo | Dataset sintético precargado (~100-200 pacientes con distribución realista de niveles I-V) |
| Modelo | Cargado desde archivo al iniciar la aplicación |
| Persistencia | SQLite (archivo local, sin servidor de base de datos separado) |

### Lo que NO incluye la demo
- Integración real con Historia Clínica Electrónica.
- Autenticación con directorio institucional (LDAP/Active Directory).
- Alta disponibilidad o balanceo de carga.
- Cifrado de datos en reposo (los datos son sintéticos, no aplica).
- Pipeline de entrenamiento en vivo (el entrenamiento es offline).

## Impacto en la arquitectura
- La demo debe funcionar como una aplicación autocontenida: un directorio con el código, un `requirements.txt`, un script de arranque y los artefactos del modelo.
- El archivo `README.md` debe incluir instrucciones claras para instalar dependencias y ejecutar la demo en 3 pasos o menos.
- Considerar empaquetar la demo como imagen Docker para eliminar problemas de compatibilidad de entorno entre los miembros del equipo y el tribunal.

## Notas del analista
- **Decisión pendiente Streamlit vs. Flask** (`05-PENDIENTES-PARA-DIRECTORA.md` #1). Streamlit simplifica el arranque (un solo comando) pero tiene limitaciones de personalización visual. Flask/FastAPI + frontend requiere más desarrollo pero ofrece más control. La recomendación técnica es Streamlit para un prototipo de TFM.
- Si se elige Streamlit, evaluar `streamlit-shap` para integrar las visualizaciones SHAP de forma nativa.
- Preparar un video/grabación de la demo como respaldo por si no se puede ejecutar en vivo durante la sustentación.
