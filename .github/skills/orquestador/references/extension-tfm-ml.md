# Extensión del Orquestador — Fase ML y Fase Académica

> Este archivo se referencia desde `orquestador/SKILL.md`. Agrega dos ramas nuevas al árbol de
> decisión existente y dos fases nuevas a la secuencia completa, sin modificar el resto del
> pipeline ya documentado. Instalar copiando este archivo a
> `.github/skills/orquestador/references/extension-tfm-ml.md` y añadiendo las dos líneas de
> "instalación" indicadas al final de este documento en el árbol de decisión de `SKILL.md`.

## Rama nueva 1 — `validacion-cientifica-ml` (entre `tdd-implementacion` y `qa`)

```
│  ├── ¿`builder` activó el modo "Pipeline de Machine Learning" (§1.2bis) y
│  │    `tdd-implementacion` acaba de producir artifacts/metrics/ nuevos
│  │    (un modelo entrenado, baseline o candidato)?
│  │     └──→ validacion-cientifica-ml  (leakage, McNemar/DeLong, calibración,
│  │           equidad por subgrupo, model card)
│  │         ├── ❌ hallazgo bloqueante (leakage, sin significancia estadística,
│  │         │      brecha de equidad no documentada) → vuelve a tdd-implementacion
│  │         │      a corregir el pipeline, NO continúa a qa/entrega-continua
│  │         └── ✅ sin bloqueantes → continúa el flujo normal
│  │
│  ├── ¿El usuario pide "desplegar la demo", "cerrar el modelo como definitivo",
│  │    o dar por bueno un modelo para pasar a entrega-continua?
│  │     └──→ GATE: validacion-cientifica-ml debe haber corrido sin hallazgos
│  │           bloqueantes pendientes para ESE modelo específico antes de permitir
│  │           el paso a entrega-continua. Si el modelo cambió desde la última
│  │           auditoría (nuevo hiperparámetro, nuevo split, nuevos datos), se
│  │           re-ejecuta antes de aprobar el gate.
```

**Trigger de lenguaje natural adicional** (para sumar a la descripción del `orquestador`):
"ya entrené el modelo", "compara early vs late fusion", "¿cuál modelo gana?", "el modelo está
listo", "audita el pipeline de ML", "¿hay fuga de datos (leakage)?", "revisa el sesgo/equidad del
modelo", "genera el model card".

## Rama nueva 2 — `tfm-redactor` (fase nueva, después de `memoria`/`obsidian`)

```
│  └── ¿El proyecto es un TFM/TFG (existe un brief de finalización tipo
│       brief_finalizacion_tfm.md, o el usuario lo indica explícitamente) y
│       pide redactar capítulos, revisar cumplimiento normativo, o preparar
│       el depósito?
│        └──→ tfm-redactor
│            ├── Precondición: si el capítulo a redactar depende de
│            │    artifacts/metrics (típicamente Resultados/Conclusiones),
│            │    validacion-cientifica-ml debe haber corrido sin bloqueantes
│            │    para esos artefactos — si no ha corrido, tfm-redactor debe
│            │    señalarlo y no redactar esa sección con cifras sin auditar.
│            └── Salida final → docx (maquetación: portada, numeración,
│                 tabla de contenido, pies de página)
```

**Trigger de lenguaje natural adicional**: "redacta el capítulo", "prepara el depósito",
"¿puedo depositar ya?", "checklist antes de depositar", "convierte esto en hechos consumados",
"revisa si cumplo con el reglamento de UNIR".

## Secuencia completa de referencia — versión extendida

```
 0. memoria (lectura)
 1. janus  →  2. refinador  →  3. desglosador
 4. figma-prd-mockups  →  5. archi  →  6. genesis
 7. builder                              [detecta modo ML → activa 9.5 más abajo]
 8. context-engineering / source-driven-development
 9. tdd-implementacion                   → produce artifacts/metrics/ nuevos

 9.5  validacion-cientifica-ml  ★ NUEVO
      Fases 1-7 internas: leakage → CV estratificado → McNemar/DeLong →
      calibración → equidad por subgrupo → trazabilidad → model card
      │
      ├─ ❌ bloqueante → vuelve a 9 (tdd-implementacion)
      └─ ✅ sin bloqueantes → continúa

10. doubt-driven-development (solo si el slice es de alto riesgo)
11. qa                                    (E2E de la app/demo, no del modelo)
12. revision-calidad
13. seguridad-rendimiento
14. documentacion-observabilidad

 GATE  validacion-cientifica-ml (re-chequeo si el modelo cambió desde 9.5) ★ NUEVO

15. entrega-continua
16. memoria (escritura) + obsidian

17. tfm-redactor  ★ NUEVO — solo si el proyecto tiene entregable académico (TFM/TFG)
    Precondición: 9.5/GATE sin bloqueantes pendientes para los artefactos citados
    Auditoría normativa (checklist UNIR) + redacción capítulo por capítulo con
    evidencia trazable a artifacts/ → resources/tfm/capitulos/
    → docx (maquetación final)
```

## Instalación en `orquestador/SKILL.md`

1. Copiar este archivo a `.github/skills/orquestador/references/extension-tfm-ml.md`.
2. En el árbol de decisión de `SKILL.md`, dentro del bloque "A partir de aquí el código ya
   existe...", insertar la Rama nueva 1 justo después de la entrada de `tdd-implementacion` y
   antes de la entrada de `qa`.
3. Al final del árbol de decisión (después de la entrada de `memoria` modo escritura), insertar
   la Rama nueva 2.
4. En la sección "Secuencia completa de referencia" de `SKILL.md`, reemplazar el bloque de pasos
   9-16 por la versión extendida de este archivo (agrega 9.5, el GATE, y el paso 17).
5. Actualizar la lista de skills mencionados en el frontmatter `description` de
   `orquestador/SKILL.md` para incluir `validacion-cientifica-ml` y `tfm-redactor`, de forma que
   el meta-skill los reconozca desde la primera lectura de su propia descripción.
