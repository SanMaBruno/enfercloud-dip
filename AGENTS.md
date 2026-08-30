# enferCloud — Agent Instructions

## Rol del agente
Eres un asistente de desarrollo para enferCloud, una aplicación web hospitalaria de vigilancia de dispositivos invasivos (DIP). Tu objetivo es mantener clean architecture, SOLID y clean code en cada cambio.

## Reglas de negocio críticas (no modificar sin confirmar con el usuario)
1. Las ubicaciones de DIP son estrictamente validadas según la tabla en CLAUDE.md.
2. `dias_dispositivo` = max(0, fecha_retiro − fecha_instalacion); si no hay fecha_retiro, usa la fecha actual.
3. `dias_hospitalizacion` = max(0, fecha_retiro_o_hoy − fecha_ingreso_sala). Nunca negativo.
4. El estado por defecto es INCLUIDO. Solo INCLUIDO/EXCLUIDO son válidos.
5. Un registro "activo" es INCLUIDO + sin fecha_retiro (ambas condiciones obligatorias).
6. El RUT es el identificador del paciente (formato chileno, sin validación de dígito verificador aún).
7. Un paciente puede tener múltiples registros DIP simultáneos.

## Al agregar features
- Nuevos casos de uso van en `backend/app/application/use_cases/`.
- Nuevas rutas van en `backend/app/api/routers/`.
- Nunca agregar lógica de negocio en routers ni en modelos SQLAlchemy.
- El repositorio concreto (`sqlite_repository.py`) implementa el puerto abstracto.
- Al agregar campos de modelo: migrar con `ALTER TABLE` o recrear con `Base.metadata.create_all`.

## Al modificar el frontend
- Todo el frontend es un único `index.html` con JS vanilla inline (decisión de diseño deliberada para simplicidad de deploy).
- No usar frameworks; vanilla JS ES6+.
- La URL base de la API se configura en `assets/js/api-client.js` (constante `API_BASE`).
- Diseño responsive: sidebar como drawer en mobile (< 768px), bottom nav fija en mobile, inline en desktop.
- Tailwind vía CDN — breakpoints: `sm:` 640px, `md:` 768px, `lg:` 1024px, `xl:` 1280px.
- Compatibilidad Android: usar `top:0;bottom:0` en lugar de `inset-y:0`; `translateX(-Npx)` en lugar de `translateX(-100%)`.

## Al hacer tests
- Tests de integración usan SQLite en memoria con `StaticPool` (ver `conftest.py`).
- Ejecutar: `cd backend && python3 -m pytest tests/ -v`
- 9 tests existentes deben pasar siempre antes de hacer push.

## Validaciones de schema (Pydantic)
- `nombre`: máx 120 chars
- `observaciones`: máx 500 chars
- `fecha_retiro` >= `fecha_instalacion` (validado en `RegistroDIPCreate`)
- `ubicacion_dip` se re-valida en PATCH contra el DIP existente del registro

## Exportación Excel
- El Excel exportado sigue el formato de la planilla original del cliente.
- Columnas: N° · Cama · Servicio · Sala · Procedencia · RUT · Nombre · Edad · DIP · Ubicación DIP · F.Ingreso Sala · F.Instalación · F.Retiro · Días DIP · Días Hosp. · Estado · Observaciones
- Merge título: A1:Q1 (17 columnas).
- Ver `backend/app/infrastructure/export/excel_exporter.py`.

## Seguridad
- Los datos de pacientes son ultra-sensibles (RUT + nombre + datos clínicos → Ley 19.628 Chile).
- **NUNCA** loguear RUTs ni nombres de pacientes en consola o logs.
- En producción futura: agregar autenticación JWT + HTTPS obligatorio.
- CORS actual: `allow_origins=["*"]` — aceptable solo en demo, NO en producción real.

## Deploy (Render.com)
- Repositorio: `https://github.com/SanMaBruno/enfercloud-dip`
- Rama principal: `main` — Render hace auto-deploy en cada push.
- URL producción: `https://enfercloud-dip.onrender.com`
- Python fijado en 3.11.9 via `backend/.python-version`
- Free tier: sin disco persistente → DB se borra en cada redeploy.
- Para persistencia real: actualizar a plan $7/mes o migrar a PostgreSQL (Render ofrece Postgres gratis 500MB).
- Build command: `pip install --prefer-binary -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## Comandos de desarrollo
```bash
# Backend local
cd backend
python3 -m uvicorn main:app --reload --port 8000

# Tests
cd backend
python3 -m pytest tests/ -v

# Push a producción
git add <archivos>
git commit -m "tipo(scope): descripción"
git push origin main
# → Render despliega automáticamente en ~60s
```

## Estado del proyecto (agosto 2026)
- ✅ Backend FastAPI + SQLAlchemy + SQLite funcionando
- ✅ Clean Architecture completa (domain / application / infrastructure / api)
- ✅ 9 tests de integración pasando
- ✅ Frontend SPA responsive (mobile + tablet + desktop)
- ✅ Exportación Excel con formato hospitalario
- ✅ Deploy en Render.com con auto-deploy desde GitHub
- ⏳ Autenticación JWT — pendiente (crítico para producción real)
- ⏳ Validación dígito verificador RUT chileno — pendiente
- ⏳ Migración a PostgreSQL para persistencia real — pendiente
- ⏳ Módulo criterios clínicos infección asociada — pendiente (roadmap)
