from soccersimulator import SoccerTeam, Simulation, show_simu
from MillaModule.Estrategias import *

# Creacion de equipos
team1 = SoccerTeam(name="Real Madrid")
team2 = SoccerTeam(name="Barcelona")

# Creacion de jugadores
team1.add("Gareth Bale", StrategieFonceur())
team1.add("Sergio Ramos", Defenseur())
team1.add("Courtois", Gardien())

team2.add("Lionel Messi", FonceurAmeliore())
team2.add("Gerard Pique", Defenseur())
team2.add("Ter Stegen", Gardien())

# Creacion del partido
simu = Simulation(team1, team2)

# Empezar simulacion
show_simu(simu)
