"""
Modulo de manejo de base de datos del torneo.
"""

import json
import csv
import os
import logging
import datetime
import platform

# Configuracion del logging
logging.basicConfig(
    filename='logs/tournament.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def load_tournament_data():
    """Carga los datos del torneo desde un archivo JSON."""
    try:
        with open("data/tournament.json", "r", encoding="utf-8") as file:
            # Verificar si el archivo esta vacio
            if os.stat("data/tournament.json").st_size == 0:
                logging.warning("El archivo de datos del torneo esta vacio.")
                return None
            return json.load(file)
    except FileNotFoundError:
        logging.warning("No se encontro el archivo de datos del torneo.")
        return None
    except (IOError, json.JSONDecodeError) as e:
        logging.error("Error al cargar los datos del torneo: %s", e)
        return None


def save_tournament_data(tournament_data):
    """Guarda los datos del torneo en un archivo JSON y registra la operacion."""
    # Verificar si ya existe un archivo tournament.json y esta en estado activo
    existing_data = load_tournament_data()
    if existing_data and existing_data.get("status") == "Active":
        error_message = "Ya existe un archivo tournament.json con un torneo activo."
        logging.error(error_message)
        raise ValueError(error_message)

    # Agregar fecha y hora, nombre del computador y version de Python
    timestamp = datetime.datetime.now().isoformat()
    computer_name = platform.node()
    python_version = platform.python_version()

    # Agregar informacion adicional
    tournament_data.update({
        'timestamp': timestamp,
        'computer_name': computer_name,
        'python_version': python_version
    })

    # Verificar si el directorio 'data' existe, si no lo crea.
    os.makedirs("data", exist_ok=True)
    try:
        with open("data/tournament.json", "w", encoding="utf-8") as file:
            json.dump(tournament_data, file, ensure_ascii=False, indent=4)
        logging.info(
            "Datos del torneo guardados correctamente en 'tournament.json'.")
    except (IOError, json.JSONDecodeError) as e:
        logging.error("Error al guardar los datos del torneo: %s", e)


def save_matches(matches_data):
    """Guarda los datos de los partidos en un archivo CSV y registra la operacion."""
    # Verificar si el directorio 'data' existe, si no lo crea.
    os.makedirs("data", exist_ok=True)
    try:
        with open("data/matches.csv", "w", newline="", encoding="utf-8") as file:
            fields = ["Week", "Match", "Team 1", "Team 2",
                      "Goals team 1", "Goals team 2", "Status"]
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(matches_data)
        logging.info(
            "Datos de los partidos guardados correctamente en 'matches.csv'.")
    except (IOError, csv.Error) as e:
        logging.error("Error al guardar los datos de los partidos: %s", e)
