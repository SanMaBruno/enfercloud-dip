# enferCloud — Vigilancia DIP

## Contexto del proyecto
Aplicación web para vigilancia de Dispositivos Invasivos en Pacientes (DIP) en salas hospitalarias.
Reemplaza una planilla Excel manual que llenaban las enfermeras diurnas.

## Cliente
Paolo — hospital sector UCI/UTI, sala A. Covarrubias.

## Stack
- **Backend**: Python 3.11+ · FastAPI · SQLAlchemy 2.x · SQLite · openpyxl
- **Frontend**: HTML5 · CSS3 · JavaScript vanilla (sin frameworks)
- **Tests**: pytest

## Estructura de carpetas
```
backend/
  app/
    domain/          # Entidades, enums, validadores (sin dependencias externas)
    application/     # Casos de uso + interfaces de puertos (depende solo de domain)
    infrastructure/  # SQLite, exportador Excel (implementa puertos)
    api/             # FastAPI routers, schemas Pydantic, DI
  main.py
frontend/
  index.html
  assets/css/
  assets/js/
```

## Principios
- Clean Architecture: dependencias apuntan hacia adentro (domain → app → infra/api)
- SOLID aplicado: un caso de uso por archivo, repos concretos detrás de interfaces abstractas
- Clean Code: nombres expresivos, sin comentarios obvios, funciones pequeñas
- Sin mocks de base de datos en tests de integración

## DIPs válidos y sus ubicaciones
| DIP | Ubicaciones permitidas |
|-----|----------------------|
| CUP | GEN M, GEN F |
| CVC | YD, YI, SCD, SCI, FEM D, FEM I, BD, BI |
| VMI | TOT, TQT |
| CUP USUARIO, CVC CON GRIPPER, CHD AGUDO, CHD CRÓNICO, CHD AFERESIS, PICCLINE | N/A |

## Estado de registro
- INCLUIDO (default)
- EXCLUIDO

## Campos calculados automáticamente
- `dias_dispositivo`: fecha_retiro − fecha_instalacion (o fecha actual si no hay retiro)
- `dias_hospitalizacion`: fecha_retiro/hoy − fecha_ingreso_sala

## Comandos de desarrollo
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Tests
pytest tests/ -v

# Frontend: abrir frontend/index.html en navegador (apunta a http://localhost:8000)
```

## Archivos de referencia originales
- `DIP A. COVARRUBIAS 2026 (5).xlsx` — planilla Excel original del cliente
- `Modulo_VBA_Vigilancia_DIP_corregido.bas` — lógica VBA con validaciones de negocio
- `Piloto_vigilancia_DIP_automatizada_xlsm.xlsm` — prototipo Excel del cliente
