# Comandos de inicialización por stack

Tabla inversa a la de detección de `builder/SKILL.md` §A/§B: en vez de detectar un ecosistema
desde manifiestos existentes, parte de la tecnología ya decidida en el
`Documento_Arquitectura_*.md` y da el comando real para inicializar el proyecto desde cero.

Si el framework detectado no aparece en esta tabla, no inventes un comando — busca la
documentación oficial de inicialización de ese framework (WebSearch/WebFetch) antes de
asumir uno.

## Java / Kotlin

| Framework | Comando de inicialización |
|---|---|
| Spring Boot (Maven) | `curl https://start.spring.io/starter.zip -d dependencies=web,data-jpa,<driver> -d type=maven-project -d javaVersion=<version> -o project.zip` (Spring Initializr) o `mvn archetype:generate` si no hay red disponible |
| Spring Boot (Gradle) | Igual vía Spring Initializr con `-d type=gradle-project`, o `gradle init --type java-application` |
| Quarkus | `mvn io.quarkus.platform:quarkus-maven-plugin:create` |
| Micronaut | `mn create-app <grupo>.<artefacto>` (CLI de Micronaut) |

Gestor de dependencias por defecto si no está decidido: Maven (mayor adopción corporativa).
Linter/formatter por defecto: Checkstyle + Spotless. Test runner: JUnit 5.

## C# / .NET

| Tipo de proyecto | Comando |
|---|---|
| Web API (controllers) | `dotnet new webapi -n <Nombre>` |
| Web API (minimal API) | `dotnet new web -n <Nombre>` |
| Solución completa | `dotnet new sln -n <Nombre>` + `dotnet sln add <proyecto>.csproj` |

Gestor de paquetes: NuGet (no hay alternativa real). Linter/formatter por defecto:
`dotnet format` + `.editorconfig`. Test runner: xUnit (`dotnet new xunit -n <Nombre>.Tests`).

## Python

| Framework | Comando |
|---|---|
| FastAPI | `poetry new <nombre>` (o `uv init <nombre>`) + `poetry add fastapi uvicorn` |
| Django | `django-admin startproject <nombre>` |
| Django REST Framework | Igual que Django + `pip install djangorestframework` y agregar a `INSTALLED_APPS` |
| Flask | `poetry new <nombre>` + `poetry add flask` (Flask no tiene generador propio de proyecto) |

Gestor de paquetes por defecto si no está decidido: Poetry (lockfile + resolución determinista;
usar `uv` solo si el documento/línea base ya lo menciona explícitamente). Linter/formatter:
Ruff. Test runner: Pytest.

## Go

| Detalle | Comando |
|---|---|
| Inicializar módulo | `go mod init <ruta-del-modulo>` (ej. `go mod init github.com/org/proyecto`) |
| Framework HTTP | Se agrega como dependencia normal (`go get github.com/gin-gonic/gin`, `github.com/labstack/echo/v4`, etc.) — Go no tiene generador de proyecto propio por framework |

Linter/formatter por defecto: `gofmt` + `golangci-lint`. Test runner: `testing` estándar de Go.

## Ruby

| Framework | Comando |
|---|---|
| Ruby on Rails | `rails new <nombre> --database=postgresql` (ajustar `--api` si es backend puro sin vistas) |
| Sinatra | No tiene generador propio: `bundle init` + agregar `gem "sinatra"` al Gemfile |

Gestor de paquetes: Bundler (estándar del ecosistema). Linter/formatter: RuboCop. Test runner:
RSpec (`rails generate rspec:install` si es Rails).

## PHP

| Framework | Comando |
|---|---|
| Laravel | `composer create-project laravel/laravel <nombre>` |
| Symfony | `composer create-project symfony/skeleton <nombre>` (agregar `symfony/webapp-pack` si necesita el stack completo) |

Gestor de paquetes: Composer. Linter/formatter: PHP-CS-Fixer. Test runner: PHPUnit.

## JavaScript / TypeScript — Backend (Node.js)

| Framework | Comando |
|---|---|
| NestJS | `nest new <nombre>` |
| Express (con TypeScript) | `npm init -y` + `npm install express` + `npm install -D typescript @types/express @types/node` + `npx tsc --init` |
| Fastify | `npm init fastify@latest <nombre>` |
| Hono | `npm create hono@latest <nombre>` |

Gestor de paquetes por defecto si no está decidido: npm (viene con Node, sin fricción de
instalación adicional; usar pnpm/yarn solo si el documento/línea base ya lo define). Linter/
formatter: ESLint + Prettier. Test runner: Jest (o el que traiga el propio generador, ej.
NestJS ya incluye Jest).

## JavaScript / TypeScript — Frontend

| Framework | Comando |
|---|---|
| React (SPA) | `npm create vite@latest <nombre> -- --template react-ts` |
| Next.js | `npx create-next-app@latest <nombre> --typescript` |
| Angular | `ng new <nombre>` (requiere `@angular/cli` instalado globalmente o vía `npx`) |
| Vue.js | `npm create vue@latest <nombre>` |
| Svelte | `npx sv create <nombre>` |

Test runner por defecto: Vitest para proyectos Vite-based, Jest + React Testing Library para
Next.js/CRA-style. Herramienta de pruebas E2E: dejar para que `qa` la incorpore cuando
corresponda — `genesis` no instala Playwright.

## Notas generales

- Si el documento de arquitectura pide una versión específica del lenguaje/framework, pásala
  como parámetro al comando de inicialización cuando el generador lo soporte (ej.
  `dotnet new webapi -n Api --framework net8.0`); si el generador no soporta fijar la versión
  al crear, ajústala inmediatamente después en el manifiesto (`.csproj`, `pyproject.toml`,
  `package.json` engines, `go.mod`).
- Ejecuta siempre el comando de inicialización dentro de la ruta ya resuelta por la topología
  de la Fase 3 (raíz del repo si es un solo contenedor, `apps/<contenedor>/` si es monorepo).
- Tras inicializar, elimina o adapta cualquier archivo de ejemplo que el generador agregue por
  defecto (ej. el `WeatherForecastController` de `dotnet new webapi`, el componente `App.tsx`
  de ejemplo de Vite) — no debe quedar código de muestra del framework mezclado con la
  plomería real de la Fase 6.
