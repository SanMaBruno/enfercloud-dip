from typing import Optional

from app.domain.enums import DIPTipo, UBICACIONES_POR_DIP, DIPS_SIN_UBICACION


class UbicacionInvalidaError(ValueError):
    pass


def validar_ubicacion_dip(dip: DIPTipo, ubicacion: Optional[str]) -> Optional[str]:
    if dip in DIPS_SIN_UBICACION:
        return "N/A"

    permitidas = UBICACIONES_POR_DIP.get(dip)
    if permitidas is None:
        return ubicacion

    if not ubicacion or ubicacion.upper() not in [u.upper() for u in permitidas]:
        raise UbicacionInvalidaError(
            f"Para {dip.value}, la ubicación debe ser una de: {', '.join(permitidas)}"
        )

    return ubicacion.upper()
