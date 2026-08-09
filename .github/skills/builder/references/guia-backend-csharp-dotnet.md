# Guía Senior: Backend C# / .NET

Patrones, anti-patrones y convenciones para scaffolds de backend C# con ASP.NET Core 8+. Aplica a .NET 8 LTS y superior.

---

## Estructura de proyecto (Clean Architecture)

```
src/
├── <Proyecto>.Domain/                # Capa de dominio — sin dependencias NuGet
│   ├── Entities/
│   │   └── <Entidad>.cs
│   ├── ValueObjects/
│   │   └── <Entidad>Id.cs
│   ├── Enums/
│   │   └── OrderStatus.cs
│   ├── Exceptions/
│   │   └── DomainException.cs
│   └── Interfaces/                   # Puertos (abstracciones)
│       ├── I<Entidad>Repository.cs
│       └── IUnitOfWork.cs
├── <Proyecto>.Application/           # Casos de uso + DTOs
│   ├── <Entidad>s/
│   │   ├── Commands/
│   │   │   ├── Create<Entidad>.cs
│   │   │   └── Update<Entidad>.cs
│   │   ├── Queries/
│   │   │   ├── Get<Entidad>ById.cs
│   │   │   └── List<Entidad>s.cs
│   │   └── DTOs/
│   │       ├── <Entidad>Request.cs
│   │       └── <Entidad>Response.cs
│   ├── Common/
│   │   ├── Interfaces/              # IApplicationDbContext, etc.
│   │   └── Behaviours/              # MediatR pipeline behaviours (logging, validation)
│   │       └── ValidationBehaviour.cs
│   └── DependencyInjection.cs       # Registro de MediatR, FluentValidation, AutoMapper
├── <Proyecto>.Infrastructure/        # Adaptadores
│   ├── Persistence/
│   │   ├── Configurations/          # IEntityTypeConfiguration<T> (Fluent API)
│   │   │   └── <Entidad>Configuration.cs
│   │   ├── Repositories/
│   │   │   └── <Entidad>Repository.cs
│   │   ├── AppDbContext.cs
│   │   └── Migrations/
│   ├── Services/                    # Clientes HTTP, email, storage
│   └── DependencyInjection.cs
└── <Proyecto>.Api/                   # Minimal API o Controllers
    ├── Endpoints/
    │   └── <Entidad>Endpoints.cs     # Minimal API: MapGroup + MapGet/MapPost
    ├── Middleware/
    │   └── GlobalExceptionMiddleware.cs
    ├── Program.cs
    └── appsettings.json
```

## Reglas de diseño senior

### 1. Minimal API como default, Controllers si el equipo lo pide

**✅ Default greenfield:** Minimal API con `MapGroup`. Más rápido, menos boilerplate, mejor performance.

```csharp
// Program.cs
var builder = WebApplication.CreateBuilder(args);
builder.Services.AddApplication();
builder.Services.AddInfrastructure(builder.Configuration);

var app = builder.Build();
app.UseMiddleware<GlobalExceptionMiddleware>();
app.MapOrderEndpoints();
app.Run();

// Endpoints/OrderEndpoints.cs
public static class OrderEndpoints
{
    public static void MapOrderEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/orders")
            .WithTags("Orders")
            .RequireAuthorization();

        group.MapGet("/", async (ISender sender, [AsParameters] ListOrdersQuery query) =>
        {
            var result = await sender.Send(query);
            return Results.Ok(result);
        })
        .WithName("ListOrders")
        .Produces<PaginatedList<OrderResponse>>();

        group.MapGet("/{id:guid}", async (ISender sender, Guid id) =>
        {
            var result = await sender.Send(new GetOrderByIdQuery(id));
            return result is not null ? Results.Ok(result) : Results.NotFound();
        })
        .WithName("GetOrder")
        .Produces<OrderResponse>()
        .Produces(404);

        group.MapPost("/", async (ISender sender, CreateOrderCommand command) =>
        {
            var result = await sender.Send(command);
            return Results.Created($"/api/orders/{result.Id}", result);
        })
        .WithName("CreateOrder")
        .Produces<OrderResponse>(201)
        .ProducesValidationProblem();
    }
}
```

### 2. CQRS con MediatR — comando SIEMPRE inmutable

```csharp
// Command: record (inmutable por defecto)
public record CreateOrderCommand(
    Guid CustomerId,
    List<OrderItemDto> Items,
    string? Notes = null
) : IRequest<OrderResponse>;

// Query: record con paginación
public record ListOrdersQuery(
    OrderStatus? Status = null,
    int Page = 1,
    int PageSize = 20
) : IRequest<PaginatedList<OrderResponse>>;

// Handler: clases separadas, una por comando/query
public sealed class CreateOrderCommandHandler(
    IOrderRepository repo,
    IUnitOfWork uow,
    IMapper mapper
) : IRequestHandler<CreateOrderCommand, OrderResponse>
{
    public async Task<OrderResponse> Handle(CreateOrderCommand cmd, CancellationToken ct)
    {
        var order = Order.Create(cmd.CustomerId, cmd.Items.Select(i => (i.ProductId, i.Quantity)));
        await repo.AddAsync(order, ct);
        await uow.SaveChangesAsync(ct);
        return mapper.Map<OrderResponse>(order);
    }
}
```

### 3. FluentValidation — pipeline behaviour automático

```csharp
// Validación (FluentValidation)
public class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        RuleFor(x => x.CustomerId).NotEmpty();
        RuleFor(x => x.Items).NotEmpty().WithMessage("La orden debe tener al menos un ítem");
        RuleForEach(x => x.Items).ChildRules(item =>
        {
            item.RuleFor(i => i.ProductId).NotEmpty();
            item.RuleFor(i => i.Quantity).GreaterThan(0);
        });
    }
}

// Pipeline behaviour (registrado en DI, se ejecuta ANTES de cada handler)
public class ValidationBehaviour<TRequest, TResponse>(
    IEnumerable<IValidator<TRequest>> validators
) : IPipelineBehavior<TRequest, TResponse>
    where TRequest : IRequest<TResponse>
{
    public async Task<TResponse> Handle(TRequest request,
        RequestHandlerDelegate<TResponse> next, CancellationToken ct)
    {
        if (!validators.Any()) return await next();

        var context = new ValidationContext<TRequest>(request);
        var failures = validators
            .Select(v => v.Validate(context))
            .SelectMany(r => r.Errors)
            .Where(f => f is not null)
            .ToList();

        if (failures.Count != 0) throw new ValidationException(failures);

        return await next();
    }
}
```

### 4. Entity Framework: Fluent API (no Data Annotations)

**✅ Siempre:** configuraciones en clases separadas con `IEntityTypeConfiguration<T>`. Las Data Annotations mezclan infraestructura con dominio.

```csharp
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.ToTable("Orders");
        builder.HasKey(o => o.Id);
        builder.Property(o => o.Id)
            .HasConversion(id => id.Value, value => new OrderId(value));

        builder.Property(o => o.Status)
            .HasConversion<string>()
            .HasMaxLength(20);

        builder.OwnsOne(o => o.ShippingAddress, address =>
        {
            address.Property(a => a.Street).HasMaxLength(200);
            address.Property(a => a.City).HasMaxLength(100);
        });

        builder.HasMany(o => o.Items)
            .WithOne()
            .HasForeignKey(i => i.OrderId)
            .OnDelete(DeleteBehavior.Cascade);
    }
}
```

### 5. Global Exception Middleware

```csharp
public class GlobalExceptionMiddleware(RequestDelegate next, ILogger<GlobalExceptionMiddleware> logger)
{
    public async Task InvokeAsync(HttpContext context)
    {
        try
        {
            await next(context);
        }
        catch (ValidationException ex)
        {
            context.Response.StatusCode = 400;
            var errors = ex.Errors.GroupBy(e => e.PropertyName)
                .ToDictionary(g => g.Key, g => g.Select(e => e.ErrorMessage).ToArray());
            await context.Response.WriteAsJsonAsync(new { title = "Error de validación", errors });
        }
        catch (NotFoundException ex)
        {
            context.Response.StatusCode = 404;
            await context.Response.WriteAsJsonAsync(new { title = "Recurso no encontrado", detail = ex.Message });
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Error no manejado");
            context.Response.StatusCode = 500;
            await context.Response.WriteAsJsonAsync(new { title = "Error interno", detail = "Contacte al equipo de soporte" });
        }
    }
}
```

### 6. Primary Constructors (C# 12+)

**✅ Usar siempre para servicios y handlers** — menos boilerplate, inyección clara.

```csharp
// Antes (C# 11): mucho boilerplate
public class OrderService
{
    private readonly IOrderRepository _repo;
    private readonly IMapper _mapper;
    public OrderService(IOrderRepository repo, IMapper mapper) { _repo = repo; _mapper = mapper; }
}

// Ahora (C# 12+): primary constructor
public class OrderService(IOrderRepository repo, IMapper mapper)
{
    // _repo y _mapper disponibles como parámetros capturados
}
```

### 7. Testing — reglas de oro

| Tipo | Framework | Convención |
|---|---|---|
| **Unitario (dominio)** | xUnit + FluentAssertions | Nombre: `<Clase>Tests`. Sin dependencias externas. |
| **Integración (repo)** | xUnit + Testcontainers (PostgreSQL) | Nombre: `<Entidad>RepositoryTests`. Container real. |
| **Integración (API)** | `WebApplicationFactory<T>` + xUnit | Nombre: `<Entidad>EndpointTests`. En memoria o Testcontainers. |

```csharp
public class OrderTests
{
    [Fact]
    public void MarkAsShipped_WhenOrderIsPaid_ShouldChangeStatus()
    {
        // Arrange
        var order = Order.Create(customerId, items);
        order.MarkAsPaid();

        // Act
        order.MarkAsShipped();

        // Assert
        order.Status.Should().Be(OrderStatus.Shipped);
    }

    [Fact]
    public void MarkAsShipped_WhenOrderIsPending_ShouldThrow()
    {
        var order = Order.Create(customerId, items);
        Action act = () => order.MarkAsShipped();
        act.Should().Throw<DomainException>()
            .WithMessage("*pagada*");
    }
}
```

## Stack recomendado por defecto (greenfield)

| Rol | Tecnología | Alternativa |
|---|---|---|
| Lenguaje | C# 12 | — |
| Runtime | .NET 8 (LTS) | .NET 9 (STS) |
| API | ASP.NET Core Minimal API | Controllers (si el equipo lo prefiere) |
| CQRS | MediatR + FluentValidation | — |
| ORM | Entity Framework Core 8 | Dapper (si performance crítica) |
| Migraciones | EF Core Migrations | DbUp, FluentMigrator |
| Mapeo | AutoMapper / Mapster | — |
| Testing | xUnit + FluentAssertions + NSubstitute | — |
| API Docs | Microsoft.AspNetCore.OpenApi + Scalar | Swashbuckle (Swagger) |
| Observabilidad | OpenTelemetry + Serilog | Application Insights (si Azure) |
| Container | `mcr.microsoft.com/dotnet/aspnet:8.0` (chiseled) | Alpine |
