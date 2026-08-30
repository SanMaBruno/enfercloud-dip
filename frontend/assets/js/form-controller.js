const UBICACIONES_POR_DIP = {
  CUP: ["GEN M", "GEN F"],
  CVC: ["YD", "YI", "SCD", "SCI", "FEM D", "FEM I", "BD", "BI"],
  VMI: ["TOT", "TQT"],
};

const DIP_SIN_UBICACION = [
  "CUP USUARIO", "CVC CON GRIPPER", "CHD AGUDO",
  "CHD CRÓNICO", "CHD AFERESIS", "PICCLINE",
];

function initFormController() {
  const form = document.getElementById("form-registro");
  const dipSelect = document.getElementById("dip");
  const ubicSelect = document.getElementById("ubicacion_dip");
  const ubicHint = document.getElementById("ubicacion-hint");
  const alert = document.getElementById("form-alert");

  dipSelect.addEventListener("change", () => actualizarUbicaciones(dipSelect.value));

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideAlert();

    const data = buildPayload();
    if (!data) return;

    try {
      await apiClient.crearRegistro(data);
      showAlert("Registro guardado correctamente.", "success");
      form.reset();
      actualizarUbicaciones("");
      await tableController.reload();
      await summaryController.reload();
    } catch (err) {
      showAlert(err.message, "error");
    }
  });

  document.getElementById("btn-limpiar").addEventListener("click", () => {
    form.reset();
    actualizarUbicaciones("");
    hideAlert();
  });

  function actualizarUbicaciones(dip) {
    const opciones = UBICACIONES_POR_DIP[dip];
    ubicSelect.innerHTML = '<option value="">— Seleccionar —</option>';
    ubicHint.textContent = "";

    if (DIP_SIN_UBICACION.includes(dip)) {
      ubicSelect.disabled = true;
      ubicHint.textContent = "No aplica ubicación para este DIP.";
      return;
    }
    ubicSelect.disabled = !opciones;
    if (opciones) {
      opciones.forEach((u) => {
        const opt = document.createElement("option");
        opt.value = u;
        opt.textContent = u;
        ubicSelect.appendChild(opt);
      });
      ubicHint.textContent = `Ubicaciones válidas: ${opciones.join(", ")}`;
    }
  }

  function buildPayload() {
    const get = (id) => document.getElementById(id).value.trim();
    const cama = get("cama");
    const rut = get("rut");
    const nombre = get("nombre");
    const dip = get("dip");
    const fechaInstalacion = get("fecha_instalacion");

    if (!cama || !rut || !nombre || !dip || !fechaInstalacion) {
      showAlert("Complete los campos obligatorios: Cama, RUT, Nombre, DIP y Fecha de instalación.", "error");
      return null;
    }

    return {
      cama,
      rut,
      nombre,
      dip,
      fecha_instalacion: fechaInstalacion,
      estado: get("estado") || "INCLUIDO",
      edad: get("edad") ? parseInt(get("edad")) : null,
      procedencia: get("procedencia") || null,
      ubicacion_dip: get("ubicacion_dip") || null,
      fecha_ingreso_sala: get("fecha_ingreso_sala") || null,
      fecha_retiro: get("fecha_retiro") || null,
      observaciones: get("observaciones") || null,
    };
  }

  function showAlert(msg, type) {
    alert.textContent = msg;
    alert.className = `alert ${type} visible`;
  }

  function hideAlert() {
    alert.className = "alert";
  }
}
