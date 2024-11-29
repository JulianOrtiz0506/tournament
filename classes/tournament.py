"""
Modulo que define la clase Tournament para gestionar la creacion y administracion de torneos.
"""

import uuid
import datetime
import random
from classes.match import Match


class Tournament:
    """Clase que representa un torneo de futbol."""

    def __init__(self, name, teams):
        """Inicializa el torneo con un nombre y lista de equipos."""
        if not self.validate_name(name):
            raise ValueError(
                "El nombre del torneo debe tener un maximo de 40 caracteres.")
        if len(teams) != 4:
            raise ValueError("El torneo debe tener exactamente 4 equipos.")
        self.name = name
        self.id = str(uuid.uuid4())
        self.type = "Round robin"
        self.status = "Active"
        self.teams = {team.alias: team for team in teams}
        self.matches = []

    @staticmethod
    def validate_name(name):
        """Valida el nombre del torneo."""
        return len(name) <= 40

    def create_schedule(self):
        """Genera el calendario de partidos para el torneo."""
        random_order = list(self.teams.values())
        random.shuffle(random_order)
        encounters = [
            (random_order[0], random_order[1]),
            (random_order[2], random_order[3]),
            (random_order[0], random_order[2]),
            (random_order[1], random_order[3]),
            (random_order[0], random_order[3]),
            (random_order[1], random_order[2])
        ]
        self.matches = [Match(i // 2 + 1, i % 2 + 1, t1, t2)
                        for i, (t1, t2) in enumerate(encounters)]

    def get_data(self):
        """Devuelve los datos del torneo como un diccionario."""
        return {
            "name": self.name,
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "teams": {alias: vars(team) for alias, team in self.teams.items()},
            "matches": [{"week": m.week, "number": m.number, "team1": m.team1.name,
                         "team2": m.team2.name, "goals_team1": m.goals_team1,
                         "goals_team2": m.goals_team2, "status": m.status} for m in self.matches],
            "timestamp": datetime.datetime.now().isoformat()
        }

    def get_team_positions(self):
        """
        Lista las posiciones de los equipos ordenados por puntos,
        diferencia de goles y goles a favor.
        """
        teams_sorted = sorted(self.teams.values(), key=lambda team: (
            team.points, team.goals - team.goals_against, team.goals), reverse=True)

        positions = []
        rank = 1
        for i, team in enumerate(teams_sorted):
            if i > 0 and (teams_sorted[i].points < teams_sorted[i-1].points or
                          teams_sorted[i].goals - teams_sorted[i-1].goals !=
                          teams_sorted[i-1].goals - teams_sorted[i-1].goals_against or
                          teams_sorted[i].goals < teams_sorted[i-1].goals):
                rank = i + 1
            positions.append((rank, team))

        return positions
