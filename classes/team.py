"""
Modulo que define la clase Team para representar a un equipo.
"""


def validate_unique_aliases(teams):
    """Valida que todos los alias de los equipos sean unicos."""
    seen_aliases = set()
    duplicate_aliases = []
    for team in teams:
        alias = team.get("alias")
        if alias in seen_aliases:
            duplicate_aliases.append(alias)
        else:
            seen_aliases.add(alias)
    return duplicate_aliases


class Team:
    """Clase que representa un equipo en el torneo."""

    def __init__(self, name):
        """Inicializa el equipo con sus atributos."""
        if not self.validate_name(name):
            raise ValueError(
                "El nombre del equipo debe tener un maximo de 40 caracteres y 3 palabras.")
        self.name = name
        self.alias = self.generate_alias(name)
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.goals = 0
        self.goals_against = 0
        self.points = 0

    @staticmethod
    def validate_name(name):
        """Valida el nombre del equipo."""
        return len(name) <= 40 and len(name.split()) <= 3

    def generate_alias(self, name):
        """Genera un alias basado en las reglas definidas."""
        words = name.split()
        if len(words) == 3:
            return ''.join([word[0].upper() for word in words])
        elif len(words) == 2:
            return words[0][0].upper() + words[1][:2].upper()
        else:
            return name[:3].upper()

    def update_statistics(self, goals, goals_against):
        """Actualiza las estadisticas del equipo."""
        self.goals += goals
        self.goals_against += goals_against
        if goals > goals_against:
            self.wins += 1
            self.points += 3
        elif goals == goals_against:
            self.draws += 1
            self.points += 1
        else:
            self.losses += 1
