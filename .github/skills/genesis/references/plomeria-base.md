# Plomería base por patrón arquitectónico

Define qué archivos transversales (no específicos de un recurso de negocio) genera `genesis`
dentro del esqueleto de carpetas vacío que ya crea siguiendo `builder/SKILL.md` §2.1. El
objetivo es que el proyecto **arranque y responda** antes de que exista el primer módulo de
negocio real.

Todo lo de este archivo se genera una sola vez por contenedor, nunca por recurso.

## Piezas comunes a cualquier patrón

1. **Carga de configuración**: un módulo/clase que lee variables de entorno (con validación de
   las obligatorias al arrancar, no en cada uso) y expone la configuración tipada al resto de
   la app. Acompañado de `.env.example` con todas las variables documentadas (sin valores
   reales).
2. **Conexión a datos**: inicialización del cliente/ORM decidido en la Fase 1 de `SKILL.md`,
   con manejo de reconexión básico si el driver lo soporta de forma nativa. Sin modelos de
   negocio todavía — solo la conexión y, si el ORM lo requiere, el archivo de configuración
   de migraciones vacío (ej. `alembic init`, carpeta `prisma/` con `schema.prisma` con el
   `datasource`/`generator` pero sin `model`).
3. **Contenedor de DI / bootstrap de la aplicación**: el punto de entrada que ensambla
   configuración + conexión a datos + logging + manejo de errores + router, en el estilo que
   ya usa el framework (módulo raíz de NestJS, `Program.cs` de .NET, `main.py` de FastAPI,
   `Application.java` de Spring Boot, etc.).
4. **Manejo de errores centralizado**: middleware/handler global que captura excepciones no
   controladas y responde con el formato de error resuelto en la Fase 2 de `SKILL.md` (nunca
   expone stack traces en producción; sí en modo desarrollo si el framework lo soporta
   nativamente).
5. **Logging**: configuración mínima de la librería resuelta (nivel por ambiente, formato
   estructurado si el stack lo soporta sin esfuerzo extra — ej. JSON en producción).
6. **Endpoint/comando de salud**: `GET /health` (o `/api/v1/health` si ya se fijó ese prefijo)
   que responde `200 OK` con `{ "status": "ok", "timestamp": "<ISO8601>" }` cuando la app y su
   conexión a datos están operativas, y `503` con el mismo formato de error del proyecto si la
   conexión a datos falla. En un CLI o worker sin servidor HTTP, el equivalente es un comando
   (`<binario> health`) que verifica lo mismo y termina con código de salida 0/1.
7. **Test del endpoint de salud**: un test de integración mínimo que levanta la app (o un
   cliente de pruebas) y verifica que `/health` responde `200`. Es el único test que entrega
   `genesis` — prueba que toda la plomería anterior realmente se conecta, no es cobertura de
   negocio.

## Hexagonal / Clean Architecture

```
[shared o types]     → tipos base compartidos (ej. Result<T, E> o excepciones base de dominio)
[dominio]            → carpeta vacía, lista para la primera entidad real
[aplicación]         → carpeta vacía, lista para los primeros casos de uso
[infraestructura]
  → adaptador de conexión a datos (repositorio base / cliente ORM configurado)
  → adaptador HTTP: router raíz + controller de salud
  → registro en el contenedor de DI (health incluido)
```

## Layered / MVC

```
[modelo]       → configuración del ORM sin modelos de negocio
[repositorio]  → clase base/abstracta si el framework usa ese patrón; si no, se omite
[servicio]     → carpeta vacía
[controller]   → controller de salud
[rutas]        → router raíz que monta el controller de salud
```

## Modular (NestJS, Spring Modular)

```
[módulo raíz]     → importa el módulo de salud (HealthModule) y expone configuración global
[HealthModule]    → controller + service mínimos del endpoint de salud
[registro]        → el módulo raíz ya queda preparado para importar módulos de negocio futuros
```

## CQRS

```
[commands]  → carpeta vacía, lista para el primer Command/Handler real
[queries]   → carpeta vacía, lista para la primera Query/Handler real
[domain]    → carpeta vacía
[infrastructure]
  → repositorio de escritura/lectura base (conexión configurada, sin agregados todavía)
  → controller que despacha comandos/queries, con un endpoint de salud que no pasa por el
    bus de comandos (verificación directa de infraestructura, más rápida de diagnosticar)
```

## MVC Convencional (Rails, Django, Laravel)

```
[modelo]      → sin modelos de negocio; migración inicial vacía o solo con extensiones de BD
[controller]  → controller de salud (`HealthController`/`health_controller.rb`/vista Django)
[rutas]       → entrada de ruta de salud en el archivo de rutas del framework
```

## Vertical Slice / Feature-based

```
[feature/health]  → único feature inicial: controller + verificación de infraestructura
[registro]        → router central que monta el feature de salud, listo para sumar features
```

## Al terminar cada contenedor

Verifica (Fase 8 de `SKILL.md`) que el endpoint/comando de salud realmente responde antes de
continuar al siguiente contenedor o de cerrar la skill — no dejes la plomería sin probar.
