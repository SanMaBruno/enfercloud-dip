const API_BASE = "http://localhost:8000/api/v1";

async function request(method, path, body = null) {
  const options = {
    method,
    headers: { "Content-Type": "application/json" },
  };
  if (body) options.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, options);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Error desconocido" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

const apiClient = {
  crearRegistro: (data) => request("POST", "/registros/", data),
  listarRegistros: (soloActivos = false) =>
    request("GET", `/registros/?solo_activos=${soloActivos}`),
  obtenerResumen: () => request("GET", "/registros/resumen"),
  actualizarRegistro: (id, data) => request("PATCH", `/registros/${id}`, data),
  eliminarRegistro: (id) => request("DELETE", `/registros/${id}`),
  urlExportExcel: () => `${API_BASE}/exportar/excel`,
};
