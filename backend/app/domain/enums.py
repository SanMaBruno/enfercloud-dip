from enum import Enum


class DIPTipo(str, Enum):
    CUP = "CUP"
    CVC = "CVC"
    VMI = "VMI"
    CUP_USUARIO = "CUP USUARIO"
    CVC_CON_GRIPPER = "CVC CON GRIPPER"
    CHD_AGUDO = "CHD AGUDO"
    CHD_CRONICO = "CHD CRÓNICO"
    CHD_AFERESIS = "CHD AFERESIS"
    PICCLINE = "PICCLINE"


class Estado(str, Enum):
    INCLUIDO = "INCLUIDO"
    EXCLUIDO = "EXCLUIDO"


UBICACIONES_POR_DIP: dict[DIPTipo, list[str]] = {
    DIPTipo.CUP: ["GEN M", "GEN F"],
    DIPTipo.CVC: ["YD", "YI", "SCD", "SCI", "FEM D", "FEM I", "BD", "BI"],
    DIPTipo.VMI: ["TOT", "TQT"],
}

DIPS_SIN_UBICACION = {
    DIPTipo.CUP_USUARIO,
    DIPTipo.CVC_CON_GRIPPER,
    DIPTipo.CHD_AGUDO,
    DIPTipo.CHD_CRONICO,
    DIPTipo.CHD_AFERESIS,
    DIPTipo.PICCLINE,
}
