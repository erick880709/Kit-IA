"""Manual de uso por rol (soporte transversal, visible para todos los roles).

Cada rol ve ÚNICAMENTE su propio manual: el contenido vive en un diccionario
puro (`MANUAL_POR_ROL`) y la vista renderiza exclusivamente la entrada del rol
activo. Los diagramas de flujo están en `assets/manual/` y se generan con
`scripts/generar_diagramas_manual.py`.
"""

from __future__ import annotations

from pathlib import Path

import streamlit as st

from app.domain.exceptions import ProhibidoError
from app.services import authorization_service

ASSETS_DIR = Path(__file__).resolve().parents[2] / "assets" / "manual"

# Cada pantalla del manual: {nombre, objetivo, pasos, consejos, errores}
MANUAL_POR_ROL: dict[str, dict] = {
    "Medico": {
        "titulo": "Manual del Médico",
        "descripcion": (
            "El Médico es el responsable clínico del triaje: registra al paciente, "
            "captura signos vitales y evaluación clínica, ejecuta la clasificación IA, "
            "valida profesionalmente el nivel y cierra el evento con el PDF de evidencia."
        ),
        "imagen": "medico_flujo.png",
        "animacion": "medico_flujo.gif",
        "pantallas": [
            {
                "nombre": "Registro de paciente",
                "objetivo": (
                    "Registrar un paciente nuevo o iniciar un nuevo triaje "
                    "de uno existente."
                ),
                "pasos": [
                    "Ingrese a «🏥 Registrar paciente (iniciar triaje)» desde el inicio.",
                    "Escriba el tipo y número de documento y pulse «Verificar documento».",
                    "Si el paciente ya existe: sus datos se precargan y aparece "
                    "«➕ Iniciar nuevo triaje» — úselo (cada visita a urgencias es "
                    "un evento nuevo, NO se duplica al paciente).",
                    "Si no existe: complete las 4 secciones del formulario y pulse "
                    "«Registrar como paciente nuevo».",
                    "Tras el alta o la precarga, pulse «➕ Iniciar triaje (signos vitales)».",
                ],
                "consejos": [
                    "Verifique SIEMPRE por documento antes de crear un paciente.",
                    "El número de triajes previos se muestra antes de iniciar el nuevo evento.",
                ],
                "errores": [
                    "Crear un paciente duplicado en vez de iniciar un nuevo triaje.",
                    "No revisar los datos precargados antes de continuar.",
                ],
            },
            {
                "nombre": "Captura de signos vitales",
                "objetivo": "Registrar los 8 signos vitales con alertas fisiológicas.",
                "pasos": [
                    "Diligencie temperatura, presión arterial, FC, FR, saturación, "
                    "peso y talla.",
                    "El IMC se calcula automáticamente (talla en metros; si digita "
                    "170 cm el sistema la convierte a 1.70 m).",
                    "Si un valor está fuera de rango fisiológico, el sistema exige la "
                    "casilla de confirmación explícita.",
                    "Pulse «Continuar → Evaluación clínica».",
                ],
                "consejos": ["Verifique la unidad de la talla (m) antes de continuar."],
                "errores": ["Digitar la talla en cm sin revisar la conversión automática."],
            },
            {
                "nombre": "Evaluación clínica",
                "objetivo": "Capturar el motivo de consulta CIE-11 y el estado clínico.",
                "pasos": [
                    "Seleccione el motivo estructurado (código CIE-11 + categoría).",
                    "Registre escala de dolor (0-10), Glasgow (3-15) y nivel de conciencia.",
                    "Complete antecedentes por autorreporte, alergias y observaciones si aplica.",
                    "Pulse «Continuar → Clasificación IA».",
                ],
                "consejos": [
                    "El texto libre alimenta el submodelo de NLP: descríbalo con detalle.",
                ],
                "errores": [
                    "Dejar el motivo estructurado con el valor por defecto sin revisarlo.",
                ],
            },
            {
                "nombre": "Clasificación IA",
                "objetivo": "Ejecutar el modelo y revisar el nivel sugerido con probabilidades.",
                "pasos": [
                    "Pulse «⚡ Ejecutar inferencia IA» (presupuesto < 3 s).",
                    "Revise el nivel sugerido, la confianza y las probabilidades por nivel.",
                    "Si el modelo no está disponible, el sistema pasa a triaje "
                    "manual y la indisponibilidad queda auditada — continúe con su "
                    "criterio clínico.",
                    "Pulse «Registrar y continuar → Explicación SHAP».",
                ],
                "consejos": ["La sugerencia es por umbrales calibrados, no por argmax puro."],
                "errores": [
                    "Interpretar la sugerencia como decisión definitiva sin "
                    "validación profesional.",
                ],
            },
            {
                "nombre": "Explicación SHAP",
                "objetivo": "Entender por qué el modelo sugirió ese nivel.",
                "pasos": [
                    "Revise el top-5 de factores con lenguaje clínico y dirección del efecto.",
                    "Preste atención a la alerta de signos prioritarios MTS.",
                    "Pulse «Continuar → Validación profesional».",
                ],
                "consejos": ["Use la explicación para documentar su decisión final."],
                "errores": [],
            },
            {
                "nombre": "Validación profesional",
                "objetivo": "Confirmar o ajustar el nivel asignado (decisión del profesional).",
                "pasos": [
                    "Compare su criterio con el nivel sugerido por la IA.",
                    "Si difiere, registre el motivo de discrepancia (obligatorio).",
                    "La concordancia IA vs profesional queda calculada automáticamente.",
                ],
                "consejos": [
                    "La discrepancia motivada es una decisión clínica válida y queda trazada.",
                ],
                "errores": ["Cambiar el nivel sin registrar el motivo de discrepancia."],
            },
            {
                "nombre": "Cierre del evento",
                "objetivo": "Cerrar el triaje con evidencia descargable.",
                "pasos": [
                    "Verifique el resumen dual (IA vs profesional) y la concordancia.",
                    "Pulse cerrar evento y descargue el PDF de evidencia.",
                    "El historial del paciente queda actualizado con el nuevo evento.",
                ],
                "consejos": ["El PDF sirve como respaldo de sustentación."],
                "errores": ["Cerrar sin revisar la clasificación registrada."],
            },
        ],
        "advertencias": [
            "Sistema de APOYO a la decisión: el profesional valida y decide el nivel.",
            "Tras 5 minutos de inactividad la sesión se cierra automáticamente.",
            "No es un dispositivo médico (demo académica con datos sintéticos).",
        ],
    },
    "Enfermera": {
        "titulo": "Manual de la Enfermera",
        "descripcion": (
            "La Enfermera apoya el ingreso y la captura clínica: registra pacientes, "
            "captura signos vitales y evaluación clínica, ejecuta la clasificación IA y "
            "colabora con el médico en la validación y el cierre del triaje."
        ),
        "imagen": "enfermera_flujo.png",
        "animacion": "enfermera_flujo.gif",
        "pantallas": [
            {
                "nombre": "Registro de paciente",
                "objetivo": "Registrar o localizar al paciente al ingreso a urgencias.",
                "pasos": [
                    "Ingrese a «🏥 Registrar paciente (iniciar triaje)».",
                    "Pulse «Verificar documento» con tipo y número de identificación.",
                    "Si existe: use «➕ Iniciar nuevo triaje» con los datos precargados.",
                    "Si no existe: complete las 4 secciones y regístrelo.",
                ],
                "consejos": ["Pida el documento físico para evitar errores de digitación."],
                "errores": ["Duplicar al paciente en visitas repetidas."],
            },
            {
                "nombre": "Búsqueda de paciente",
                "objetivo": "Localizar pacientes por documento, nombre o apellidos.",
                "pasos": [
                    "Use «🔎 Buscar paciente» desde el inicio.",
                    "Digite documento exacto o nombre/apellidos parciales.",
                    "La búsqueda es paginada; seleccione el paciente correcto.",
                ],
                "consejos": ["El documento exacto es la búsqueda más precisa."],
                "errores": [],
            },
            {
                "nombre": "Captura de signos vitales",
                "objetivo": "Registrar los signos del paciente con controles de rango.",
                "pasos": [
                    "Diligencie los 8 campos (temperatura, TA, FC, FR, SatO2, peso, talla).",
                    "Confirme los valores fuera de rango fisiológico con la casilla habilitada.",
                    "Revise el IMC calculado y continúe.",
                ],
                "consejos": ["Tome los signos antes de digitarlos para evitar dobles lecturas."],
                "errores": ["Confundir la unidad de talla (m vs cm)."],
            },
            {
                "nombre": "Evaluación clínica",
                "objetivo": "Capturar motivo CIE-11 y evaluación de enfermería.",
                "pasos": [
                    "Seleccione el motivo estructurado por categoría.",
                    "Registre dolor, Glasgow y nivel de conciencia.",
                    "Complete antecedentes (autorreporte) y alergias.",
                ],
                "consejos": ["El texto libre mejora la predicción del modelo NLP."],
                "errores": [],
            },
            {
                "nombre": "Clasificación IA y explicación",
                "objetivo": "Ejecutar la inferencia y revisar la explicación.",
                "pasos": [
                    "Pulse «⚡ Ejecutar inferencia IA» y revise nivel y probabilidades.",
                    "Si el modelo no responde, continúe con triaje manual (queda auditado).",
                    "Revise el top-5 SHAP y avance a validación.",
                ],
                "consejos": ["Avise al médico si la sugerencia es I o II (prioridad de atención)."],
                "errores": [],
            },
            {
                "nombre": "Validación y cierre",
                "objetivo": "Acompañar al médico en la validación profesional y el cierre.",
                "pasos": [
                    "El médico confirma o ajusta el nivel (motivo de discrepancia si difiere).",
                    "Cierre el evento y descargue el PDF de evidencia.",
                ],
                "consejos": ["Verifique que la concordancia quede registrada antes de cerrar."],
                "errores": [],
            },
        ],
        "advertencias": [
            "La decisión final del nivel es del profesional médico.",
            "La sesión se cierra tras 5 minutos de inactividad.",
        ],
    },
    "Administrador": {
        "titulo": "Manual del Administrador",
        "descripcion": (
            "El Administrador gestiona usuarios, roles, modelos de IA y supervisa toda "
            "la operación: además del flujo clínico completo, administra permisos, "
            "activa modelos (con rollback de un clic) y consulta auditoría y dashboards."
        ),
        "imagen": "administrador_flujo.png",
        "animacion": "administrador_flujo.gif",
        "pantallas": [
            {
                "nombre": "Flujo clínico completo",
                "objetivo": "El administrador puede operar todas las pantallas clínicas.",
                "pasos": [
                    "Registro de paciente → signos vitales → evaluación clínica.",
                    "Clasificación IA → explicación SHAP → validación → cierre.",
                    "Mismo flujo descrito en el manual del Médico.",
                ],
                "consejos": ["Use el flujo clínico para reproducir incidencias reportadas."],
                "errores": [],
            },
            {
                "nombre": "Gestión de roles y permisos",
                "objetivo": "Administrar usuarios y roles del sistema.",
                "pasos": [
                    "Abra «👥 Gestión de roles y permisos».",
                    "Cree usuarios asignando correo institucional, nombre y rol.",
                    "Cambie roles cuando sea necesario (todo cambio queda auditado).",
                ],
                "consejos": ["Nunca comparta contraseñas; cada usuario tiene su cuenta."],
                "errores": ["Asignar roles con más permisos de los necesarios."],
            },
            {
                "nombre": "Gestión de modelos IA",
                "objetivo": "Activar la versión de modelo que usa la inferencia.",
                "pasos": [
                    "Abra «🧠 Gestión de modelos».",
                    "Revise el historial de versiones con métricas.",
                    "Active la versión ganadora; las demás quedan inactivas automáticamente.",
                    "Si una versión activa falla, reactive la anterior (rollback de un clic).",
                ],
                "consejos": [
                    "Verifique que el artefacto .joblib exista en artifacts/models "
                    "antes de activar.",
                    "Tras activar, la caché de inferencia se invalida automáticamente.",
                ],
                "errores": [
                    "Dejar activa una versión antigua sin submodelo de texto "
                    "(bug 2026-08-14).",
                ],
            },
            {
                "nombre": "Auditoría y trazabilidad",
                "objetivo": "Consultar la bitácora append-only del sistema.",
                "pasos": [
                    "Abra «🕵️ Auditoría y trazabilidad».",
                    "Filtre por usuario, acción, entidad o rango de fechas.",
                    "Exporte a CSV, Excel o PDF para reportes.",
                ],
                "consejos": ["Revise la trazabilidad tras incidentes de seguridad."],
                "errores": [],
            },
            {
                "nombre": "Dashboard operativo",
                "objetivo": "Supervisar indicadores del triaje en tiempo real.",
                "pasos": [
                    "Abra «📈 Dashboard operativo».",
                    "Revise volúmenes por nivel, tiempos y concordancia IA/profesional.",
                ],
                "consejos": ["Use el dashboard antes de reuniones operativas."],
                "errores": [],
            },
        ],
        "advertencias": [
            "Los cambios de rol y de modelo quedan registrados en auditoría.",
            "Respete el principio de mínimo privilegio al asignar permisos.",
        ],
    },
    "Investigador": {
        "titulo": "Manual del Investigador",
        "descripcion": (
            "El Investigador trabaja con la evidencia del modelo: compara experimentos, "
            "revisa explicaciones SHAP, consulta historiales y dashboards, y participa "
            "en la gestión de versiones de modelo. NO opera el flujo clínico."
        ),
        "imagen": "investigador_flujo.png",
        "animacion": "investigador_flujo.gif",
        "pantallas": [
            {
                "nombre": "Comparación de modelos",
                "objetivo": "Comparar los experimentos del pipeline lado a lado.",
                "pasos": [
                    "Abra «📊 Comparación de modelos de IA».",
                    "Revise métricas (AUC, macro-F1, Brier, ECE) por experimento.",
                    "Use el análisis para proponer la próxima versión a activar.",
                ],
                "consejos": ["El AUC del demo-test es optimista; consulte el holdout SJdD."],
                "errores": ["Concluir superioridad sin validación estadística (McNemar/DeLong)."],
            },
            {
                "nombre": "Explicación SHAP",
                "objetivo": "Analizar las variables que más pesan en la clasificación.",
                "pasos": [
                    "Desde un evento clasificado, abra la explicación SHAP.",
                    "Interprete el top-5 con lenguaje clínico y dirección del efecto.",
                ],
                "consejos": ["Correlacione SHAP con la literatura clínica."],
                "errores": [],
            },
            {
                "nombre": "Historial de triajes",
                "objetivo": "Consultar la historia de eventos de un paciente.",
                "pasos": [
                    "Busque al paciente y abra su historial.",
                    "Revise la secuencia cronológica de triajes (más reciente primero).",
                ],
                "consejos": ["El historial valida la relación 1:N paciente→eventos."],
                "errores": [],
            },
            {
                "nombre": "Gestión de modelos",
                "objetivo": "Participar en el registro y activación de versiones.",
                "pasos": [
                    "Abra «🧠 Gestión de modelos».",
                    "Registre nuevas versiones con sus métricas desde el manifiesto.",
                    "Coordine con el administrador la activación y el rollback.",
                ],
                "consejos": ["Toda activación queda auditada con usuario y fecha."],
                "errores": [],
            },
            {
                "nombre": "Dashboard operativo",
                "objetivo": "Monitorear el desempeño operacional del sistema.",
                "pasos": [
                    "Abra «📈 Dashboard operativo» y revise indicadores por nivel.",
                ],
                "consejos": ["Cruzar volumen y concordancia apoya la investigación de uso."],
                "errores": [],
            },
        ],
        "advertencias": [
            "No opere el flujo clínico con el rol de investigador.",
            "Respete la anonimización de los datos (Ley 1581/2012).",
        ],
    },
    "Auditor": {
        "titulo": "Manual del Auditor",
        "descripcion": (
            "El Auditor vigila la integridad y el cumplimiento: revisa la bitácora "
            "append-only, audita accesos y acciones, y monitorea el dashboard operativo. "
            "NO participa en la atención clínica."
        ),
        "imagen": "auditor_flujo.png",
        "animacion": "auditor_flujo.gif",
        "pantallas": [
            {
                "nombre": "Auditoría y trazabilidad",
                "objetivo": "Revisar toda acción sensible del sistema.",
                "pasos": [
                    "Abra «🕵️ Auditoría y trazabilidad».",
                    "Filtre por usuario, acción (CREAR_PACIENTE, CAMBIO_ESTADO, "
                    "ACTIVAR_MODELO…), entidad y fechas.",
                    "Exporte la evidencia a CSV, Excel o PDF.",
                ],
                "consejos": [
                    "Busque los eventos MODELO_INDISPONIBLE para detectar fallos de IA.",
                    "Revise CIERRE_SESION_INACTIVIDAD para evaluar higiene de sesiones.",
                ],
                "errores": ["Concluir sin cruzar filtros de usuario y rango de fechas."],
            },
            {
                "nombre": "Dashboard operativo",
                "objetivo": "Monitorear indicadores de operación y uso.",
                "pasos": [
                    "Abra «📈 Dashboard operativo».",
                    "Revise distribución de niveles, tiempos y concordancia.",
                ],
                "consejos": ["Compare períodos para detectar desviaciones."],
                "errores": [],
            },
        ],
        "advertencias": [
            "La auditoría es append-only: no se pueden modificar ni borrar registros.",
            "Reporte hallazgos al administrador sin alterar evidencia.",
        ],
    },
}


def contenido_manual(rol: str) -> dict | None:
    """Devuelve el manual del rol (None si el rol no tiene manual)."""
    return MANUAL_POR_ROL.get(rol)


# Pantallas RBAC que cada manual enseña (invariante: solo pantallas permitidas
# al rol). Se usa en tests para validar la consistencia manual ↔ permisos.
PANTALLAS_RBAC_POR_ROL: dict[str, set[str]] = {
    "Medico": {
        "registro_paciente", "signos_vitales", "evaluacion_clinica",
        "clasificacion_ia", "explicacion_shap", "validacion_triaje",
        "cierre_evento",
    },
    "Enfermera": {
        "registro_paciente", "buscar_paciente", "signos_vitales",
        "evaluacion_clinica", "clasificacion_ia", "cierre_evento",
    },
    "Administrador": {
        "inicio", "admin_roles", "gestion_modelos", "auditoria", "dashboard",
    },
    "Investigador": {
        "comparacion_modelos", "explicacion_shap", "historial_paciente",
        "gestion_modelos", "dashboard",
    },
    "Auditor": {"auditoria", "dashboard"},
}


def pantallas_rbac_del_rol(rol: str) -> set[str]:
    return PANTALLAS_RBAC_POR_ROL.get(rol, set())


def render() -> None:
    rol = st.session_state.get("usuario_rol", "")
    if not authorization_service.puede_acceder(rol, "manual_uso"):
        raise ProhibidoError("Acceso denegado al manual de uso", detalle=rol)

    manual = contenido_manual(rol)
    if manual is None:
        st.error(f"No hay manual definido para el rol «{rol}».")
        if st.button("← Volver al inicio"):
            st.session_state["pantalla"] = "inicio"
            st.rerun()
        return

    st.title(f"📖 {manual['titulo']}")
    st.caption(
        "Este manual es EXCLUSIVO de su rol. Cada rol del sistema ve únicamente "
        "las funciones que le corresponden."
    )
    st.info(manual["descripcion"])

    imagen = ASSETS_DIR / manual["imagen"]
    if imagen.exists():
        st.image(str(imagen), caption=f"Flujo de trabajo — {rol}", width="stretch")
    else:
        st.warning(
            f"Diagrama no disponible ({imagen.name}). Regénerelo con "
            "scripts/generar_diagramas_manual.py"
        )

    animacion = ASSETS_DIR / manual["animacion"]
    if animacion.exists():
        st.image(
            str(animacion),
            caption=f"🎬 Recorrido animado paso a paso — {rol}",
            width="stretch",
        )
    else:
        st.warning(
            f"Animación no disponible ({animacion.name}). Regénerela con "
            "scripts/generar_gifs_manual.py"
        )

    st.subheader("Pantallas disponibles para su rol")
    for pantalla in manual["pantallas"]:
        with st.expander(f"🖥 {pantalla['nombre']}", expanded=False):
            st.markdown(f"**Objetivo:** {pantalla['objetivo']}")
            st.markdown("**Paso a paso:**")
            for i, paso in enumerate(pantalla["pasos"], start=1):
                st.markdown(f"{i}. {paso}")
            if pantalla["consejos"]:
                st.markdown("**Consejos:**")
                for consejo in pantalla["consejos"]:
                    st.markdown(f"- 💡 {consejo}")
            if pantalla["errores"]:
                st.markdown("**Errores frecuentes a evitar:**")
                for error in pantalla["errores"]:
                    st.markdown(f"- ⚠ {error}")

    st.subheader("Advertencias importantes")
    for advertencia in manual["advertencias"]:
        st.warning(advertencia)

    st.divider()
    if st.button("← Volver al inicio"):
        st.session_state["pantalla"] = "inicio"
        st.rerun()
