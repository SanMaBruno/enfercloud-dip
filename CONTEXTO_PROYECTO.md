# enferCloud — Contexto del Proyecto para Continuación

> Lee este archivo al inicio de cada sesión nueva para tener contexto completo del proyecto.

---

## Qué es esto

**enferCloud DIP** es una aplicación web hospitalaria que reemplaza una planilla Excel manual que llenaban las enfermeras diurnas para vigilar Dispositivos Invasivos en Pacientes (DIP).

- **Cliente**: Paolo Beroiza — UCI/UTI, Sala A. Covarrubias (hospital chileno)
- **Desarrollador**: Bruno San Martín Navarro (`@SanMaBruno`)
- **Repositorio**: `https://github.com/SanMaBruno/enfercloud-dip`
- **Producción**: `https://enfercloud-dip.onrender.com`

---

## Cómo clonar y correr en un PC nuevo

```bash
# 1. Clonar
git clone https://github.com/SanMaBruno/enfercloud-dip.git
cd enfercloud-dip

# 2. Instalar dependencias
cd backend
pip install -r requirements.txt

# 3. Levantar el servidor
python3 -m uvicorn main:app --reload --port 8000

# 4. Abrir en navegador
# http://localhost:8000

# 5. Correr tests (debe dar 9/9)
python3 -m pytest tests/ -v
```

---

## Stack técnico

| Capa | Tecnología |
|------|-----------|
| Backend | Python 3.11 · FastAPI · SQLAlchemy 2.x · SQLite |
| Export | openpyxl |
| Tests | pytest + httpx + SQLite in-memory (StaticPool) |
| Frontend | HTML5 · CSS3 · Vanilla JS · Tailwind CSS (CDN) |
| Charts | Chart.js 4.4 |
| Icons | Lucide |
| Deploy | Render.com (auto-deploy desde GitHub) |

---

## Arquitectura (Clean Architecture)

```
backend/
├── main.py                          ← FastAPI app + CORS + static files
├── .python-version                  ← 3.11.9 (fijado para Render)
├── requirements.txt
└── app/
    ├── domain/                      ← Entidades puras, enums, validadores
    │   ├── entities.py              ← RegistroDIP dataclass + propiedades calculadas
    │   ├── enums.py                 ← DIPTipo, Estado, UBICACIONES_POR_DIP
    │   └── validators.py           ← validar_ubicacion_dip()
    ├── application/                 ← Casos de uso (orquestan el dominio)
    │   ├── ports/
    │   │   └── record_repository.py ← Interface abstracta RecordRepository
    │   └── use_cases/
    │       ├── add_record.py
    │       ├── list_records.py
    │       ├── get_summary.py
    │       └── export_excel.py
    ├── infrastructure/              ← Implementaciones concretas
    │   ├── persistence/
    │   │   ├── database.py         ← engine, SessionLocal, get_db()
    │   │   ├── models.py           ← RegistroDIPModel (SQLAlchemy)
    │   │   └── sqlite_repository.py ← Implementa RecordRepository
    │   └── export/
    │       └── excel_exporter.py   ← OpenpyxlExcelExporter
    └── api/                        ← FastAPI layer
        ├── schemas.py              ← Pydantic schemas (Create/Update/Response)
        ├── dependencies.py         ← Dependency Injection
        └── routers/
            ├── records_router.py   ← /api/v1/registros/
            └── export_router.py    ← /api/v1/exportar/excel

frontend/
├── index.html                      ← SPA completo (HTML + CSS + JS inline)
└── assets/
    ├── css/styles.css
    └── js/api-client.js            ← Todas las llamadas HTTP a la API
```

---

## API REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/v1/registros/` | Listar registros (`?solo_activos=true`) |
| POST | `/api/v1/registros/` | Crear registro |
| GET | `/api/v1/registros/resumen` | KPIs del dashboard |
| GET | `/api/v1/registros/{id}` | Obtener un registro |
| PATCH | `/api/v1/registros/{id}` | Actualizar (ej: registrar retiro) |
| DELETE | `/api/v1/registros/{id}` | Eliminar |
| GET | `/api/v1/exportar/excel` | Descargar planilla Excel |

Documentación interactiva: `http://localhost:8000/docs`

---

## Servicios y Salas configurados

| Servicio | Salas |
|----------|-------|
| **UCI** | UCI · UTI Q |
| **UTI** | Borquez Silva · Hector Ducci · UTIM |
| **UHI** | UHI |
| **Medicina** | Manuel Matus · Gustavo Pineda · Álvaro Covarrubias · Joaquín Luco · Pérez Canto · Joel Rodríguez · Ricardo Donoso · RERA |
| **Cirugía** | Oftalmología · Ignacio Díaz · Eduardo Moore · San Daniel · San Vicente · San José · Jorge Molina · Torres Boone |

---

## DIPs y ubicaciones

| DIP | Ubicaciones válidas |
|-----|---------------------|
| CUP | GEN M · GEN F |
| CVC | YD · YI · SCD · SCI · FEM D · FEM I · BD · BI |
| VMI | TOT · TQT |
| CUP USUARIO · CVC CON GRIPPER · CHD AGUDO · CHD CRÓNICO · CHD AFERESIS · PICCLINE | N/A |

---

## Decisiones técnicas importantes

### Por qué StaticPool en tests
SQLite `:memory:` crea una DB por conexión. Con `StaticPool` todas las conexiones comparten la misma DB en memoria. Sin esto los tests fallan con "no such table".

### Por qué Python 3.11 fijado
Render usa Python 3.14 por defecto. `pydantic-core 2.23.4` no tiene wheels para 3.14 y falla al intentar compilar Rust en el filesystem read-only de Render. Solución: `backend/.python-version` con `3.11.9`.

### Por qué `--prefer-binary` en build command
Evita que pip intente compilar pydantic-core desde fuente (requiere Rust/Cargo) en ambientes con filesystem read-only.

### Por qué sidebar con `top:0;bottom:0` y no `inset-y:0`
`inset-y` no está soportado en versiones antiguas de Android WebView/Chrome. Usando propiedades explícitas garantiza compatibilidad universal.

### Por qué `translateX(-220px)` y no `translateX(-100%)`
En algunos Android browsers, `-100%` del elemento fixed se calcula incorrectamente. Valor absoluto es más confiable.

### Frontend como un solo index.html
Decisión deliberada para simplificar el deploy: FastAPI sirve el directorio `frontend/` como archivos estáticos. No hay build step, no hay bundler.

---

## Bugs corregidos (code review agosto 2026)

1. **`find_activos`** filtraba solo por `fecha_retiro IS NULL`, ignorando `estado`. Ahora requiere ambos.
2. **PATCH** no re-validaba `ubicacion_dip` al actualizar. Ahora pasa por `validar_ubicacion_dip()`.
3. **`delete`** era no-op silencioso si el ID no existía. Ahora lanza `ValueError`.
4. **`dias_dispositivo` / `dias_hospitalizacion`** podían ser negativos. Ahora usan `max(0, days)`.
5. **`get_db()`** no hacía rollback en excepciones. Corregido.
6. **Content-Disposition** sin comillas en filename. Corregido a RFC 6266.
7. **Schemas**: añadidos `max_length` y validación cruzada de fechas.
8. **`api-client.js`**: chequeo `body !== null` en lugar de falsy.

---

## Lo que falta (roadmap)

### Crítico para producción real
- [ ] **Autenticación JWT** — ahora cualquiera con la URL accede a todos los datos
- [ ] **HTTPS forzado** — Render ya lo provee, pero sin auth es insuficiente
- [ ] **Validación RUT chileno** (dígito verificador) + normalización de formato

### Base de datos
- [ ] Migrar a **PostgreSQL** (Render ofrece gratis 500MB) para que los datos persistan entre redeploys
- [ ] O pagar $7/mes en Render para activar el disco persistente de SQLite

### Funcionalidad
- [ ] Editar registros completos desde la tabla (ahora solo retiro y eliminar)
- [ ] Filtro por sala además de por servicio
- [ ] Alertas de dispositivos > 7 días (no solo > 14)
- [ ] Historial de cambios por paciente
- [ ] Reporte diario PDF / vista de impresión
- [ ] Módulo de criterios clínicos para detección de infecciones asociadas (IAAS)
- [ ] Integración con plataforma Tracker (signos vitales + cultivos)
- [ ] Módulo de IA para diagnóstico asistido
- [ ] Soporte multi-hospital

### Frontend
- [ ] Página de edición completa de registros
- [ ] Filtro por sala en la tabla
- [ ] SRI hashes en CDN (seguridad)
- [ ] Build de Tailwind CSS en lugar de CDN (performance)

---

## Deploy en Render

El `render.yaml` en la raíz configura todo automáticamente.

**Para redesplegar manualmente:**
1. Ir a `dashboard.render.com`
2. Servicio `enfercloud-dip`
3. "Manual Deploy" → "Deploy latest commit"

**Cuando se borra la DB** (cada redeploy en free tier), ejecutar este script para repoblar con 100 registros de prueba:

```bash
# Requiere: pip install httpx
python3 /tmp/seed_full.py   # si el archivo aún existe
# O correr el seed script desde el repositorio (ver más abajo)
```

---

## Seed de base de datos (para demos)

Si necesitas repoblar la base de datos de producción con datos de prueba, ejecutar este comando desde la terminal (requiere `httpx`):

```python
# seed_demo.py — correr con: python3 seed_demo.py
import httpx, random
from datetime import date, timedelta

API = "https://enfercloud-dip.onrender.com/api/v1"
# ... (ver script completo en historial de conversación con Claude)
```

El script completo está guardado localmente en `/tmp/seed_full.py` en la sesión original.

---

## Contexto de la conversación con Claude

Esta aplicación fue construida en una sesión extensa con Claude Code (claude-sonnet-4-6). Para continuar el trabajo:

1. Clona el repo en el nuevo PC
2. Abre Claude Code en el directorio del proyecto
3. Claude leerá `CLAUDE.md` y `AGENTS.md` automáticamente
4. Menciona este archivo para que Claude tenga el contexto completo
5. Los archivos de referencia originales del cliente (Excel, VBA) están en `.gitignore` — no están en el repo por seguridad

**Última sesión:** 29 agosto 2026  
**Commits en main:** 8+  
**Tests:** 9/9 pasando  
**Estado:** App funcional en producción, lista para demo con Paolo
