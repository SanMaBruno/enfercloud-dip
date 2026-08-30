const summaryController = {
  async reload() {
    const resumen = await apiClient.obtenerResumen();
    this.render(resumen);
  },

  render(r) {
    setText("s-total", r.total_registros);
    setText("s-incluidos", r.total_incluidos);
    setText("s-excluidos", r.total_excluidos);
    setText("s-activos", r.registros_sin_retiro);
    setText("s-promedio", r.dias_promedio_dispositivo.toFixed(1) + " días");

    const container = document.getElementById("dip-breakdown");
    container.innerHTML = "";
    Object.entries(r.por_dip).forEach(([dip, count]) => {
      const badge = document.createElement("div");
      badge.className = "dip-badge";
      badge.textContent = `${dip}: ${count}`;
      container.appendChild(badge);
    });

    if (Object.keys(r.por_dip).length === 0) {
      container.innerHTML = '<span style="color:#999;font-size:13px">Sin registros incluidos aún.</span>';
    }
  },
};

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}
