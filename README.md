# CanchApp API — Sistema de Reservas de Canchas Deportivas

API REST construida con **FastAPI**, **SQLAlchemy**, **Alembic**, **PostgreSQL** y
**Docker**. Permite administrar canchas deportivas y gestionar sus reservas,
validando la disponibilidad de horarios para evitar empalmes.

Proyecto de la materia **Desarrollo de Software Backend 1** — CESUN Universidad.

---

## Tecnologías

- **FastAPI** — framework de la API.
- **SQLAlchemy** — ORM para la base de datos.
- **Alembic** — migraciones de la base de datos.
- **PostgreSQL** — base de datos relacional.
- **Pydantic** — validación y esquemas de respuesta.
- **Docker + Docker Compose** — contenerización del entorno.

---

## Estructura del proyecto

```
canchapp/
├── app/
│   ├── main.py            # Punto de entrada de la API
│   ├── database.py        # Conexión y sesión de SQLAlchemy
│   ├── errors.py          # Manejo de errores de negocio
│   ├── canchas/           # Módulo Canchas (modelo, schemas, rutas)
│   └── reservas/          # Módulo Reservas (modelo, schemas, rutas)
├── alembic/               # Migraciones
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh          # Corre migraciones y levanta la API
├── requirements.txt
├── .env.example
└── README.md
```

## Validaciones y reglas de negocio

- **Cancha:** el nombre no puede repetirse; el precio debe ser mayor a 0.
- **Reserva:** la cancha debe existir y estar disponible; la hora de fin debe ser
  posterior a la de inicio; no puede haber dos reservas encimadas en la misma
  cancha y horario; el estado debe ser válido (confirmada, cancelada, completada).
- **Pago:** el monto se calcula automáticamente (horas × precio de la cancha);
  una reserva no puede pagarse dos veces ni pagarse si está cancelada; el método
  debe ser efectivo, tarjeta o transferencia.

Todos los errores se devuelven con un formato consistente
(`{"success": false, "error": "mensaje"}`) y el código HTTP correcto.

## Endpoints de utilidad

- `GET /` — mensaje de bienvenida.
- `GET /health` — verificación de estado (health check) para Docker.

---

## Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/DiegoRiv10/proyecto-backend.git
cd proyecto-backend
```

### 2. Crear el archivo de variables de entorno

Copia el archivo de ejemplo y ajústalo si lo necesitas:

```bash
cp .env.example .env
```

### 3. Levantar el proyecto con Docker

```bash
docker compose up --build
```

Este comando construye la imagen, levanta PostgreSQL, aplica las migraciones de
Alembic automáticamente y arranca la API.

### 4. Abrir la documentación

Una vez levantado, la API queda disponible en:

- API: <http://localhost:8000>
- Documentación interactiva (Swagger): <http://localhost:8000/docs>

---

## Entidades

### Cancha
`id`, `nombre`, `tipo`, `precio_hora`, `disponible`.

### Reserva
`id`, `cancha_id`, `nombre_cliente`, `email_cliente`, `fecha`,
`hora_inicio`, `hora_fin`, `estado`. Cada reserva pertenece a una cancha.

### Pago
`id`, `reserva_id`, `monto`, `metodo`, `estado`, `fecha_pago`.
Cada pago pertenece a una reserva (relación uno a uno).

**Regla de negocio:** el `monto` del pago **no lo envía el cliente**: la API lo
calcula automáticamente multiplicando las horas reservadas por el precio por hora
de la cancha. Además, una reserva no puede pagarse dos veces ni pagarse si está
cancelada.

---

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/canchas/` | Crear una cancha |
| GET | `/api/v1/canchas/` | Listar canchas (filtros: tipo, disponible) |
| GET | `/api/v1/canchas/{id}` | Obtener una cancha |
| PUT | `/api/v1/canchas/{id}` | Actualizar una cancha |
| DELETE | `/api/v1/canchas/{id}` | Eliminar una cancha |
| POST | `/api/v1/reservas/` | Crear una reserva |
| GET | `/api/v1/reservas/` | Listar reservas (filtros: cancha_id, estado) |
| GET | `/api/v1/reservas/{id}` | Obtener una reserva |
| PUT | `/api/v1/reservas/{id}` | Actualizar una reserva |
| PATCH | `/api/v1/reservas/{id}` | Cambiar el estado de una reserva |
| DELETE | `/api/v1/reservas/{id}` | Eliminar una reserva |
| POST | `/api/v1/pagos/` | Registrar el pago de una reserva (monto automático) |
| GET | `/api/v1/pagos/` | Listar pagos (filtros: metodo, estado) |
| GET | `/api/v1/pagos/{id}` | Obtener un pago |
| PATCH | `/api/v1/pagos/{id}` | Actualizar método o estado de un pago |
| DELETE | `/api/v1/pagos/{id}` | Eliminar un pago |

---

## Migraciones (Alembic)

Las migraciones se aplican solas al levantar el contenedor. Para crear una nueva
migración tras cambiar los modelos:

```bash
docker compose exec api alembic revision --autogenerate -m "descripcion"
docker compose exec api alembic upgrade head
```

---

## Autor

**Diego Rivera** — Desarrollo de Software, CESUN Universidad.
