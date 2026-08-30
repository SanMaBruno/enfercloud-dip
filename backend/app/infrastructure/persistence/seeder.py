from datetime import date, timedelta
import random

from sqlalchemy.orm import Session

from app.infrastructure.persistence.models import RegistroDIPModel

SERVICIOS = {
    "UCI":      ["UCI", "UTI Q"],
    "UTI":      ["Borquez Silva", "Hector Ducci", "UTIM"],
    "UHI":      ["UHI"],
    "Medicina": ["Manuel Matus", "Gustavo Pineda", "Álvaro Covarrubias", "Joaquín Luco",
                 "Pérez Canto", "Joel Rodríguez", "Ricardo Donoso", "RERA"],
    "Cirugía":  ["Oftalmología", "Ignacio Díaz", "Eduardo Moore", "San Daniel",
                 "San Vicente", "San José", "Jorge Molina", "Torres Boone"],
}

DIPS = {
    "CUP":             ["GEN M", "GEN F"],
    "CVC":             ["YD", "YI", "SCD", "SCI", "FEM D", "FEM I", "BD", "BI"],
    "VMI":             ["TOT", "TQT"],
    "CUP USUARIO":     [],
    "CVC CON GRIPPER": [],
    "CHD AGUDO":       [],
    "CHD CRÓNICO":     [],
    "CHD AFERESIS":    [],
    "PICCLINE":        [],
}

NOMBRES = [
    "María González", "Juan Pérez", "Ana Martínez", "Carlos López", "Rosa Soto",
    "Pedro Ramírez", "Elena Muñoz", "Luis Herrera", "Carmen Flores", "Jorge Torres",
    "Patricia Reyes", "Miguel Díaz", "Claudia Morales", "Roberto Jiménez", "Andrea Castro",
    "Fernando Vargas", "Isabel Ruiz", "Héctor Mendoza", "Lucía Ortega", "Marcos Navarro",
    "Alejandra Silva", "Rodrigo Fuentes", "Valeria Espinoza", "Cristian Rojas", "Daniela Lagos",
    "Sebastián Contreras", "Camila Vega", "Felipe Araya", "Natalia Pizarro", "Gonzalo Mena",
    "Verónica Bravo", "Ignacio Salazar", "Javiera Campos", "Matías Riquelme", "Pilar Sandoval",
    "Diego Álvarez", "Francisca Molina", "Andrés Paredes", "Bárbara Ibáñez", "Tomás Guerrero",
    "Constanza Peña", "Nicolás Cárdenas", "Paulina Figueroa", "Esteban Aguilar", "Macarena Ríos",
    "Benjamín Núñez", "Gabriela Medina", "Emilio Gutiérrez", "Catalina Sepúlveda", "Álvaro Muñoz",
    "Sofía Arriagada", "Renata Cáceres", "Martín Herrera", "Isidora Vásquez", "Patricio Meza",
    "Lorena Pinto", "Sergio Castillo", "Amanda Rojas", "Hugo Fernández", "Ximena Sánchez",
    "Mauricio Lara", "Cecilia Fuentes", "Raúl Espinoza", "Tatiana Moreno", "Víctor Alvarado",
    "Claudia Ríos", "Óscar Navarro", "Beatriz Molina", "Samuel Torres", "Pamela Castro",
    "Rodrigo Vega", "Loreto Matus", "Cristóbal Díaz", "Yasna Araya", "Enrique Salinas",
    "Fabiola Reyes", "Claudio Herrera", "Rebeca Figueroa", "Álvaro Campos", "Antonia Ruiz",
    "Hernán Muñoz", "Valentina López", "Francisco Soto", "Paula Ramírez", "Nicolás Contreras",
    "Karina Torres", "Alejandro Pérez", "Romina Gutiérrez", "Héctor Jiménez", "Daniela Vargas",
    "Mario Flores", "Verónica Medina", "Patricio González", "Camila Ortega", "Luis Espinoza",
    "Fernanda Rojas", "Diego Pizarro", "Andrea Fuentes", "Roberto Navarro", "Marcela Morales",
]

PROCEDENCIAS = ["Urgencia", "Pabellón", "Traslado externo", "Consulta externa", "UCI"]


def _rut(i: int) -> str:
    n = 5_000_000 + i * 193_711
    return f"{n:,}".replace(",", ".") + "-" + "0123456789K"[n % 11]


def seed_demo(session: Session) -> None:
    if session.query(RegistroDIPModel).count() > 0:
        return

    rng = random.Random(42)
    today = date.today()

    for i, nombre in enumerate(NOMBRES):
        srv = rng.choice(list(SERVICIOS))
        sala = rng.choice(SERVICIOS[srv])
        dip = rng.choice(list(DIPS))
        ubics = DIPS[dip]
        ubic = rng.choice(ubics) if ubics else "N/A"
        ingreso = today - timedelta(days=rng.randint(2, 60))
        inst = ingreso + timedelta(days=rng.randint(0, 3))
        retiro = (inst + timedelta(days=rng.randint(1, 20))) if rng.random() < 0.3 else None
        estado = "EXCLUIDO" if rng.random() < 0.08 else "INCLUIDO"

        session.add(RegistroDIPModel(
            cama=str(rng.randint(1, 30)),
            servicio=srv,
            sala=sala,
            rut=_rut(i),
            nombre=nombre,
            edad=rng.randint(18, 95),
            procedencia=rng.choice(PROCEDENCIAS),
            dip=dip,
            ubicacion_dip=ubic,
            fecha_ingreso_sala=ingreso,
            fecha_instalacion=inst,
            fecha_retiro=retiro,
            estado=estado,
            observaciones="",
        ))

    session.commit()
