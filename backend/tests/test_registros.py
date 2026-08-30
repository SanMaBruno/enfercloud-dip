import pytest
from datetime import date


PAYLOAD_BASE = {
    "cama": "10A",
    "rut": "12.345.678-9",
    "nombre": "Juan Pérez",
    "dip": "CUP",
    "ubicacion_dip": "GEN M",
    "fecha_instalacion": "2026-08-01",
    "estado": "INCLUIDO",
}


def test_crear_registro(client):
    res = client.post("/api/v1/registros/", json=PAYLOAD_BASE)
    assert res.status_code == 201
    data = res.json()
    assert data["cama"] == "10A"
    assert data["dias_dispositivo"] >= 0


def test_listar_registros(client):
    client.post("/api/v1/registros/", json=PAYLOAD_BASE)
    res = client.get("/api/v1/registros/")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_ubicacion_invalida_rechazada(client):
    payload = {**PAYLOAD_BASE, "ubicacion_dip": "INVALIDA"}
    res = client.post("/api/v1/registros/", json=payload)
    assert res.status_code == 422


def test_ubicacion_invalida_para_cvc(client):
    payload = {**PAYLOAD_BASE, "dip": "CVC", "ubicacion_dip": "GEN M"}
    res = client.post("/api/v1/registros/", json=payload)
    assert res.status_code == 422


def test_resumen(client):
    client.post("/api/v1/registros/", json=PAYLOAD_BASE)
    res = client.get("/api/v1/registros/resumen")
    assert res.status_code == 200
    data = res.json()
    assert data["total_incluidos"] == 1
    assert "CUP" in data["por_dip"]


def test_registrar_retiro(client):
    r = client.post("/api/v1/registros/", json=PAYLOAD_BASE).json()
    res = client.patch(f"/api/v1/registros/{r['id']}", json={"fecha_retiro": "2026-08-15"})
    assert res.status_code == 200
    assert res.json()["fecha_retiro"] == "2026-08-15"
    assert res.json()["dias_dispositivo"] == 14


def test_eliminar_registro(client):
    r = client.post("/api/v1/registros/", json=PAYLOAD_BASE).json()
    res = client.delete(f"/api/v1/registros/{r['id']}")
    assert res.status_code == 204
    assert client.get(f"/api/v1/registros/{r['id']}").status_code == 404


def test_exportar_excel(client):
    client.post("/api/v1/registros/", json=PAYLOAD_BASE)
    res = client.get("/api/v1/exportar/excel")
    assert res.status_code == 200
    assert "spreadsheetml" in res.headers["content-type"]
    assert len(res.content) > 0


def test_dip_sin_ubicacion_asignada_na(client):
    payload = {**PAYLOAD_BASE, "dip": "PICCLINE", "ubicacion_dip": None}
    res = client.post("/api/v1/registros/", json=payload)
    assert res.status_code == 201
    assert res.json()["ubicacion_dip"] == "N/A"
