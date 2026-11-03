# Energy Management System

A backend for managing users and their associated devices. The project consists of three FastAPI microservices, each with its own PostgreSQL database, and uses Traefik to route HTTP requests. Currently, the system manages devices and a configured maximum consumption value; it does not collect or analyze consumption measurements.

## Architecture

```text
                         localhost:8080
Client / Postman ────────────► Traefik
                                ├── /auth    ──► auth-service   ──► auth-db
                                ├── /users   ──► user-service   ──► user-db
                                └── /devices ──► device-service ──► device-db
```

| Component | Responsibility | Local port |
| --- | --- | --- |
| Traefik | Routes requests by path prefix | `8080`; dashboard: `8081` |
| Auth Service | Registration, authentication, and JWT issuance | `8000` |
| User Service | User profile management | `8001` |
| Device Service | Device management and assignment | `8002` |
| PostgreSQL | Separate databases for auth, users, and devices | `5433`, `5434`, and `5435`, respectively |

The services validate JWTs locally using the same key and algorithm. Passwords are stored as bcrypt hashes. PostgreSQL data is persisted in separate Docker volumes. Tables are created at service startup using SQLAlchemy's `create_all`; this does not apply migrations to existing schemas.

## Requirements and startup

- Docker and Docker Compose installed and running.
- The ports listed above available on the local machine.
- In `docker-compose.yml`, the Docker socket mount for Traefik uses a path specific to the author's machine: `/Users/ionut/.docker/run/docker.sock`. Before starting, change the source to the Docker socket for your environment, for example `/var/run/docker.sock` where available.

From the project root:

```bash
docker compose up --build -d
docker compose ps
```

The gateway is available at `http://localhost:8080` and the Traefik dashboard at `http://localhost:8081/dashboard/`. Interactive FastAPI documentation is available directly on each service:

- Auth: http://localhost:8000/docs
- Users: http://localhost:8001/docs
- Devices: http://localhost:8002/docs

To view logs and stop the services:

```bash
docker compose logs -f
docker compose down
```

`docker compose down` preserves the volumes. To delete **all data** in the project's three databases, use `docker compose down -v`.

## Configuration

Compose configures the database connections and the following variables:

| Variable | Services | Default in Compose |
| --- | --- | --- |
| `DATABASE_URL` | all | PostgreSQL URL specific to each service |
| `SECRET_KEY` | all | `dev-secret-change-in-production-min-32-chars` |
| `ALGORITHM` | all | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | auth | `60` |

The key and algorithm must match across services. For development, the key can be overridden using the `SECRET_KEY` environment variable or a `.env` file at the project root, read by Compose. The default configuration, including the database password and the unauthenticated Traefik dashboard, is intended for local development.

## Authentication and usage flow

The supported roles are `admin` and `client`. A user registers with Auth Service and then logs in to obtain a token. Protected requests use the `Authorization: Bearer <token>` header. An administrator separately creates profiles in User Service and manages devices. A client can list devices associated with their identity.

A minimal example through the gateway:

```bash
curl -X POST http://localhost:8080/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin1","password":"admin123","role":"admin"}'

curl -X POST http://localhost:8080/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"admin1","password":"admin123"}'
```

Use the `access_token` value from the response in subsequent requests:

```bash
curl -X POST http://localhost:8080/devices \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer <ADMIN_TOKEN>' \
  -d '{"name":"Smart Meter 1","max_consumption":120.5}'
```

`max_consumption` is a number; the code does not define a unit of measurement or enforce a positive value. A newly created device is unassigned. For a complete registration, profile creation, and assignment flow, import the collection and environment described in [postman/README.md](postman/README.md). The collection assumes clean databases and matching credential and profile IDs; see the limitations below before using it with existing data.

## API

All paths below can be called through `http://localhost:8080` or directly on the corresponding service's port. `PUT` requires all fields in the update schema, not just the changed fields.

| Method and path | Access | Description |
| --- | --- | --- |
| `POST /auth/register` | public | Creates credentials: `username`, `password`, `role` |
| `POST /auth/login` | public | Accepts `username` and `password`; returns a token and role |
| `GET /auth/verify`, `GET /auth/me` | valid token | Returns the JWT payload |
| `POST /users` | admin | Creates a profile: `username`, `name`, `email`, optional `address`, `role` |
| `GET /users` | admin | Lists profiles |
| `GET /users/{user_id}` | admin | Returns a profile |
| `PUT /users/{user_id}` | admin | Updates a profile using the same fields as creation |
| `DELETE /users/{user_id}` | admin | Deletes a profile |
| `POST /devices` | admin | Creates a device with `name` and `max_consumption` |
| `GET /devices` | admin | Lists devices |
| `GET /devices/me` | client | Lists devices assigned to the ID in the token |
| `GET /devices/{device_id}` | admin | Returns a device |
| `PUT /devices/{device_id}` | admin | Updates `name` and `max_consumption` |
| `DELETE /devices/{device_id}` | admin | Deletes a device |
| `POST /devices/{device_id}/assign` | admin | Assigns a device using the body `{"user_id": 1}` |
| `POST /devices/{device_id}/unassign` | admin | Removes the assignment |

Each service also exposes `GET /` for a simple status message, accessible directly on its port. See the FastAPI documentation for schema and response details.

## Project structure

```text
auth-service/       Credentials, passwords, and JWTs
user-service/       User profiles
device-service/     Devices and assignments
docker-compose.yml  Services, databases, volumes, and Traefik
postman/            Collection and environment for manual testing
docs/               Project PDF documents
```

Within each service's `app/` directory, HTTP routes, service logic, SQLAlchemy models, Pydantic schemas, authentication dependencies, and database configuration are kept separate.

## Current limitations

- Registration is public and allows callers to select the `admin` role. Together with the default key and exposed dashboard, this makes the configuration unsuitable for production.
- Credentials and profiles are created independently, have separately generated IDs, and are not synchronized. Updating or deleting a profile does not update the Auth Service identity or the role in an existing token.
- Device Service does not check whether a user exists when assigning a device. `GET /devices/me` compares the stored `user_id` with the credential ID in the JWT, while profiles have their own IDs. These can differ, so assigning by profile ID can show devices to the wrong client or to no client.
- The repository contains no database migrations or automated test suite. The Postman collection provides a manual verification flow.
- Measurement collection, consumption monitoring, and alerts are not implemented; `max_consumption` is only stored.
