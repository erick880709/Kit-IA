# Pendientes reales — requieren decisión humana (Damaris Fuentes Lorenzo)

Todo lo demás en este set de documentos ya quedó resuelto por consolidación de fuentes existentes. Esto es lo que de verdad no está decidido en ningún documento y no me corresponde decidir por inferencia:

1. **Stack de la demo: Streamlit vs. Flask.** Ambos se mencionan, ninguno se decide. Recomendación no vinculante en `04-ESPECIFICACION-APLICACION-DEMO.md` §1 (Streamlit), pero es tu llamada y la del equipo.

2. **Reflejar la aprobación ética en el PDF del TFM.** `CONTEXTO_TRIAJE.txt` v2.0 (16 jul 2026) dice que el Comité de Ética del Hospital San Juan de Dios ya aprobó, pero el PDF entregado (Cap. 3) todavía dice "requiere autorización, Art. 2.7". Hace falta actualizar esa sección con la evidencia formal antes del depósito — y confirmar si Damaris ya tiene ese documento de aprobación o si falta solicitarlo formalmente por escrito.

3. **Actualizar RF-IA-003 en `CONTEXT_TRIA.txt`** para que refleje explícitamente la selección por umbral optimizado en Niveles I-II (no argmax puro) — ver hallazgo #5 de `00-VALIDACION-HALLAZGOS.md`. Es una corrección de texto, pero conviene que el equipo la revise antes de que quede como entregable formal.

4. **Método de combinación en late fusion** (promedio ponderado / stacking / meta-clasificador) — `CONTEXTO_TRIAJE.txt` lo deja abierto ("a determinar empíricamente en Fase 3"). No es ambigüedad de contexto, es resultado experimental pendiente — no requiere decisión previa, solo queda registrado aquí para que no se pierda de vista en el Cap. 5.

5. **Pendientes normativos del TFM ya identificados en `contexto-tfm.md` §9** (orden alfabético de autores en portada, sección "Organización del trabajo en grupo", herramienta anti-plagio) — no son de arquitectura/IA pero siguen abiertos y son bloqueantes para el depósito.
