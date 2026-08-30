<div align="center">

<br/>

<img src="https://img.shields.io/badge/enferCloud-DIP-0c8ee8?style=for-the-badge&logo=heart&logoColor=white" alt="enferCloud DIP" />

# enferCloud — Vigilancia DIP

**Sistema digital de vigilancia de Dispositivos Invasivos en Pacientes hospitalarios**

Reemplaza la planilla Excel manual que completaban las enfermeras diurnas por un **dashboard web completo**: ingreso de datos, cálculos automáticos, resumen dinámico y exportación Excel con un clic.

<br/>

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![TailwindCSS](https://img.shields.io/badge/Tailwind-3-06B6D4?style=flat-square&logo=tailwindcss&logoColor=white)](https://tailwindcss.com)
[![License](https://img.shields.io/badge/Licencia-MIT-green?style=flat-square)](LICENSE)

<br/>

</div>

---

## ¿Qué problema resuelve?

En salas hospitalarias, las enfermeras diurnas registraban **a mano** en planillas Excel la vigilancia de cada paciente con dispositivo invasivo (sonda Foley, catéter venoso central, ventilación mecánica, etc.).

Ese proceso era lento, propenso a errores y no generaba reportes automáticos. **enferCloud DIP** digitaliza todo el flujo:

```
Antes → Excel manual  →  cálculos a mano  →  resumen manual  →  planilla impresa
Ahora → Formulario web  →  cálculos automáticos  →  dashboard en tiempo real  →  Excel descargable
```

---

## Funcionalidades

| Funcionalidad | Descripción |
|---|---|
| 📋 **Ingreso de registros** | Formulario web con validación de ubicaciones por tipo de DIP |
| 🏥 **5 Servicios · 19 Salas** | UCI, UTI, UHI, Medicina y Cirugía con sus salas reales |
| 📊 **Dashboard en tiempo real** | KPIs, gráfico de distribución, días por dispositivo |
| ⏱️ **Cálculo automático** | Días de uso del dispositivo y días de hospitalización |
| 🔔 **Alertas visuales** | Destaca en ámbar los dispositivos con más de 14 días |
| 📁 **Exportación Excel** | Planilla lista con todos los datos y formato profesional |
| 🔍 **Filtros avanzados** | Por servicio, sala, estado activo/inactivo, búsqueda libre |
| ✅ **Validaciones clínicas** | Ubicaciones de DIP según protocolo (CUP: GEN M/F, CVC: YD/YI/etc.) |

---

## Estructura del proyecto

```
enfercloud-dip/
├── backend/
│   ├── main.py                          # FastAPI app
│   ├── requirements.txt
│   ├── app/
│   │   ├── domain/                      # Entidades, enums, validadores
│   │   │   ├── entities.py
│   │   │   ├── enums.py
│   │   │   └── validators.py
│   │   ├── application/                 # Casos de uso (Clean Architecture)
│   │   │   ├── ports/                   # Interfaces abstractas (DIP)
│   │   │   └── use_cases/               # AddRecord, ListRecords, GetSummary, ExportExcel
│   │   ├── infrastructure/              # SQLite, exportador Excel
│   │   │   ├── persistence/
│   │   │   └── export/
│   │   └── api/                         # FastAPI routers, schemas Pydantic
│   │       ├── routers/
│   │       ├── schemas.py
│   │       └── dependencies.py
│   └── tests/                           # 9 tests de integración
└── frontend/
    ├── index.html                       # SPA — dashboard completo
    └── assets/
        ├── css/styles.css
        └── js/api-client.js
```

### Arquitectura

```
┌─────────────────────────────────────────┐
│              Frontend (SPA)             │
│         HTML · CSS · Vanilla JS         │
└────────────────┬────────────────────────┘
                 │ HTTP REST
┌────────────────▼────────────────────────┐
│            FastAPI (API REST)           │
│  ┌──────────┐  ┌───────────────────┐   │
│  │  Routers │  │  Schemas Pydantic │   │
│  └────┬─────┘  └───────────────────┘   │
│       │  Dependency Injection           │
│  ┌────▼──────────────────────────────┐ │
│  │         Casos de Uso              │ │
│  │  AddRecord · GetSummary · Export  │ │
│  └────┬──────────────────────────────┘ │
│       │  Puerto abstracto              │
│  ┌────▼──────────────────────────────┐ │
│  │     SQLiteRecordRepository        │ │
│  │     OpenpyxlExcelExporter         │ │
│  └────┬──────────────────────────────┘ │
└───────┼─────────────────────────────────┘
        │
┌───────▼──────┐
│  SQLite DB   │
└──────────────┘
```

---

## Instalación y uso local

### Requisitos
- Python 3.9+
- pip

### 1. Clonar el repositorio

```bash
git clone https://github.com/SanMaBruno/enfercloud-dip.git
cd enfercloud-dip
```

### 2. Instalar dependencias

```bash
cd backend
pip install -r requirements.txt
```

### 3. Iniciar el servidor

```bash
uvicorn main:app --reload --port 8000
```

### 4. Abrir la aplicación

Abre tu navegador en **[http://localhost:8000](http://localhost:8000)**

La base de datos SQLite se crea automáticamente en el primer inicio.

---

## API REST

La documentación interactiva está disponible en:

- **Swagger UI** → `http://localhost:8000/docs`
- **ReDoc** → `http://localhost:8000/redoc`

### Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/api/v1/registros/` | Listar todos los registros |
| `POST` | `/api/v1/registros/` | Crear nuevo registro |
| `GET` | `/api/v1/registros/resumen` | Obtener resumen estadístico |
| `PATCH` | `/api/v1/registros/{id}` | Actualizar registro (ej: registrar retiro) |
| `DELETE` | `/api/v1/registros/{id}` | Eliminar registro |
| `GET` | `/api/v1/exportar/excel` | Descargar planilla Excel |

---

## Tests

```bash
cd backend
pytest tests/ -v
```

```
tests/test_registros.py::test_crear_registro              PASSED
tests/test_registros.py::test_listar_registros            PASSED
tests/test_registros.py::test_ubicacion_invalida_rechazada PASSED
tests/test_registros.py::test_ubicacion_invalida_para_cvc PASSED
tests/test_registros.py::test_resumen                     PASSED
tests/test_registros.py::test_registrar_retiro            PASSED
tests/test_registros.py::test_eliminar_registro           PASSED
tests/test_registros.py::test_exportar_excel              PASSED
tests/test_registros.py::test_dip_sin_ubicacion_asignada_na PASSED

9 passed in 0.09s
```

---

## Servicios y salas configuradas

| Servicio | Salas |
|----------|-------|
| **UCI** | UCI · UTI Q |
| **UTI** | Borquez Silva · Hector Ducci · UTIM |
| **UHI** | UHI |
| **Medicina** | Manuel Matus · Gustavo Pineda · Álvaro Covarrubias · Joaquín Luco · Pérez Canto · Joel Rodríguez · Ricardo Donoso · RERA |
| **Cirugía** | Oftalmología · Ignacio Díaz · Eduardo Moore · San Daniel · San Vicente · San José · Jorge Molina · Torres Boone |

---

## Tipos de DIP soportados

| DIP | Ubicaciones válidas |
|-----|---------------------|
| CUP | GEN M · GEN F |
| CVC | YD · YI · SCD · SCI · FEM D · FEM I · BD · BI |
| VMI | TOT · TQT |
| CUP Usuario · CVC con Gripper · CHD Agudo · CHD Crónico · CHD Aféresis · PICCLINE | N/A |

---

## Principios de desarrollo

- **Clean Architecture** — dependencias apuntan hacia el dominio
- **SOLID** — un caso de uso por archivo, repositorio detrás de interfaz abstracta
- **Clean Code** — nombres expresivos, funciones pequeñas, sin comentarios obvios
- **Tests de integración** — SQLite en memoria, sin mocks de base de datos

---

## Roadmap

- [ ] Autenticación JWT por usuario
- [ ] Módulo de criterios clínicos para detección de infecciones asociadas
- [ ] Integración con plataforma Tracker (signos vitales + cultivos)
- [ ] Módulo de inteligencia artificial para diagnóstico asistido
- [ ] Hosting en producción (Railway / Render)
- [ ] Soporte multi-hospital

---

## Autor

**Bruno San Martín Navarro**
- GitHub: [@SanMaBruno](https://github.com/SanMaBruno)

---

<div align="center">

Desarrollado para mejorar la vigilancia clínica hospitalaria 🏥

</div>
