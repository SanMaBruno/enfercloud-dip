from typing import Optional

from app.domain.enums import (
    DIPTipo, UBICACIONES_POR_DIP, DIPS_SIN_UBICACION,
    SALAS_CRITICO_TOTAL, SALAS_SEMICRITICO,
    DIPS_PROHIBIDOS_SEMICRITICO, DIPS_PROHIBIDOS_GENERAL,
)


class UbicacionInvalidaError(ValueError):
    pass


class DIPNoPermitidoEnSalaError(ValueError):
    pass


def validar_dip_en_sala(dip: DIPTipo, sala: Optional[str]) -> None:
    if sala is None:
        return

    if sala in SALAS_CRITICO_TOTAL:
        return  # todo permitido

    if sala in SALAS_SEMICRITICO:
        if dip in DIPS_PROHIBIDOS_SEMICRITICO:
            raise DIPNoPermitidoEnSalaError(
                f"{dip.value} no está permitido en {sala}. "
                f"VMI solo puede usarse en salas de cuidado crítico total: {', '.join(sorted(SALAS_CRITICO_TOTAL))}."
            )
        return

    # Sala general (Medicina / Cirugía)
    if dip in DIPS_PROHIBIDOS_GENERAL:
        raise DIPNoPermitidoEnSalaError(
            f"{dip.value} no está permitido en {sala}. "
            f"En salas de Medicina y Cirugía solo se permiten: CUP, CHD, CUP USUARIO, PICCLINE."
        )


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
