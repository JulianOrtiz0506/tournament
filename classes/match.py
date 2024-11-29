"""
Modulo que define la clase Match para registrar los encuentros entre equipos.
"""


class Match:
    """Clase que representa un partido entre dos equipos en el torneo."""

    def __init__(self, week, number, team1, team2):
        """Inicializa un partido entre dos equipos."""
        self.week = week
        self.number = number
        self.team1 = team1
        self.team2 = team2
        self.goals_team1 = 0
        self.goals_team2 = 0
        self.status = "Scheduled"

    def register_result(self, goals_team1, goals_team2):
        """Registra el resultado del partido y actualiza las estadisticas."""
        self.goals_team1 = goals_team1
        self.goals_team2 = goals_team2
        self.status = "Played"
        self.team1.update_statistics(goals_team1, goals_team2)
        self.team2.update_statistics(goals_team2, goals_team1)
