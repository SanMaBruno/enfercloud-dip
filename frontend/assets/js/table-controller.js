let allRecords = [];

const tableController = {
  async reload() {
    allRecords = await apiClient.listarRegistros();
    this.render(allRecords);
  },

  render(records) {
    const tbody = document.getElementById("tabla-registros");
    const empty = document.getElementById("tabla-empty");

    tbody.innerHTML = "";
    if (records.length === 0) {
      empty.style.display = "block";
      return;
    }
    empty.style.display = "none";

    records.forEach((r) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${r.cama}</td>
        <td>${r.nombre}</td>
        <td>${r.rut}</td>
        <td>${r.dip}</td>
        <td>${r.ubicacion_dip || "—"}</td>
        <td>${formatDate(r.fecha_instalacion)}</td>
        <td>${r.fecha_retiro ? formatDate(r.fecha_retiro) : "Activo"}</td>
        <td><strong>${r.dias_dispositivo}</strong></td>
        <td>${r.dias_hospitalizacion ?? "—"}</td>
        <td><span class="badge ${r.estado.toLowerCase()}">${r.estado}</span></td>
        <td>
          <button class="btn-icon" title="Registrar retiro" onclick="abrirModalRetiro(${r.id}, '${escapeHtml(r.nombre)}')">🏥</button>
          <button class="btn-icon" title="Eliminar" onclick="confirmarEliminar(${r.id}, '${escapeHtml(r.nombre)}')">🗑️</button>
        </td>
      `;
      tbody.appendChild(tr);
    });
  },

  filtrar(texto) {
    const q = texto.toLowerCase();
    const filtrados = allRecords.filter(
      (r) =>
        r.nombre.toLowerCase().includes(q) ||
        r.rut.toLowerCase().includes(q) ||
        r.cama.toLowerCase().includes(q) ||
        r.dip.toLowerCase().includes(q)
    );
    this.render(filtrados);
  },
};

function formatDate(dateStr) {
  if (!dateStr) return "—";
  const [y, m, d] = dateStr.split("-");
  return `${d}/${m}/${y}`;
}

function escapeHtml(str) {
  return str.replace(/'/g, "\\'").replace(/"/g, "&quot;");
}

function initTableController() {
  document.getElementById("buscador").addEventListener("input", (e) => {
    tableController.filtrar(e.target.value);
  });

  document.getElementById("btn-solo-activos").addEventListener("change", async (e) => {
    allRecords = await apiClient.listarRegistros(e.target.checked);
    tableController.render(allRecords);
  });
}

// ── Modal retiro ──
function abrirModalRetiro(id, nombre) {
  document.getElementById("modal-retiro-nombre").textContent = nombre;
  document.getElementById("modal-retiro-fecha").value = new Date().toISOString().split("T")[0];
  document.getElementById("modal-retiro").dataset.recordId = id;
  document.getElementById("overlay-retiro").classList.add("open");
}

async function confirmarRetiro() {
  const modal = document.getElementById("modal-retiro");
  const id = modal.dataset.recordId;
  const fecha = document.getElementById("modal-retiro-fecha").value;
  if (!fecha) return;
  try {
    await apiClient.actualizarRegistro(id, { fecha_retiro: fecha });
    cerrarModalRetiro();
    await tableController.reload();
    await summaryController.reload();
  } catch (err) {
    alert("Error: " + err.message);
  }
}

function cerrarModalRetiro() {
  document.getElementById("overlay-retiro").classList.remove("open");
}

// ── Modal eliminar ──
let _deleteId = null;

function confirmarEliminar(id, nombre) {
  _deleteId = id;
  document.getElementById("modal-delete-nombre").textContent = nombre;
  document.getElementById("overlay-delete").classList.add("open");
}

async function ejecutarEliminar() {
  if (!_deleteId) return;
  try {
    await apiClient.eliminarRegistro(_deleteId);
    cerrarModalDelete();
    await tableController.reload();
    await summaryController.reload();
  } catch (err) {
    alert("Error: " + err.message);
  }
}

function cerrarModalDelete() {
  document.getElementById("overlay-delete").classList.remove("open");
  _deleteId = null;
}
