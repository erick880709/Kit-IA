# Plantilla: Reporte HTML de arquitectura de despliegue y costos multi-nube

Se genera junto con `Pricing_<Proyecto>.md` cuando el Caso A activa el modo multi-nube (ver `references/guia-multi-cloud-deployment.md`). Es un único archivo `.html` autocontenido (CSS inline) que un no-técnico (ej. quien aprueba presupuesto) pueda abrir directamente en el navegador sin instalar nada, y ver: el contexto de cada arquitectura de despliegue, el diagrama con los iconos reales de cada nube, y el costo comparado.

Reemplaza todo lo que está entre `[...]` por el contenido real. El texto entre `<!-- -->` son instrucciones para ti, no deben aparecer en el archivo final. Guarda el resultado como `resources/architecture/Arquitectura_Costos_<NombreProyecto>.html` — crea la carpeta si no existe.

## Cómo embeber los diagramas .drawio

Usa el visor oficial de diagrams.net (`viewer.min.js`), que renderiza el XML del diagrama sin necesitar la app instalada. Toma el contenido de `<mxGraphModel>...</mxGraphModel>` del `.drawio` correspondiente (ver `references/drawio-iconos-nube.md`), escápalo como string JSON, e insértalo en el atributo `data-mxgraph` de un `<div class="mxgraph">`. No dupliques el diagrama a mano en SVG — reutiliza el mismo XML que generaste para el archivo `.drawio`.

## Esqueleto HTML

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Arquitectura de Despliegue y Costos — [Nombre del Proyecto]</title>
<style>
  :root {
    --aws-color: #ED7100;
    --azure-color: #0078D4;
    --gcp-color: #4285F4;
    --ink: #1a1a1a;
    --muted: #5f6368;
    --border: #e0e0e0;
    --bg-soft: #f7f8fa;
  }
  * { box-sizing: border-box; }
  body {
    font-family: -apple-system, "Segoe UI", Roboto, Arial, sans-serif;
    color: var(--ink);
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 24px 80px;
    line-height: 1.55;
  }
  h1 { font-size: 1.8rem; margin-bottom: 4px; }
  .subtitle { color: var(--muted); margin-top: 0; }
  h2 {
    margin-top: 48px;
    padding-bottom: 8px;
    border-bottom: 2px solid var(--border);
  }
  .provider-section { margin-top: 32px; }
  .provider-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 999px;
    color: #fff;
    font-weight: 600;
    font-size: 0.85rem;
  }
  .provider-badge.aws { background: var(--aws-color); }
  .provider-badge.azure { background: var(--azure-color); }
  .provider-badge.gcp { background: var(--gcp-color); }
  .diagram-wrap {
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 12px;
    background: #fff;
    margin: 16px 0;
    overflow-x: auto;
  }
  table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 0.92rem; }
  th, td { border: 1px solid var(--border); padding: 8px 10px; text-align: left; }
  th { background: var(--bg-soft); }
  td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
  .total-row td { font-weight: 700; background: var(--bg-soft); }
  .disclaimer {
    background: #fff8e1;
    border-left: 4px solid #f9a825;
    padding: 12px 16px;
    margin: 20px 0;
    font-size: 0.9rem;
  }
  .assumptions { background: var(--bg-soft); border-radius: 8px; padding: 16px 20px; }
  .recommendation { background: #eef7ee; border-left: 4px solid #34a853; padding: 16px 20px; border-radius: 4px; }
  footer { margin-top: 60px; color: var(--muted); font-size: 0.8rem; text-align: center; }
  @media print { body { padding: 0; } }
</style>
</head>
<body>

<h1>Arquitectura de Despliegue y Costos</h1>
<p class="subtitle">[Nombre del Proyecto] · Generado el [fecha] · Comparación AWS / Azure / GCP</p>

<div class="disclaimer">
  <strong>Nota sobre los costos:</strong> las cifras de este reporte son estimaciones basadas en precios públicos de lista (on-demand) vigentes a la fecha indicada. No incluyen descuentos por volumen, instancias reservadas ni acuerdos empresariales. Valida los montos finales en la calculadora oficial de cada proveedor:
  <a href="https://calculator.aws" target="_blank">AWS Pricing Calculator</a> ·
  <a href="https://azure.microsoft.com/pricing/calculator" target="_blank">Azure Pricing Calculator</a> ·
  <a href="https://cloud.google.com/products/calculator" target="_blank">Google Cloud Pricing Calculator</a>.
</div>

<h2>Resumen ejecutivo</h2>
<p>[2-4 líneas: qué arquitectura se evaluó, por qué se comparan las tres nubes (no había un proveedor definido en las especificaciones), y el hallazgo principal del comparativo de costo.]</p>

<div class="assumptions">
  <strong>Supuestos de dimensionamiento:</strong>
  <p>[Lista de supuestos de carga/tamaño usados para dimensionar los servicios — debe ser consistente con Pricing_&lt;Proyecto&gt;.md.]</p>
</div>

<h2>Comparativo de costo mensual estimado</h2>
<table>
  <thead>
    <tr><th>Proveedor</th><th class="num">Cómputo</th><th class="num">Base de datos</th><th class="num">Storage</th><th class="num">Red/CDN</th><th class="num">Otros</th><th class="num">Total mensual</th></tr>
  </thead>
  <tbody>
    <tr><td><span class="provider-badge aws">AWS</span></td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[total]</td></tr>
    <tr><td><span class="provider-badge azure">Azure</span></td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[total]</td></tr>
    <tr><td><span class="provider-badge gcp">GCP</span></td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[x]</td><td class="num">$[total]</td></tr>
  </tbody>
</table>

<!-- Repite este bloque completo por cada proveedor (AWS, Azure, GCP) -->
<div class="provider-section">
  <h2><span class="provider-badge aws">AWS</span> Arquitectura de despliegue</h2>
  <p>[2-4 líneas de contexto: cómo se mapean los contenedores del C4 a servicios AWS concretos, y por qué esas elecciones — ej. "el API se despliega en ECS Fargate por no requerir gestión de servidores, con RDS PostgreSQL Multi-AZ para alta disponibilidad".]</p>

  <div class="diagram-wrap">
    <div class="mxgraph" style="max-width:100%;" data-mxgraph="{&quot;toolbar&quot;:&quot;zoom&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;[PEGAR AQUÍ EL XML DE mxGraphModel DEL ARCHIVO Despliegue_AWS_&lt;Proyecto&gt;.drawio, ESCAPADO PARA HTML]&quot;}"></div>
  </div>

  <table>
    <thead><tr><th>Servicio</th><th>SKU / Tier</th><th>Cantidad</th><th class="num">Precio unitario</th><th class="num">Costo mensual</th></tr></thead>
    <tbody>
      <tr><td>[ej. EC2]</td><td>[ej. t3.medium]</td><td>[ej. 2 instancias]</td><td class="num">$[x]</td><td class="num">$[x]</td></tr>
      <tr class="total-row"><td colspan="4">Total AWS</td><td class="num">$[total]</td></tr>
    </tbody>
  </table>
</div>
<!-- Fin bloque repetible -->

<h2>Recomendación</h2>
<div class="recommendation">
  <p>[2-4 líneas: qué proveedor conviene dado el balance costo/requerimientos no funcionales del proyecto, y qué variable podría cambiar esa conclusión (ej. tráfico de salida real, soporte 24/7 necesario, familiaridad del equipo con el proveedor).]</p>
</div>

<footer>
  Generado con asistencia de IA a partir de <code>Documento_Arquitectura_[Proyecto].md</code> y <code>Pricing_[Proyecto].md</code>. Revisar antes de usar para decisiones de presupuesto.
</footer>

<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
</body>
</html>
```

## Reglas

- Un solo archivo `.html`, sin dependencias locales (la única referencia externa es el script del visor de diagrams.net, necesario para renderizar los `.drawio` embebidos — coméntaselo al usuario si va a distribuir el reporte a alguien sin acceso a internet, en cuyo caso puede reemplazarse por una captura estática exportada del diagrama).
- Los números de este HTML y de `Pricing_<Proyecto>.md` deben coincidir exactamente — genera ambos a partir de la misma tabla de costos, nunca la recalcules dos veces.
- Si el proyecto no está en modo multi-nube (ya hay un proveedor definido), no generes este reporte — el costo estimado para un solo proveedor va directo en `Pricing_<Proyecto>.md` sin necesidad del comparativo HTML.
