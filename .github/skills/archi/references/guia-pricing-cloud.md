# Guía: Estimación de costos por proveedor de nube

Aplica cuando el Caso A activa el modo multi-nube (ver `references/guia-multi-cloud-deployment.md`), o cuando el usuario pide explícitamente el costo estimado de una arquitectura de despliegue ya definida en una sola nube.

> `Pricing_<Proyecto>.md` se guarda dentro de `resources/architecture/` — créala si no existe.

## Principio rector

No inventes precios de memoria — el pricing de la nube cambia con frecuencia y varía por región. **Usa WebSearch/WebFetch para obtener precios publicados vigentes** en el momento de generar el documento, y dedica un componente del costo a cada servicio identificado en el diagrama de despliegue correspondiente.

## Proceso

1. **Extrae la lista de servicios facturables** desde cada diagrama `.drawio` generado: cómputo (tipo/tamaño de instancia o vCPU+RAM equivalente), base de datos (motor + tamaño), cache, almacenamiento (GB estimados), transferencia de datos saliente, balanceador de carga, colas/mensajería, CDN. Ignora servicios sin costo relevante a la escala del proyecto (ej. IAM, Route 53 salvo el costo fijo de hosted zone).
2. **Dimensiona cada servicio** según los requerimientos no funcionales del documento (volumen de usuarios esperado, disponibilidad, picos de tráfico). Si el `.md` de specs no da suficiente información para dimensionar (ej. no dice cuántos usuarios concurrentes), documenta el supuesto de dimensionamiento explícitamente (ej. "se asume una carga inicial de 10,000 usuarios activos mensuales, tráfico moderado") — este supuesto también va en la sección 16 del documento de arquitectura.
3. **Busca el precio publicado** de cada ítem con WebSearch/WebFetch. Usa consultas específicas con el nombre exacto del SKU/tier y la región (por defecto la región principal más común salvo que el usuario indique otra: `us-east-1` para AWS, `eastus` para Azure, `us-central1` para GCP). Ejemplos de consulta:
   - `"AWS EC2 pricing t3.medium us-east-1 on-demand"`
   - `"Azure App Service pricing P1v3 East US"`
   - `"Google Cloud SQL pricing db-custom-2-7680 us-central1"`
   - Prioriza siempre la página oficial de pricing del proveedor (`aws.amazon.com/*/pricing`, `azure.microsoft.com/*/pricing`, `cloud.google.com/*/pricing`) sobre blogs de terceros.
4. **Arma la tabla de costos por proveedor** (una tabla por proveedor, ver plantilla abajo) y súmalas en un total mensual estimado.
5. **Arma la tabla comparativa** de los tres totales, con una columna de observaciones (ej. "AWS resulta más económico en cómputo pero más caro en salida de datos").
6. **Guarda el resultado** como `Pricing_<NombreProyecto>.md`.
7. Los mismos totales y tablas alimentan el reporte HTML (`references/plantilla-reporte-costos.md`) — no recalcules ni dupliques cifras entre ambos archivos.

## Plantilla de `Pricing_<Proyecto>.md`

```markdown
# Estimación de Costos de Despliegue: [Nombre del Proyecto]

**Fecha de la estimación:** [fecha]
**Región de referencia:** [región usada por proveedor, si difiere indicarlo por proveedor]

> ⚠️ **Esto es una estimación basada en precios públicos de lista (on-demand) vigentes a la fecha indicada.**
> No incluye: descuentos por volumen, instancias reservadas/committed use, planes de soporte, ni acuerdos empresariales.
> Valida las cifras finales en la calculadora oficial de cada proveedor antes de tomar decisiones de presupuesto:
> [AWS Pricing Calculator](https://calculator.aws) · [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator) · [Google Cloud Pricing Calculator](https://cloud.google.com/products/calculator)

## Supuestos de dimensionamiento

[Lista de supuestos de carga/tamaño usados para dimensionar cada servicio — ver paso 2 del proceso.]

## Comparativo de costo mensual estimado

| Proveedor | Cómputo | Base de datos | Storage | Red/CDN | Otros | **Total mensual estimado** |
|---|---|---|---|---|---|---|
| AWS | $[x] | $[x] | $[x] | $[x] | $[x] | **$[total]** |
| Azure | $[x] | $[x] | $[x] | $[x] | $[x] | **$[total]** |
| GCP | $[x] | $[x] | $[x] | $[x] | $[x] | **$[total]** |

## Detalle AWS

| Servicio | SKU / Tier | Cantidad | Precio unitario | Costo mensual estimado | Fuente |
|---|---|---|---|---|---|
| [ej. EC2] | [ej. t3.medium] | [ej. 2 instancias, 730h/mes] | $[x]/h | $[x] | [enlace a la página de pricing consultada] |

## Detalle Azure

[misma estructura de tabla]

## Detalle GCP

[misma estructura de tabla]

## Observaciones y recomendación

[2-4 líneas: qué proveedor conviene según el balance costo/requerimientos no funcionales del proyecto, y qué variable (ej. tráfico de salida, soporte 24/7, familiaridad del equipo) podría cambiar esa conclusión.]
```

## Reglas de honestidad

- Si no encuentras el precio exacto de un SKU específico, usa el tier equivalente más cercano y dilo explícitamente en la columna "Fuente" (ej. "aproximado por tier equivalente, no se encontró el SKU exacto").
- Nunca presentes un total como definitivo — siempre "estimado".
- Si el usuario ya tiene descuentos negociados o un Enterprise Agreement con algún proveedor, pregúntale antes de asumir precios de lista, ya que puede cambiar la conclusión por completo.
