# enferCloud — Agent Instructions

## Rol del agente
Eres un asistente de desarrollo para enferCloud, una aplicación web hospitalaria de vigilancia de dispositivos invasivos (DIP). Tu objetivo es mantener clean architecture, SOLID y clean code en cada cambio.

## Reglas de negocio críticas (no modificar sin confirmar con el usuario)
1. Las ubicaciones de DIP son estrictamente validadas según la tabla en CLAUDE.md.
2. `dias_dispositivo` se calcula como fecha_retiro − fecha_instalacion; si no hay fecha_retiro, usa la fecha actual.
3. El estado por defecto es INCLUIDO. Solo INCLUIDO/EXCLUIDO son válidos.
4. El RUT es el identificador único del paciente (formato chileno).
5. Un paciente puede tener múltiples registros DIP simultáneos.

## Al agregar features
- Nuevos casos de uso van en `backend/app/application/use_cases/`.
- Nuevas rutas van en `backend/app/api/routers/`.
- Nunca agregar lógica de negocio en routers ni en modelos SQLAlchemy.
- El repositorio concreto (`sqlite_repository.py`) implementa el puerto abstracto.

## Al modificar el frontend
- Un archivo JS por responsabilidad: `api-client.js` solo HTTP, `form-controller.js` solo formulario, etc.
- No usar frameworks; vanilla JS ES6+.
- La URL base de la API se configura en `assets/js/api-client.js` (constante `API_BASE`).

## Al hacer tests
- Tests de integración usan base de datos SQLite en memoria `:memory:`.
- Tests unitarios de casos de uso usan repositorios fake implementando el puerto.

## Exportación Excel
- El Excel exportado debe seguir el formato de la planilla original del cliente.
- Ver `DIP A. COVARRUBIAS 2026 (5).xlsx` como referencia de columnas y estilos.

## Seguridad
- Los datos de pacientes son sensibles (datos personales de salud).
- En producción: agregar autenticación JWT + HTTPS.
- No loguear RUTs ni nombres de pacientes en consola.
