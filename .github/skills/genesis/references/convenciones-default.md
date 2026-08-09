# Convenciones por defecto cuando `archi` no las decide

`archi` decide arquitectura macro (estilo, contenedores, atributos de calidad). No suele bajar
al nivel de convención de código — eso normalmente lo deriva `builder` de un módulo existente
(`builder/SKILL.md` §E). En greenfield no hay módulo del que derivarlas, así que `genesis`
aplica estos defaults cuando ni el `Documento_Arquitectura_*.md` ni
`Linea_Base_<Proyecto>.md` los fijan explícitamente. Ninguno de estos bloquea el arranque —
se documentan como supuesto en el reporte final (§Reporte final de `SKILL.md`).

Si el usuario corrige un default después de que `genesis` ya inicializó el repo, el ajuste se
aplica directamente sobre el código generado (renombrar/reconfigurar), no requiere reiniciar
todo el proceso.

## Nombrado

| Lenguaje | Archivos | Clases/Tipos | Métodos/funciones |
|---|---|---|---|
| Java / Kotlin | `PascalCase.java` | `PascalCase` | `camelCase` |
| C# | `PascalCase.cs` | `PascalCase` | `PascalCase` |
| Python | `snake_case.py` | `PascalCase` | `snake_case` |
| Go | `snake_case.go` | `PascalCase` (exportado) / `camelCase` (privado) | igual que tipos |
| Ruby | `snake_case.rb` | `PascalCase` | `snake_case` |
| PHP | `PascalCase.php` (PSR-1) | `PascalCase` | `camelCase` |
| TypeScript (backend) | `kebab-case.ts` (o `camelCase.ts` si el framework lo impone, ej. NestJS `nombre.service.ts`) | `PascalCase` | `camelCase` |
| TypeScript/JS (frontend) | `PascalCase.tsx` para componentes, `camelCase.ts` para hooks/utils | `PascalCase` | `camelCase` |

## Inyección de dependencias

| Stack | Default |
|---|---|
| Spring Boot | Constructor injection + `@Service`/`@Repository`/`@Component` (evitar `@Autowired` de campo) |
| .NET | Constructor injection registrado en el contenedor nativo (`Program.cs` / `IServiceCollection`) |
| NestJS | Constructor injection nativo del framework (decoradores `@Injectable()`) |
| FastAPI | `Depends()` de FastAPI |
| Django/Django REST | Sin contenedor de DI formal — se sigue la convención de imports directos del framework |
| Express/Fastify sin framework de DI | Constructor injection manual simple (sin librería externa salvo que el documento la pida) |

## Manejo de errores

Formato de error por defecto si no está decidido (JSON, cualquier stack HTTP):

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Descripción legible del error",
    "details": null
  }
}
```

- Códigos de error en `SCREAMING_SNAKE_CASE`, estables (no cambian aunque cambie el mensaje).
- Excepciones de dominio tipadas (no genéricas) capturadas en el borde (middleware/handler),
  nunca en cada controller individualmente.
- Stack trace visible solo si `NODE_ENV`/`ASPNETCORE_ENVIRONMENT`/`DEBUG` indican ambiente de
  desarrollo.

## Formato de API

| Aspecto | Default |
|---|---|
| Prefijo de rutas | `/api/v1` |
| Envoltorio de listas paginadas | `{ "data": [...], "meta": { "page": 1, "pageSize": 20, "total": 0 } }` |
| Parámetros de paginación | `page` + `pageSize` (query params) |
| Autenticación | Header `Authorization: Bearer <token>` (JWT) salvo que el documento indique otro mecanismo |
| Formato de fecha/hora | ISO 8601 UTC en todas las respuestas |
| Formato de ID en URL | UUID v4 |
| Códigos HTTP | 200 (lectura ok), 201 (creación ok), 204 (eliminación ok sin cuerpo), 400/422 (validación), 401 (no autenticado), 403 (no autorizado), 404 (no encontrado), 409 (conflicto/duplicado), 500 (error no controlado) |

## Testing

| Stack | Test runner por defecto | Estrategia inicial |
|---|---|---|
| Java/Kotlin | JUnit 5 (+ Mockito si hace falta mockear) | Un test de integración del endpoint de salud (Fase 6 de `SKILL.md`) |
| .NET | xUnit | Igual |
| Python | Pytest | Igual, con `TestClient` de FastAPI o el equivalente de Django |
| Go | `testing` estándar + `net/http/httptest` | Igual |
| Node/TS backend | Jest (o el que traiga el generador del framework) | Igual |
| Frontend | Vitest (proyectos Vite) / Jest + RTL (Next.js) | Un test trivial de que la app renderiza sin errores — `qa` se encarga de la estrategia completa después |

## Cuándo esto NO aplica

Si el `Documento_Arquitectura_*.md`, la `Linea_Base_<Proyecto>.md`, o una respuesta explícita
del usuario en la Fase 2.3 de `SKILL.md` ya fijan cualquiera de estos puntos, esa decisión
tiene prioridad total sobre el default de esta tabla — nunca lo sobrescribas.
