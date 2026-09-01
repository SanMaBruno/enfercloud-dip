const API_BASE = window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1"
  ? "http://localhost:8000/api/v1"
  : `${window.location.origin}/api/v1`;

function getToken() {
  return localStorage.getItem("ec_token") || "";
}

async function request(method, path, body = null) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${getToken()}`,
    },
  };
  if (body !== null && body !== undefined) options.body = JSON.stringify(body);
  const res = await fetch(`${API_BASE}${path}`, options);

  if (res.status === 401) {
    localStorage.removeItem("ec_token");
    localStorage.removeItem("ec_user");
    window.location.reload();
    return;
  }

  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: "Error desconocido" }));
    throw new Error(err.detail || `HTTP ${res.status}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

const apiClient = {
  login: (username, password) => {
    const body = new URLSearchParams({ username, password });
    return fetch(`${API_BASE}/auth/login`, { method: "POST", body }).then(async res => {
      if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: "Error desconocido" }));
        throw new Error(err.detail || `HTTP ${res.status}`);
      }
      return res.json();
    });
  },

  crearUsuario:      (data)              => request("POST",   "/usuarios/", data),
  listarUsuarios:    ()                  => request("GET",    "/usuarios/"),
  eliminarUsuario:   (id)               => request("DELETE",  `/usuarios/${id}`),

  crearRegistro:    (data)              => request("POST",   "/registros/", data),
  listarRegistros:  (soloActivos=false) => request("GET",    `/registros/?solo_activos=${soloActivos}`),
  obtenerResumen:   ()                  => request("GET",    "/registros/resumen"),
  actualizarRegistro: (id, data)        => request("PATCH",  `/registros/${id}`, data),
  eliminarRegistro: (id)               => request("DELETE",  `/registros/${id}`),
  urlExportExcel: (servicio, sala) => {
    const params = new URLSearchParams();
    if (servicio) params.set('servicio', servicio);
    if (sala) params.set('sala', sala);
    params.set('token', getToken());
    const qs = params.toString();
    return `${API_BASE}/exportar/excel${qs ? '?' + qs : ''}`;
  },
};
