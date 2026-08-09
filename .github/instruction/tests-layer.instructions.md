---
applyTo: "test/**"
description: "Reglas para tests Jest: unit tests de use cases y handlers, integration tests de endpoints"
---

# Instrucciones — Carpeta `test/`

## Estructura esperada

```
test/
├── unit/
│   ├── use-cases/    # Mockear repositorios con jest.fn()
│   └── handlers/     # Mockear use cases, verificar HttpResponseInit
└── integration/
    └── functions/    # Flujo HTTP completo (request → response)
```

## Patrón obligatorio para unit tests de use cases

```typescript
describe("<Verb><Resource>UseCase", () => {
  let useCase: <Verb><Resource>UseCase;
  let mockRepo: jest.Mocked<I<Resource>Repository>;

  beforeEach(() => {
    // Crear mock tipado del repositorio
    mockRepo = {
      findById: jest.fn(),
      findAll: jest.fn(),
      save: jest.fn(),
      delete: jest.fn(),
    };
    useCase = new <Verb><Resource>UseCase(mockRepo);
  });

  it("debería <acción exitosa> cuando <condición>", async () => {
    // Arrange
    mockRepo.save.mockResolvedValue(new <Resource>Entity({ id: "uuid-test" }));
    // Act
    const result = await useCase.execute({ /* dto válido */ });
    // Assert
    expect(result.id).toBe("uuid-test");
    expect(mockRepo.save).toHaveBeenCalledTimes(1);
  });

  it("debería lanzar NotFoundError cuando <recurso> no existe", async () => {
    mockRepo.findById.mockResolvedValue(null);
    await expect(useCase.execute({ id: "no-existe" }))
      .rejects.toThrow(NotFoundError);
  });
});
```

## Reglas

- Patrón **Arrange / Act / Assert** con comentarios en español.
- Nombres descriptivos en español: `"debería lanzar ValidationError cuando el input está vacío"`.
- Un solo `expect` por comportamiento cuando sea posible.
- Para errores async: `await expect(promise).rejects.toThrow(EspecificError)`.
- `beforeEach` para inicializar mocks — `afterAll` para cerrar la DB en integration tests.
- Cobertura mínima: `domain/` ≥ 90%, `application/use-cases/` ≥ 85%, `handlers/` ≥ 75%.
- **NO** hacer llamadas reales a Azure AD, Key Vault ni bases de datos externas en unit tests.
