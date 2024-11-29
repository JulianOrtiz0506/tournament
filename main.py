"""
Archivo principal del programa para gestionar torneos de futbol.
Permite crear torneos, registrar resultados y ver clasificaciones.
"""

import os
import logging
from classes.tournament import Tournament
from classes.team import Team, validate_unique_aliases
from db_manager import save_tournament_data, load_tournament_data, save_matches

# Crear el directorio logs si no existe
if not os.path.exists('logs'):
    os.makedirs('logs')

# Configuracion del logging
logging.basicConfig(filename='logs/tournament.log', level=logging.INFO,
                    format='%(asctime)s - %(nivelname)s - %(message)s')


def create_teams():
    """Funcion para crear una lista de cuatro equipos."""
    teams = []
    for i in range(1, 5):
        while True:
            name = input(f"Ingresa el nombre del equipo {
                         i} (maximo 40 caracteres y 3 palabras): ")
            try:
                teams.append(Team(name))
                break
            except ValueError as e:
                logging.error("Error al crear el equipo: %s", e)
                print(e)

    # Validar que los alias de los equipos sean unicos
    duplicate_aliases = validate_unique_aliases(
        [team.__dict__ for team in teams])
    if duplicate_aliases:
        error_message = f"Los siguientes alias no son unicos: {
            ', '.join(duplicate_aliases)}"
        logging.error(error_message)
        print(error_message)
        return []

    return teams


def start_tournament():
    """Funcion para iniciar un torneo y programar sus partidos."""
    while True:
        name = input("Ingrese el nombre del torneo (maximo 40 caracteres): ")
        if Tournament.validate_name(name):
            break
        else:
            print("El nombre del torneo debe tener un maximo de 40 caracteres.")

    teams = create_teams()
    if not teams:
        return

    tournament = Tournament(name, teams)
    tournament.create_schedule()
    logging.info("Torneo creado y calendario de partidos generado.")
    return tournament


def show_schedule(tournament):
    """Funcion para mostrar el calendario de partidos del torneo."""
    print("\n--- Calendario de Partidos ---")
    for match in tournament.matches:
        print(f"Semana {match.week}, Partido {match.number}: {
              match.team1.name} vs {match.team2.name} - Estado: {match.status}")


def register_results(tournament):
    """Funcion para registrar los resultados de los partidos."""
    for week in range(1, 4):
        if all(m.status == "Played" for m in tournament.matches if m.week == week):
            continue  # Saltar semanas que ya tienen todos los resultados
        for number in range(1, 3):
            match = next((m for m in tournament.matches if m.week ==
                         week and m.number == number), None)
            if match:
                while True:
                    try:
                        goals_team1 = int(input(f"Ingrese los goles de {
                                          match.team1.name} (entero positivo): "))
                        goals_team2 = int(input(f"Ingrese los goles de {
                                          match.team2.name} (entero positivo): "))
                        if goals_team1 < 0 or goals_team2 < 0:
                            raise ValueError(
                                "Los goles deben ser enteros positivos.")
                        match.register_result(goals_team1, goals_team2)
                        logging.info("Resultado registrado: %s %d - %d %s",
                                     match.team1.name, goals_team1, goals_team2, match.team2.name)
                        break
                    except ValueError as e:
                        print(e)
        if week < 3:
            cont = input(
                "¿Desea ingresar los resultados de la siguiente fecha? (s/n): ")
            if cont.lower() != 's':
                return

    # Verificar si todas las semanas tienen resultados registrados
    if all(m.status == "Played" for m in tournament.matches):
        tournament.status = "Finished"
        logging.info("El torneo ha finalizado.")


def save_data(tournament):
    """Funcion para guardar los datos del torneo y de los partidos."""
    tournament_data = tournament.get_data()
    save_tournament_data(tournament_data)
    matches_data = [{"Week": m.week, "Match": m.number, "Team 1": m.team1.name,
                     "Team 2": m.team2.name, "Goals team 1": m.goals_team1,
                     "Goals team 2": m.goals_team2, "Status": m.status} for m in tournament.matches]
    save_matches(matches_data)


def load_and_show_data():
    """Funcion para cargar y mostrar los datos del torneo guardados."""
    tournament_data = load_tournament_data()
    if tournament_data:
        print("\n--- Datos del Torneo Cargados ---")
        print(f"Nombre: {tournament_data['name']}")
        print(f"ID: {tournament_data['id']}")
        print(f"Tipo: {tournament_data['type']}")
        print(f"Estado: {tournament_data['status']}")
        print("\n--- Equipos ---")
        for alias, team in tournament_data["teams"].items():
            print(f"{alias}: {
                  team['name']} - Puntos: {team['points']}, Goles: {team['goals']}")


def show_positions(tournament):
    """Funcion para mostrar las posiciones de los equipos."""
    positions = tournament.get_team_positions()
    print("\n--- Posiciones de los Equipos ---")
    for position, team in positions:
        print(f"Posicion {position}: {team.name} - Puntos: {team.points}, Diferencia de Goles: {
              team.goals - team.goals_against}, Goles a Favor: {team.goals}")


def main():
    """Funcion principal para ejecutar el gestor de torneos."""
    tournament = start_tournament()
    if tournament:
        show_schedule(tournament)
        register_results(tournament)
        save_data(tournament)
        load_and_show_data()
        show_positions(tournament)


if __name__ == "__main__":
    main()
